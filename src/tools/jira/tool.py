"""
JIRA tool implementation
"""
import os
import logging
from langchain_community.agent_toolkits.jira.toolkit import JiraToolkit
from langchain_community.utilities.jira import JiraAPIWrapper
from typing import List
from langchain_core.tools import BaseTool
from src.models.api_models import ToolStatus

logger = logging.getLogger(__name__)

class JiraTool:
    """JIRA Tool implementation"""
    
    def __init__(self):
        self.toolkit = None
        self.tools: List[BaseTool] = []
        self.status = ToolStatus(name="jira", status="not_initialized")
        self._initialize_tools()
    
    def _initialize_tools(self):
        """Initialize JIRA tools with proper error handling"""
        try:
            jira = JiraAPIWrapper(
                jira_username=os.getenv("JIRA_USERNAME"),
                jira_api_token=os.getenv("JIRA_API_TOKEN"),
                jira_instance_url=os.getenv("JIRA_URL"),
                jira_cloud=True
            )
            self.toolkit = JiraToolkit.from_jira_api_wrapper(jira)
            self.tools = self.toolkit.get_tools()
            self.status = ToolStatus(name="jira", status="enabled")
            logger.info(f"JIRA tools initialized: {len(self.tools)} tools - {[tool.name for tool in self.tools]}")
        except Exception as e:
            self.status = ToolStatus(
                name="jira", 
                status="error", 
                error_message=str(e)
            )
            logger.error(f"Failed to initialize JIRA tools: {e}")
            
    def get_tools(self) -> List[BaseTool]:
        """Return all initialized JIRA tools"""
        return self.tools
        
    def get_status(self) -> ToolStatus:
        """Return the current status of the JIRA tools"""
        return self.status
