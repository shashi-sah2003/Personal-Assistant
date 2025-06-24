from datetime import datetime, timedelta, timezone
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class SlackClient:
    def __init__(self, bot_token):
        self.client = WebClient(token=bot_token)
        self.user_cache = {}

    def get_user_name(self, user_id):
        if user_id in self.user_cache:
            return self.user_cache[user_id]
        try:
            user_info = self.client.users_info(user=user_id)
            name = user_info['user']['real_name'] or user_info['user']['name']
            self.user_cache[user_id] = name
            return name
        except Exception:
            return user_id

    def get_todays_messages(self, max_channels=5, max_messages=200):
        today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        oldest = today.timestamp()
        latest = (today + timedelta(days=1)).timestamp()
        messages_summary = []

        try:
            all_channels = self.client.conversations_list(types="public_channel,private_channel")['channels']
            joined_channels = [ch for ch in all_channels if ch.get('is_member', False)][:max_channels]
            for channel in joined_channels:
                channel_id = channel['id']
                channel_name = channel['name']
                result = self.client.conversations_history(
                    channel=channel_id,
                    oldest=oldest,
                    latest=latest,
                    limit=max_messages
                )
                for msg in result['messages']:
                    user_id = msg.get('user', 'unknown')
                    user_name = self.get_user_name(user_id) if user_id != 'unknown' else 'unknown'
                    text = msg.get('text', '')
                    ts = float(msg['ts'])
                    msg_time = datetime.fromtimestamp(ts, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
                    if 'has joined the channel' in text or 'has left the channel' in text:
                        continue
                    messages_summary.append({
                        'channel': channel_name,
                        'user': user_name,
                        'text': text,
                        'time': msg_time
                    })
        except SlackApiError as e:
            print(f"Error fetching messages: {e.response['error']}")
        return messages_summary
