import logging
from typing import List
import os
from langchain_openai import AzureChatOpenAI

logger = logging.getLogger(__name__)

class ToolSelector:
    """Intelligently selects which tools are needed for a given query using LLM"""
    
    def __init__(self):
        """Initialize the tool selector with an LLM"""
        try:
            self.llm = AzureChatOpenAI(
                openai_api_key=os.environ["AZURE_OPENAI_API_KEY"],
                azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
                azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
                api_version=os.environ["AZURE_OPENAI_API_VERSION"],
                temperature=0,
                max_tokens=50  
            )
            logger.info("Tool selector initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize tool selector: {e}")
            self.llm = None

    def select_tools(self, query: str, available_tools: List[str]) -> List[str]:
        """
        Analyze the query and determine which tools are likely needed
        
        Args:
            query: The user query
            available_tools: List of available tool categories
            
        Returns:
            List of tool categories that should be used for this query
        """
        if not self.llm:
            logger.warning("Tool selector LLM not initialized, using all tools")
            return available_tools
        
        try:
            prompt = f"""Given the following user query:
                    "{query}"

                    Available tools and their purposes:
                    - jira: For Jira ticket related tasks
                    - calendar: For calendar events and scheduling
                    - gmail: For email related tasks
                    - slack: For Slack messages and channels

                    Select ONLY the essential tools needed to directly answer this query.
                    Be precise and avoid selecting tools that aren't strictly necessary.

                    Respond ONLY with a comma-separated list of the tool names that are needed.
                    Don't include explanations, just the tool names.
                    """
            
            response = self.llm.invoke(prompt).content.strip()
            
            selected_tools = [
                tool.strip().lower() 
                for tool in response.split(',')
                if tool.strip().lower() in [t.lower() for t in available_tools]
            ]
            
            if not selected_tools:
                logger.warning(f"No valid tools selected for query, using all tools: '{query}'")
                return available_tools
                
            logger.info(f"Selected tools for query: {selected_tools}")
            return selected_tools
            
        except Exception as e:
            logger.error(f"Error selecting tools: {e}")
            return available_tools