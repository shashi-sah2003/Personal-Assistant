import sys
import os
from src.integrations.google_client import GoogleClient
from src.helpers.llm_client import GeminiClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


class EmailAgent:
    def __init__(self):
        self.google_client = GoogleClient()
        self.llm_client = GeminiClient()
        
    def run(self, max_results=20):
        """
        Run email agent to collect and analyze email data
        
        Args:
            top (int): Maximum number of emails to retrieve
            days (int): Number of days to look back
            
        Returns:
            dict: Email data and summary
        """
        try:
            print("📧 Email Agent: Retrieving recent emails from Gmail...")
            
            emails = self.google_client.get_todays_emails(max_results=max_results)
            
            if not emails:
                return {"summary": "No recent emails found.", "emails": []}
                
            summary = self.llm_client.summarize_emails(emails)
            
            return {
                "summary": summary,
                "emails": emails
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
