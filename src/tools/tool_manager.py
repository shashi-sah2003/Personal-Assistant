import logging
from typing import Dict, List, Any
from langchain_core.tools import BaseTool
from src.models.api_models import ToolStatus
from src.tools.jira.tool import JiraTool
from src.tools.calendar.tool import CalendarTool
from src.tools.gmail.tool import GmailTool
from src.tools.slack.tool import SlackTool

logger = logging.getLogger(__name__)


class ToolManager:
    """Manages all toolkit integrations with error handling and selective enabling"""
    
    def __init__(self):
        self.tools: List[BaseTool] = []
        self.tool_instances: Dict[str, Any] = {}
        self._initialize_tools()
    
    def _initialize_tools(self):
        """Initialize all available tools with proper error handling"""
        
        self.tool_instances["jira"] = JiraTool()
        self.tool_instances["calendar"] = CalendarTool()
        self.tool_instances["gmail"] = GmailTool()
        self.tool_instances["slack"] = SlackTool()
        
        for tool_name, tool_instance in self.tool_instances.items():
            self.tools.extend(tool_instance.get_tools())
        
        logger.info(f"Total tools initialized: {len(self.tools)}")
    
    def get_filtered_tools(self, enabled_tools: List[str]) -> List[BaseTool]:
        """Get only the tools that are enabled and requested"""
        if not enabled_tools:
            return self.tools
        
        filtered_tools = []
        for tool in self.tools:
            tool_name = self._get_tool_category(tool)
            tool_instance = self.tool_instances.get(tool_name)
            if tool_name in enabled_tools and tool_instance and tool_instance.get_status().status == "enabled":
                filtered_tools.append(tool)
        return filtered_tools
    
    def _get_tool_category(self, tool: BaseTool) -> str:
        """Determine which category a tool belongs to based on its name or class"""
        tool_name = tool.name.lower()
        tool_class = tool.__class__.__name__.lower()
        
        if "jira" in tool_name or "jira" in tool_class:
            return "jira"
        elif "calendar" in tool_name or "calendar" in tool_class:
            return "calendar"
        elif "gmail" in tool_name or "mail" in tool_name or "gmail" in tool_class:
            return "gmail"
        elif "slack" in tool_name or "slack" in tool_class:
            return "slack"
        return "unknown"
    
    def get_tool_status(self) -> List[ToolStatus]:
        """Get status of all tools"""
        return [tool_instance.get_status() for tool_instance in self.tool_instances.values()]
