import os
from fastapi import APIRouter, HTTPException, Body
from typing import Optional
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from langchain_community.agent_toolkits import SlackToolkit
from langchain_openai import AzureChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv
from langfuse import observe

load_dotenv()

class SlackQuery(BaseModel):
    query: str
    thread_id: Optional[str] = "default"

class SlackResponse(BaseModel):
    response: str
    thread_id: str

router = APIRouter(
    prefix="/api/slack",
    tags=["slack"],
    responses={404: {"description": "Not found"}},
)

memory = MemorySaver()

toolkit = SlackToolkit()
tools = toolkit.get_tools()

def get_agent_executor():
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

# Singleton agent executor
agent_executor = get_agent_executor()

@observe(name="slack_agent_query")
def run_slack_agent(query: str, thread_id: str = "default"):
    config = {"configurable": {"thread_id": thread_id}}
    result = agent_executor.invoke(
        {"messages": [HumanMessage(content=query)]},
        config=config
    )
    return result["messages"][-1].content

@router.post("/query", response_model=SlackResponse)
async def query_slack(slack_query: SlackQuery = Body(...)):
    try:
        response = run_slack_agent(
            slack_query.query,
            slack_query.thread_id
        )
        return SlackResponse(
            response=response,
            thread_id=slack_query.thread_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing Slack query: {str(e)}")

@router.get("/conversation/{thread_id}")
async def get_conversation(thread_id: str):
    try:
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