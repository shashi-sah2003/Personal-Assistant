import sys
import os
from datetime import datetime, timedelta
from src.integrations.ms_graph_client import MSGraphClient
from src.helpers.llm_client import GeminiClient
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


class CalendarAgent:
    def __init__(self, use_mock_data=False):
        self.ms_graph_client = MSGraphClient(use_mock_data=use_mock_data)
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
            
            end_date = (today + timedelta(days=days_ahead)).replace(hour=23, minute=59, second=59)
            
            start_time = today.isoformat() + "Z"
            end_time = end_date.isoformat() + "Z"
            
            events = self.ms_graph_client.get_calendar_events(
                start_time=start_time,
                end_time=end_time,
                top=50
            )
            
            if not events or 'value' not in events or len(events['value']) == 0:
                return {"summary": "No upcoming meetings found.", "events": []}
            
            summary = self.llm_client.summarize_meetings(events)
            
            return {
                "summary": summary,
                "events": events['value']
            }
        
        except Exception as e:
            error_msg = f"Error in Calendar Agent: {str(e)}"
            print(error_msg)
            return {"summary": error_msg, "events": []}
