import sys
import os
from src.integrations.slack_client import SlackClient
from src.helpers.llm_client import GeminiClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")


class SlackAgent:
    def __init__(self):
        self.slack_client = SlackClient(bot_token=SLACK_BOT_TOKEN)
        self.llm_client = GeminiClient()
        
    def run(self, top=20):
        """
        Run Slack agent to collect and analyze Slack messages
        
        Args:
            top (int): Maximum number of messages to retrieve
            
        Returns:
            dict: Slack messages data and summary
        """
        try:
            print("💬 Slack Agent: Retrieving recent messages...")
            
            messages = self.slack_client.get_todays_messages()
            
            if not messages or len(messages) == 0:
                return {"summary": "No recent Slack messages found.", "messages": []}
            
            summary = self.llm_client.summarize_slack_messages(messages)
            
            return {
                "summary": summary,
                "messages": messages
            }
        
        except Exception as e:
            error_msg = f"Error in Slack Agent: {str(e)}"
            print(error_msg)
            return {"summary": error_msg, "messages": []}
