"""
Gmail tool implementation
"""
import os
import logging
from langchain_google_community import GmailToolkit
from langchain_google_community.gmail.utils import (
    build_resource_service as build_gmail_service,
    get_gmail_credentials,
)
from typing import List
from langchain_core.tools import BaseTool
from src.models.api_models import ToolStatus

logger = logging.getLogger(__name__)

class GmailTool:
    """Gmail Tool implementation"""
    
    def __init__(self):
        self.toolkit = None
        self.tools: List[BaseTool] = []
        self.status = ToolStatus(name="gmail", status="not_initialized")
        self._initialize_tools()
    
    def _initialize_tools(self):
        """Initialize Gmail tools with proper error handling"""
        try:
            gmail_credentials = get_gmail_credentials(
                token_file="token.json",
                scopes=["https://mail.google.com/"],
                client_secrets_file="src/config/credentials.json",
            )
            gmail_resource = build_gmail_service(credentials=gmail_credentials)
            self.toolkit = GmailToolkit(api_resource=gmail_resource)
            self.tools = self.toolkit.get_tools()
            self.status = ToolStatus(name="gmail", status="enabled")
            logger.info(f"Gmail tools initialized: {len(self.tools)} tools - {[tool.name for tool in self.tools]}")
        except Exception as e:
            self.status = ToolStatus(
                name="gmail", 
                status="error", 
                error_message=str(e)
            )
            logger.error(f"Failed to initialize Gmail tools: {e}")
            
    def get_tools(self) -> List[BaseTool]:
        """Return all initialized Gmail tools"""
        return self.tools
        
    def get_status(self) -> ToolStatus:
        """Return the current status of the Gmail tools"""
        return self.status
