import sys
import os
from datetime import datetime, timedelta
from src.integrations.google_client import GoogleClient
from src.helpers.llm_client import GeminiClient
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


class CalendarAgent:
    def __init__(self):
        self.google_client = GoogleClient()
        self.llm_client = GeminiClient()
        
    def run(self, days_ahead=2):
        """
        Run calendar agent to collect and analyze calendar events
        
        Args:
            days_ahead (int): Number of days to look ahead
            
        Returns:
            dict: Calendar events data and summary
        """
        try:
            print("📅 Calendar Agent: Retrieving upcoming meetings...")
            
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                        
            events = self.google_client.get_todays_events()
            
            if not events or len(events) == 0:
                return {"summary": "No upcoming meetings found.", "events": []}
            
            summary = self.llm_client.summarize_meetings(events)
            
            return {
                "summary": summary,
                "events": events
            }
        
        except Exception as e:
            error_msg = f"Error in Calendar Agent: {str(e)}"
            print(error_msg)
            return {"summary": error_msg, "events": []}
