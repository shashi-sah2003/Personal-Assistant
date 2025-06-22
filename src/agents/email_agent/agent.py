import sys
import os
from src.integrations.ms_graph_client import MSGraphClient
from src.helpers.llm_client import GeminiClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


class EmailAgent:
    def __init__(self, use_mock_data=False):
        self.ms_graph_client = MSGraphClient(use_mock_data=use_mock_data)
        self.llm_client = GeminiClient()
        
    def run(self, top=10, days=1):
        """
        Run email agent to collect and analyze email data
        
        Args:
            top (int): Maximum number of emails to retrieve
            days (int): Number of days to look back
            
        Returns:
            dict: Email data and summary
        """
        try:
            print("📧 Email Agent: Retrieving recent emails...")
            
            filter_criteria = f"receivedDateTime ge {self._get_date_filter(days)}"
            emails = self.ms_graph_client.get_emails(top=top, filter_criteria=filter_criteria)
            
            if not emails or 'value' not in emails or len(emails['value']) == 0:
                return {"summary": "No recent emails found.", "emails": []}
                
            summary = self.llm_client.summarize_emails(emails)
            
            return {
                "summary": summary,
                "emails": emails['value']
            }
        
        except Exception as e:
            error_msg = f"Error in Email Agent: {str(e)}"
            print(error_msg)
            return {"summary": error_msg, "emails": []}
    
    def _get_date_filter(self, days):
        """Helper to create a date filter string for MS Graph API"""
        from datetime import datetime, timedelta
        date = (datetime.utcnow() - timedelta(days=days)).isoformat() + 'Z'
        return date
