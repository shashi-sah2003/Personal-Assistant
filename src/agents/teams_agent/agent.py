import sys
import os
from src.integrations.ms_graph_client import MSGraphClient
from src.helpers.llm_client import GeminiClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


class TeamsAgent:
    def __init__(self, use_mock_data=False):
        self.ms_graph_client = MSGraphClient(use_mock_data=use_mock_data)
        self.llm_client = GeminiClient()
        
    def run(self, top=20):
        """
        Run Teams agent to collect and analyze Teams messages
        
        Args:
            top (int): Maximum number of messages to retrieve
            
        Returns:
            dict: Teams messages data and summary
        """
        try:
            print("💬 Teams Agent: Retrieving recent messages...")
            
            messages = self.ms_graph_client.get_teams_chats(top=top)
            
            if not messages or 'value' not in messages or len(messages['value']) == 0:
                return {"summary": "No recent Teams messages found.", "messages": []}
            
            summary = self.llm_client.summarize_teams_messages(messages)
            
            return {
                "summary": summary,
                "messages": messages['value']
            }
        
        except Exception as e:
            error_msg = f"Error in Teams Agent: {str(e)}"
            print(error_msg)
            return {"summary": error_msg, "messages": []}
