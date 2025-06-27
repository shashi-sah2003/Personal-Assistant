"""
Abstract base class for all tools
"""
from abc import ABC, abstractmethod
import logging
from typing import List
from langchain_core.tools import BaseTool
from src.models.api_models import ToolStatus

logger = logging.getLogger(__name__)

class AbstractTool(ABC):
    """Abstract base class for all tools"""
    
    def __init__(self, name: str):
        self.name = name
        self.toolkit = None
        self.tools: List[BaseTool] = []
        self.status = ToolStatus(name=name, status="not_initialized")
        self._initialize_tools()
    
    @abstractmethod
    def _initialize_tools(self):
        """Initialize tools with proper error handling"""
        pass
        
    def get_tools(self) -> List[BaseTool]:
        """Return all initialized tools"""
        return self.tools
        
    def get_status(self) -> ToolStatus:
        """Return the current status of the tools"""
        return self.status
