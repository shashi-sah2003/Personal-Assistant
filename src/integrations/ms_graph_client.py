import os
from dotenv import load_dotenv
import msal
import requests
from datetime import datetime, timedelta

load_dotenv()

try:
    from src.helpers.mock_data import MockMSGraphData
except ImportError:
    class MockMSGraphData:
        @staticmethod
        def get_email_data():
            return {"value": []}
        
        @staticmethod
        def get_calendar_data():
            return {"value": []}
        
        @staticmethod
        def get_teams_data():
            return {"value": []}

class MSGraphClient:
    def __init__(self, use_mock_data=False):
        """
        Initialize the Microsoft Graph API Client
        
        Args:
            use_mock_data (bool): If True, use mock data instead of real API calls
        """
        self.client_id = os.getenv("MS_CLIENT_ID")
        self.client_secret = os.getenv("MS_CLIENT_SECRET")
        self.tenant_id = os.getenv("MS_TENANT_ID")
        self.authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        self.scope = ["https://graph.microsoft.com/.default"]
        self.endpoint = "https://graph.microsoft.com/v1.0"
        self.token = None
        self.token_expiry = None
        self.use_mock_data = use_mock_data
        
        if not all([self.client_id, self.client_secret, self.tenant_id]):
            print("Warning: Missing Microsoft Graph API credentials. Using mock data instead.")
            self.use_mock_data = True
        
    def get_token(self):
        """Get Microsoft Graph API access token."""
        if self.token and self.token_expiry > datetime.now():
            return self.token
            
        app = msal.ConfidentialClientApplication(
            self.client_id,
            authority=self.authority,
            client_credential=self.client_secret
        )
        
        result = app.acquire_token_for_client(scopes=self.scope)
        
        if "access_token" in result:
            self.token = result["access_token"]
            self.token_expiry = datetime.now() + timedelta(seconds=result.get("expires_in", 3600))
            return self.token
        else:
            error_description = result.get("error_description", "Unknown error")
            raise Exception(f"Failed to acquire token: {error_description}")
    
    def make_request(self, method, endpoint, data=None, params=None):
        """Make a request to Microsoft Graph API."""
        headers = {
            "Authorization": f"Bearer {self.get_token()}",
            "Content-Type": "application/json"
        }
        
        url = f"{self.endpoint}/{endpoint}"
        
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            json=data,
            params=params
        )
        
        if response.status_code >= 400:
            raise Exception(f"Microsoft Graph API error: {response.status_code} - {response.text}")
        
        return response.json() if response.content else {}
    def get_emails(self, top=10, filter_criteria=None):
        """Get recent emails."""
        if self.use_mock_data:
            print("Using mock email data")
            return MockMSGraphData.get_email_data()
            
        try:
            params = {
                "$top": top,
                "$orderby": "receivedDateTime DESC"
            }
            
            if filter_criteria:
                params["$filter"] = filter_criteria
                
            return self.make_request("GET", "me/messages", params=params)
        except Exception as e:
            print(f"Error fetching emails: {str(e)}. Using mock data instead.")
            return MockMSGraphData.get_email_data()
    def get_calendar_events(self, start_time=None, end_time=None, top=10):
        """Get calendar events."""
        if self.use_mock_data:
            print("Using mock calendar data")
            return MockMSGraphData.get_calendar_data()
            
        try:
            if not start_time:
                start_time = datetime.now().strftime("%Y-%m-%dT00:00:00Z")
            if not end_time:
                end_time = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%dT23:59:59Z")
                
            params = {
                "$top": top,
                "$orderby": "start/dateTime ASC",
                "$filter": f"start/dateTime ge '{start_time}' and end/dateTime le '{end_time}'"
            }
            
            return self.make_request("GET", "me/calendar/events", params=params)
        except Exception as e:
            print(f"Error fetching calendar events: {str(e)}. Using mock data instead.")
            return MockMSGraphData.get_calendar_data()
            
    def get_teams_chats(self, top=20):
        """Get recent Teams chat messages."""
        if self.use_mock_data:
            print("Using mock Teams data")
            return MockMSGraphData.get_teams_data()
            
        try:
            chats = self.make_request("GET", "me/chats", params={"$top": top})
            
            all_messages = {"value": []}
            
            for chat in chats.get("value", []):
                chat_id = chat.get("id")
                if chat_id:
                    messages = self.make_request(
                        "GET", 
                        f"me/chats/{chat_id}/messages", 
                        params={"$top": 10}  
                    )
                    
                    for message in messages.get("value", []):
                        message["chatName"] = chat.get("topic", "Unnamed chat")
                        all_messages["value"].append(message)
            return all_messages
        except Exception as e:
            print(f"Error getting Teams messages: {str(e)}. Using mock data instead.")
            return MockMSGraphData.get_teams_data()
