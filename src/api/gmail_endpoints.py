import os
from fastapi import APIRouter, HTTPException, Body
from typing import Optional
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from langchain_google_community import GmailToolkit
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv
from langfuse import observe
from langchain_google_community.gmail.utils import (
    build_resource_service,
    get_gmail_credentials,
)

load_dotenv()

DEFAULT_MODEL_NAME = "gemini-1.5-flash"

class GmailQuery(BaseModel):
    query: str
    thread_id: Optional[str] = "default"
    model: Optional[str] = DEFAULT_MODEL_NAME

class GmailResponse(BaseModel):
    response: str
    thread_id: str

router = APIRouter(
    prefix="/api/gmail",
    tags=["gmail"],
    responses={404: {"description": "Not found"}},
)

memory = MemorySaver()

credentials = get_gmail_credentials(
    token_file="token.json",
    scopes=["https://mail.google.com/"],
    client_secrets_file="src/config/credentials.json",
)

api_resource = build_resource_service(credentials=credentials)

toolkit = GmailToolkit(api_resource=api_resource)
tools = toolkit.get_tools()

def get_agent_executor(model_name=DEFAULT_MODEL_NAME):
    llm = ChatGoogleGenerativeAI(
        api_key=os.getenv("GEMINI_API_KEY"),
        model=model_name,
        temperature=0
    )
    return create_react_agent(
        llm,
        tools,
        checkpointer=memory
    )

_agent_executors = {}

def get_or_create_agent(model_name):
    if model_name not in _agent_executors:
        _agent_executors[model_name] = get_agent_executor(model_name)
    return _agent_executors[model_name]

@observe(name="gmail_agent_query")
def run_gmail_agent(query: str, thread_id: str = "default", model_name: str = DEFAULT_MODEL_NAME):
    agent_executor = get_or_create_agent(model_name)
    config = {"configurable": {"thread_id": thread_id}}
    result = agent_executor.invoke(
        {"messages": [HumanMessage(content=query)]},
        config=config
    )
    return result["messages"][-1].content

@router.post("/query", response_model=GmailResponse)
async def query_gmail(gmail_query: GmailQuery = Body(...)):
    try:
        response = run_gmail_agent(
            gmail_query.query,
            gmail_query.thread_id,
            gmail_query.model
        )
        return GmailResponse(
            response=response,
            thread_id=gmail_query.thread_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing Gmail query: {str(e)}")

@router.get("/conversation/{thread_id}")
async def get_conversation(thread_id: str):
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