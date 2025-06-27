from typing import Optional, List
from pydantic import BaseModel

DEFAULT_MODEL_NAME = "gemini-1.5-flash"

class UnifiedQuery(BaseModel):
    query: str
    thread_id: Optional[str] = "default"
    model: Optional[str] = DEFAULT_MODEL_NAME
    enabled_tools: Optional[List[str]] = None

class UnifiedResponse(BaseModel):
    response: str
    thread_id: str
    # tools_used: List[str] 

class ToolStatus(BaseModel):
    name: str
    status: str 
    error_message: Optional[str] = None

class AgentStatusResponse(BaseModel):
    available_tools: List[ToolStatus]
    total_tools: int