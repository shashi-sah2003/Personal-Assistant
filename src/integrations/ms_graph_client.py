import os
import asyncio
from dotenv import load_dotenv
from datetime import datetime, timedelta
from azure.identity import ClientSecretCredential
from msgraph import GraphServiceClient
from src.helpers.mock_data import MockMSGraphData
from msgraph.generated.users.item.messages.messages_request_builder import MessagesRequestBuilder
from msgraph.generated.users.item.calendar.calendar_view.calendar_view_request_builder import CalendarViewRequestBuilder
from msgraph.generated.users.item.chats.chats_request_builder import ChatsRequestBuilder
from msgraph.generated.users.item.chats.item.messages.messages_request_builder import MessagesRequestBuilder as ChatMessagesRequestBuilder

load_dotenv()

class MSGraphClient:
    def __init__(self, use_mock_data=False):
        """
        Initialize the Microsoft Graph API Client using the Graph SDK
        """
        self.client_id = os.getenv("MS_CLIENT_ID")
        self.client_secret = os.getenv("MS_CLIENT_SECRET")
        self.tenant_id = os.getenv("MS_TENANT_ID")
        self.scopes = ["https://graph.microsoft.com/.default"]
        self.use_mock_data = use_mock_data
        self.client = None

        if not all([self.client_id, self.client_secret, self.tenant_id]):
            print("Warning: Missing Microsoft Graph API credentials. Using mock data instead.")
            self.use_mock_data = True
        else:
            credential = ClientSecretCredential(
                tenant_id=self.tenant_id,
                client_id=self.client_id,
                client_secret=self.client_secret
            )
            self.client = GraphServiceClient(credentials=credential, scopes=self.scopes)

    async def _run_graph_request(self, request_coroutine):
        """Helper method to run async Graph API requests"""
        if self.use_mock_data:
            return None
        try:
            return await request_coroutine
        except Exception as e:
            print(f"Graph API request failed: {str(e)}")
            return None

    def get_emails(self, user_id=os.getenv("USER_ID"), top=10, filter_criteria=None):
        """Get recent emails using Graph SDK."""
        if self.use_mock_data:
            print("Using mock email data")
            return MockMSGraphData.get_email_data()

        try:
            builder = self.client.users.by_user_id(user_id).messages
            if filter_criteria:
                builder = builder.filter(filter_criteria)
            builder = builder.order_by("receivedDateTime desc").top(top)

            messages = asyncio.run(self._run_graph_request(builder.get()))
            if messages:
                return {"value": [msg.to_dict() for msg in messages.value]}
            return MockMSGraphData.get_email_data()
        except Exception as e:
            print(f"Error fetching emails: {str(e)}. Using mock data instead.")
            return MockMSGraphData.get_email_data()

    # async def get_emails(self, user_id=os.getenv("USER_ID"), top=10, filter_criteria=None):
    #     """Get emails with new SDK pattern"""
    #     if self.use_mock_data:
    #         return MockMSGraphData.get_email_data()

    #     try:
    #         # Build query parameters
    #         query_params = MessagesRequestBuilder.MessagesRequestBuilderGetQueryParameters(
    #             top=top,
    #             orderby=["receivedDateTime desc"],
    #             filter=filter_criteria
    #         )
    #         request_config = MessagesRequestBuilder.MessagesRequestBuilderGetRequestConfiguration(
    #             query_parameters=query_params
    #         )
            
    #         # Execute request
    #         messages = await self.client.users.by_user_id(user_id).messages.get(
    #             request_configuration=request_config
    #         )
    #         return {"value": [msg.to_dict() for msg in messages.value]}
    #     except Exception as e:
    #         print(f"Email error: {str(e)}")
    #         return MockMSGraphData.get_email_data()

    def get_calendar_events(self, user_id=os.getenv("USER_ID"), start_time=None, end_time=None, top=10):
        """Get calendar events using Graph SDK."""
        if self.use_mock_data:
            print("Using mock calendar data")
            return MockMSGraphData.get_calendar_data()

        try:
            if not start_time:
                start_time = datetime.utcnow().strftime("%Y-%m-%dT00:00:00Z")
            if not end_time:
                end_time = (datetime.utcnow() + timedelta(days=7)).strftime("%Y-%m-%dT23:59:59Z")

            filter_str = f"start/dateTime ge '{start_time}' and end/dateTime le '{end_time}'"
            builder = self.client.users.by_user_id(user_id).calendar.events
            builder = builder.filter(filter_str).order_by("start/dateTime").top(top)

            events = asyncio.run(self._run_graph_request(builder.get()))
            if events:
                return {"value": [event.to_dict() for event in events.value]}
            return MockMSGraphData.get_calendar_data()
        except Exception as e:
            print(f"Error fetching calendar events: {str(e)}. Using mock data instead.")
            return MockMSGraphData.get_calendar_data()

    # async def get_calendar_events(self, user_id=os.getenv("USER_ID"), start_time=None, end_time=None, top=10):
    #     """Get calendar events with calendarView endpoint"""
    #     if self.use_mock_data:
    #         return MockMSGraphData.get_calendar_data()

    #     try:
    #         # Build time range
    #         if not start_time:
    #             start_time = datetime.utcnow().strftime("%Y-%m-%dT00:00:00Z")
    #         if not end_time:
    #             end_time = (datetime.utcnow() + timedelta(days=7)).strftime("%Y-%m-%dT23:59:59Z")
            
    #         # Configure calendar view
    #         query_params = CalendarViewRequestBuilder.CalendarViewRequestBuilderGetQueryParameters(
    #             startDateTime=start_time,
    #             endDateTime=end_time,
    #             top=top,
    #             orderby=["start/dateTime"]
    #         )
    #         request_config = CalendarViewRequestBuilder.CalendarViewRequestBuilderGetRequestConfiguration(
    #             query_parameters=query_params
    #         )
            
    #         # Get calendar view
    #         events = await self.client.users.by_user_id(user_id).calendar.calendar_view.get(
    #             request_configuration=request_config
    #         )
    #         return {"value": [event.to_dict() for event in events.value]}
    #     except Exception as e:
    #         print(f"Calendar error: {str(e)}")
    #         return MockMSGraphData.get_calendar_data()

    def get_teams_chats(self, user_id=os.getenv("USER_ID"), top=20):
        """Get recent Teams chat messages using Graph SDK."""
        if self.use_mock_data:
            print("Using mock Teams data")
            return MockMSGraphData.get_teams_data()

        try:
            all_messages = {"value": []}
            chat_builder = self.client.users.by_user_id(user_id).chats.top(top)

            chats = asyncio.run(self._run_graph_request(chat_builder.get()))
            if not chats:
                return MockMSGraphData.get_teams_data()

            for chat in chats.value:
                messages_builder = (
                    self.client.users.by_user_id(user_id)
                        .chats.by_chat_id(chat.id)
                        .messages
                        .top(10)
                )
                messages = asyncio.run(self._run_graph_request(messages_builder.get()))
                if messages:
                    for message in messages.value:
                        msg_dict = message.to_dict()
                        msg_dict["chatName"] = chat.topic or "Unnamed chat"
                        all_messages["value"].append(msg_dict)

            return all_messages if all_messages["value"] else MockMSGraphData.get_teams_data()
        except Exception as e:
            print(f"Error getting Teams messages: {str(e)}. Using mock data instead.")
            return MockMSGraphData.get_teams_data()
    
    # async def get_teams_chats(self, user_id=os.getenv("USER_ID"), top=20):
    #     """Get Teams chats with new configuration pattern"""
    #     if self.use_mock_data:
    #         return MockMSGraphData.get_teams_data()

    #     try:
    #         all_messages = {"value": []}
            
    #         # Get chats with top parameter
    #         chat_query = ChatsRequestBuilder.ChatsRequestBuilderGetQueryParameters(top=top)
    #         chat_config = ChatsRequestBuilder.ChatsRequestBuilderGetRequestConfiguration(
    #             query_parameters=chat_query
    #         )
    #         chats = await self.client.users.by_user_id(user_id).chats.get(
    #             request_configuration=chat_config
    #         )
            
    #         if not chats.value:
    #             return MockMSGraphData.get_teams_data()
            
    #         # Get messages for each chat
    #         for chat in chats.value:
    #             msg_query = ChatMessagesRequestBuilder.MessagesRequestBuilderGetQueryParameters(top=10)
    #             msg_config = ChatMessagesRequestBuilder.MessagesRequestBuilderGetRequestConfiguration(
    #                 query_parameters=msg_query
    #             )
    #             messages = await self.client.users.by_user_id(user_id).chats.by_chat_id(chat.id).messages.get(
    #                 request_configuration=msg_config
    #             )
    #             if messages.value:
    #                 for message in messages.value:
    #                     msg_dict = message.to_dict()
    #                     msg_dict["chatName"] = chat.topic or "Unnamed chat"
    #                     all_messages["value"].append(msg_dict)
            
    #         return all_messages
    #     except Exception as e:
    #         print(f"Teams error: {str(e)}")
    #         return MockMSGraphData.get_teams_data()