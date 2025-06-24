import os.path
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/calendar.readonly'
]

class GoogleClient:
    def __init__(self):
        self.creds = None
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'src/config/credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())
        self.gmail_service = build('gmail', 'v1', credentials=self.creds)
        self.calendar_service = build('calendar', 'v3', credentials=self.creds)

    def get_todays_emails(self, max_results=20):
        """Fetch detailed emails received today."""
        today = datetime.now().date()
        after = today.strftime('%Y/%m/%d')
        before = (today + timedelta(days=1)).strftime('%Y/%m/%d')
        query = f'after:{after} before:{before}'
        results = self.gmail_service.users().messages().list(
            userId='me', q=query, maxResults=max_results
        ).execute()
        messages = results.get('messages', [])
        emails = []
        for msg in messages:
            msg_detail = self.gmail_service.users().messages().get(
                userId='me', id=msg['id'], format='full'
            ).execute()
            headers = {h['name']: h['value'] for h in msg_detail['payload']['headers']}
            body = ""
            payload = msg_detail.get('payload', {})
            if 'parts' in payload:
                for part in payload['parts']:
                    if part['mimeType'] == 'text/plain':
                        body = part['body'].get('data', '')
                        break
            elif payload.get('mimeType') == 'text/plain':
                body = payload['body'].get('data', '')
            if body:
                try:
                    body = base64.urlsafe_b64decode(body).decode('utf-8')
                except Exception:
                    pass
            emails.append({
                'id': msg['id'],
                'subject': headers.get('Subject', ''),
                'from': headers.get('From', ''),
                'date': headers.get('Date', ''),
                'snippet': msg_detail.get('snippet', ''),
                'body': body
            })
        return emails

    def get_todays_events(self):
        """Fetch detailed calendar events for today."""
        today = datetime.utcnow().date()
        start_of_day = datetime.combine(today, datetime.min.time()).isoformat() + 'Z'
        end_of_day = datetime.combine(today, datetime.max.time()).isoformat() + 'Z'
        events_result = self.calendar_service.events().list(
            calendarId='primary',
            timeMin=start_of_day,
            timeMax=end_of_day,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])
        detailed_events = []
        for event in events:
            detailed_events.append({
                'id': event.get('id'),
                'summary': event.get('summary', 'No Title'),
                'description': event.get('description', ''),
                'organizer': event.get('organizer', {}).get('email', ''),
                'start': event.get('start', {}).get('dateTime', event.get('start', {}).get('date')),
                'end': event.get('end', {}).get('dateTime', event.get('end', {}).get('date')),
                'attendees': [att.get('email') for att in event.get('attendees', [])] if event.get('attendees') else [],
                'location': event.get('location', ''),
                'status': event.get('status', ''),
                'hangoutLink': event.get('hangoutLink', ''),
            })
        return detailed_events

client = GoogleClient()