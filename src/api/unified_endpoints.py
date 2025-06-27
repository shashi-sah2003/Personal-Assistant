import os
from fastapi import APIRouter, HTTPException, Body
from typing import List, Dict, Any
from langchain_core.messages import HumanMessage
from langchain_openai import AzureChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv
from langfuse import observe
from src.models.api_models import UnifiedQuery, UnifiedResponse
from src.tools.tool_manager import ToolManager
from src.tools.tool_selector import ToolSelector

from src.models.api_models import DEFAULT_MODEL_NAME
import logging

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/unified",
    tags=["unified-agent"],
    responses={404: {"description": "Not found"}},
)

memory = MemorySaver()

tool_manager = ToolManager()
tool_selector = ToolSelector()

def get_agent_executor(model_name: str = DEFAULT_MODEL_NAME, enabled_tools: List[str] = None):
    """Create an agent executor with specified model and tools"""
    llm = AzureChatOpenAI(
        openai_api_key=os.environ["AZURE_OPENAI_API_KEY"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
        api_version=os.environ["AZURE_OPENAI_API_VERSION"],
        temperature=0,
    )
    
    tools = tool_manager.get_filtered_tools(enabled_tools or ["jira", "calendar", "gmail", "slack"])
    
    if not tools:
        raise HTTPException(
            status_code=500, 
            detail="No tools available. Please check tool configurations."
        )
    
    return create_react_agent(
        llm, 
        tools, 
        checkpointer=memory
    )

_agent_executors: Dict[str, Any] = {}

def get_or_create_agent(model_name: str, enabled_tools: List[str]):
    """Get existing agent or create a new one"""
    cache_key = f"{model_name}_{'-'.join(sorted(enabled_tools))}"
    
    if cache_key not in _agent_executors:
        _agent_executors[cache_key] = get_agent_executor(model_name, enabled_tools)
    
    return _agent_executors[cache_key]

@observe(name="unified_agent_query")
def run_unified_agent(
    query: str, 
    thread_id: str = "default", 
    model_name: str = DEFAULT_MODEL_NAME,
    enabled_tools: List[str] = None
):
    """
    Run the unified agent with all available tools
    
    Args:
        query: The question or task to ask the agent
        thread_id: Unique identifier for the conversation thread
        model_name: Model name to use for the agent
        enabled_tools: List of tools to enable for this query
    """
    available_tools = ["jira", "calendar", "gmail", "slack"]

    if not enabled_tools:
        selected_tools = tool_selector.select_tools(query, available_tools)
        logger.info(f"Intelligently selected tools for query: {selected_tools}")
        enabled_tools = selected_tools
    else:
        logger.info(f"Using explicitly specified tools: {enabled_tools}")
    
    agent_executor = get_or_create_agent(model_name, enabled_tools)    

    
    config = {"configurable": {"thread_id": thread_id}}
    
    try:
        result = agent_executor.invoke(
            {"messages": [HumanMessage(content=query)]},
            config=config
        )
        
        return result["messages"][-1].content
    
    except Exception as e:
        logger.error(f"Error in agent execution: {e}")
        raise

@router.post("/query", response_model=UnifiedResponse)
async def query_unified_agent(unified_query: UnifiedQuery = Body(...)):
    """Send a query to the unified agent and get a response"""
    try:
        response = run_unified_agent(
            unified_query.query,
            unified_query.thread_id,
            unified_query.model,
            unified_query.enabled_tools
        )
        return UnifiedResponse(
            response=response,
            thread_id=unified_query.thread_id,
        )
    except Exception as e:
        logger.error(f"Error processing unified query: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing unified query: {str(e)}"
        )
