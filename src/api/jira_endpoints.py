import os
from fastapi import APIRouter, HTTPException, Body
from typing import Optional
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from langchain_community.agent_toolkits.jira.toolkit import JiraToolkit
from langchain_community.utilities.jira import JiraAPIWrapper
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
from langfuse import observe 

load_dotenv()

DEFAULT_MODEL_NAME = "gemini-1.5-flash"

class JiraQuery(BaseModel):
    query: str
    thread_id: Optional[str] = "default"

class JiraResponse(BaseModel):
    response: str
    thread_id: str

router = APIRouter(
    prefix="/api/jira",
    tags=["jira"],
    responses={404: {"description": "Not found"}},
)

memory = MemorySaver()

jira = JiraAPIWrapper(
    jira_username=os.getenv("JIRA_USERNAME"),
    jira_api_token=os.getenv("JIRA_API_TOKEN"),
    jira_instance_url=os.getenv("JIRA_URL"),
    jira_cloud=True
)
toolkit = JiraToolkit.from_jira_api_wrapper(jira)
tools = toolkit.get_tools()

def get_agent_executor(model_name=DEFAULT_MODEL_NAME):
    """Create an agent executor with specified model"""
    llm = AzureChatOpenAI(
        openai_api_key=os.environ["AZURE_OPENAI_API_KEY"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
        api_version=os.environ["AZURE_OPENAI_API_VERSION"],
        temperature=0,
    )

    return create_react_agent(
        llm, 
        tools, 
        checkpointer=memory
    )

_agent_executors = {}

def get_or_create_agent(model_name):
    """Get existing agent or create a new one"""
    if model_name not in _agent_executors:
        _agent_executors[model_name] = get_agent_executor(model_name)
    return _agent_executors[model_name]

@observe(name="jira_agent_query")
def run_jira_agent(query: str, thread_id: str = "default", model_name: str = DEFAULT_MODEL_NAME):
    """
    Run the JIRA agent with a given query
    
    Args:
        query: The question or task to ask the agent
        thread_id: Unique identifier for the conversation thread
        model_name: Model name to use for the agent
    """
    agent_executor = get_or_create_agent(model_name)
    config = {"configurable": {"thread_id": thread_id}}

    result = agent_executor.invoke(
        {"messages": [HumanMessage(content=query)]},
        config=config
    )
    
    return result["messages"][-1].content

@router.post("/query", response_model=JiraResponse)
async def query_jira(jira_query: JiraQuery = Body(...)):
    """Send a query to the JIRA agent and get a response"""
    try:
        response = run_jira_agent(
            jira_query.query, 
            jira_query.thread_id, 
            jira_query.model
        )
        return JiraResponse(
            response=response,
            thread_id=jira_query.thread_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing JIRA query: {str(e)}")

@router.get("/conversation/{thread_id}")
async def get_conversation(thread_id: str):
    """Get conversation history for a specific thread"""
    try:
        agent_executor = next(iter(_agent_executors.values())) if _agent_executors else get_agent_executor()
        
        config = {"configurable": {"thread_id": thread_id}}
        state = agent_executor.get_state(config)
        messages = state.values.get("messages", [])
        
        formatted_messages = []
        for msg in messages:
            formatted_messages.append({
                "role": msg.__class__.__name__.replace("Message", "").lower(),
                "content": msg.content,
                "id": getattr(msg, "id", None)
            })
        
        return {"thread_id": thread_id, "messages": formatted_messages}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving conversation: {str(e)}")