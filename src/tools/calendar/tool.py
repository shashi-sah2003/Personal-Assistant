"""
Calendar tool implementation
"""
import os
import logging
from langchain_google_community import CalendarToolkit
from langchain_google_community.calendar.utils import (
    build_resource_service as build_calendar_service,
    get_google_credentials as get_calendar_credentials,
)
from typing import List
from langchain_core.tools import BaseTool
from src.models.api_models import ToolStatus

logger = logging.getLogger(__name__)

class CalendarTool:
    """Calendar Tool implementation"""
    
    def __init__(self):
        self.toolkit = None
        self.tools: List[BaseTool] = []
        self.status = ToolStatus(name="calendar", status="not_initialized")
        self._initialize_tools()
    
    def _initialize_tools(self):
        """Initialize Calendar tools with proper error handling"""
        try:
            calendar_credentials = get_calendar_credentials(
                token_file="token.json",
                scopes=["https://www.googleapis.com/auth/calendar"],
                client_secrets_file="src/config/credentials.json",
            )
            calendar_resource = build_calendar_service(credentials=calendar_credentials)
            self.toolkit = CalendarToolkit(api_resource=calendar_resource)
            self.tools = self.toolkit.get_tools()
            self.status = ToolStatus(name="calendar", status="enabled")
            logger.info(f"Calendar tools initialized: {len(self.tools)} tools - {[tool.name for tool in self.tools]}")
        except Exception as e:
            self.status = ToolStatus(
                name="calendar", 
                status="error", 
                error_message=str(e)
            )
            logger.error(f"Failed to initialize Calendar tools: {e}")
            
    def get_tools(self) -> List[BaseTool]:
        """Return all initialized Calendar tools"""
        return self.tools
        
    def get_status(self) -> ToolStatus:
        """Return the current status of the Calendar tools"""
        return self.status
