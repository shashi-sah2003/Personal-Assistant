"""
Slack tool implementation
"""
import os
import logging
from langchain_community.agent_toolkits import SlackToolkit
from typing import List
from langchain_core.tools import BaseTool
from src.models.api_models import ToolStatus

logger = logging.getLogger(__name__)

class SlackTool:
    """Slack Tool implementation"""
    
    def __init__(self):
        self.toolkit = None
        self.tools: List[BaseTool] = []
        self.status = ToolStatus(name="slack", status="not_initialized")
        self._initialize_tools()
    
    def _initialize_tools(self):
        """Initialize Slack tools with proper error handling"""
        try:
            self.toolkit = SlackToolkit()
            self.tools = self.toolkit.get_tools()
            self.status = ToolStatus(name="slack", status="enabled")
            logger.info(f"Slack tools initialized: {len(self.tools)} tools - {[tool.name for tool in self.tools]}")
        except Exception as e:
            self.status = ToolStatus(
                name="slack", 
                status="error", 
                error_message=str(e)
            )
            logger.error(f"Failed to initialize Slack tools: {e}")
            
    def get_tools(self) -> List[BaseTool]:
        """Return all initialized Slack tools"""
        return self.tools
        
    def get_status(self) -> ToolStatus:
        """Return the current status of the Slack tools"""
        return self.status
