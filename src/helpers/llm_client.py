import os
import google.generativeai as genai
from dotenv import load_dotenv
from langfuse import observe

load_dotenv()


class GeminiClient:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        
    def analyze_text(self, text, prompt_template=None):
        """
        Analyze text using Gemini model
        
        Args:
            text (str): Text to analyze
            prompt_template (str, optional): Custom prompt template to use
        
        Returns:
            str: Generated response from the model
        """
        try:
            if prompt_template:
                prompt = prompt_template.format(text=text)
            else:
                prompt = text
                
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error in analyzing text: {str(e)}")
            return f"Error analyzing text: {str(e)}"
    
    @observe(name="email_summary")
    def summarize_emails(self, emails):
        """
        Summarize emails
        
        Args:
            emails (list): List of email details
        
        Returns:
            str: Summary of emails
        """
        prompt = """
        Analyze the following emails and provide:
        1. A concise summary of key points from each important email
        2. Identify any action items or tasks that need to be addressed
        3. Categorize emails by priority (High, Medium, Low)
        4. Note any deadline-sensitive items
        
        Emails:
        {text}
        
        Format your response as:
        
        ## Email Summary
        
        ### High Priority
        - [Item 1] - Brief summary with action required
        - [Item 2] - Brief summary with action required
        
        ### Medium Priority
        - [Item 1] - Brief summary
        
        ### Low Priority
        - [Item X] - Brief summary
        
        ## Action Items
        1. [Action 1] - Deadline (if applicable)
        2. [Action 2]
        """
        
        emails_text = "\n\n".join([
            f"From: {email.get('from', 'Unknown')}\n"
            f"Subject: {email.get('subject', 'No Subject')}\n"
            f"Date: {email.get('date', 'Unknown')}\n"
            f"Snippet: {email.get('snippet', '')}\n"
            f"Body: {email.get('body', 'No body available')}\n"
            for email in emails if email
        ])
        
        return self.analyze_text(emails_text, prompt)

    @observe(name="meeting_summary")
    def summarize_meetings(self, events):
        """
        Summarize calendar events
        
        Args:
            events (list): List of calendar events
        
        Returns:
            str: Summary of events
        """
        prompt = """
        Analyze the following calendar events and provide:
        1. A timeline of upcoming meetings for today and tomorrow
        2. Note any preparation needed for meetings
        3. Highlight conflicts or back-to-back meetings
        
        Calendar Events:
        {text}
        
        Format your response as:
        
        ## Meeting Schedule
        
        ### Today
        - [Time] [Meeting Title] - [Location/Slack/Zoom]
          Brief description, attendees, preparation needed
        
        ### Tomorrow
        - [Time] [Meeting Title] - [Location/Slack/Zoom]
          Brief description, attendees, preparation needed
        
        ## Preparation Required
        1. [Meeting Name] - [Preparation Item]
        2. [Meeting Name] - [Preparation Item]
        """
        
        events_text = "\n\n".join([
            f"Title: {event.get('summary', 'No Title')}\n"
            f"Start: {event.get('start', 'Unknown')}\n"
            f"End: {event.get('end', 'Unknown')}\n"
            f"Location: {event.get('location', 'No location')}\n"
            f"Hangout Link: {event.get('hangoutLink', '')}\n"
            f"Organizer: {event.get('organizer', 'Unknown')}\n"
            f"Attendees: {', '.join(event.get('attendees', []))}\n"
            f"Description: {event.get('description', '')}\n"
            f"Status: {event.get('status', 'Unknown')}\n"
            for event in events if event
        ])
        
        return self.analyze_text(events_text, prompt)

    @observe(name="jira_summary")
    def summarize_jira_tickets(self, jira_issues):
        """
        Summarize JIRA tickets
        
        Args:
            jira_issues: List of JIRA issue objects
        
        Returns:
            str: Summary of JIRA tickets
        """
        prompt = """
        Analyze the following JIRA tickets and provide:
        1. A summary of tickets assigned to the user by priority
        2. Upcoming deadlines or due dates
        3. Status updates on tickets
        
        JIRA Tickets:
        {text}
        
        Format your response as:
        
        ## JIRA Tickets
        
        ### High Priority
        - [Ticket-123] [Title] - Due: [Date], Status: [Status]
          Brief summary of the ticket and what needs to be done
        
        ### Medium Priority
        - [Ticket-456] [Title] - Due: [Date], Status: [Status]
          Brief summary
        
        ### Low Priority
        - [Ticket-789] [Title] - Due: [Date], Status: [Status]
          Brief summary
        
        ## Upcoming Deadlines
        1. [Ticket-123] - Due in [X] days
        2. [Ticket-456] - Due in [Y] days
        """
        
        issues_text = ""
        for issue in jira_issues:
            issues_text += f"Key: {issue.key}\n"
            issues_text += f"Summary: {issue.fields.summary}\n"
            issues_text += f"Status: {issue.fields.status.name}\n"
            issues_text += f"Priority: {issue.fields.priority.name if hasattr(issue.fields, 'priority') and issue.fields.priority else 'Not set'}\n"
            issues_text += f"Assignee: {issue.fields.assignee.displayName if issue.fields.assignee else 'Unassigned'}\n"
            issues_text += f"Due Date: {issue.fields.duedate if hasattr(issue.fields, 'duedate') and issue.fields.duedate else 'Not set'}\n"
            issues_text += f"Description: {issue.fields.description if issue.fields.description else 'No description'}\n\n"
        
        return self.analyze_text(issues_text, prompt)


    @observe(name="slack_summary")
    def summarize_Slack_messages(self, messages):
        """
        Summarize Slack messages
        
        Args:
            messages (list): List of Slack message details
        
        Returns:
            str: Summary of Slack messages
        """
        prompt = """
        Analyze the following Microsoft Slack messages and provide:
        1. A summary of important conversations
        2. Any action items or requests directed at the user
        3. Unanswered questions or pending replies
        
        Slack Messages:
        {text}
        
        Format your response as:
        
        ## Slack Messages Summary
        
        ### Important Conversations
        - [Chat Name/Person] - Brief summary of important discussion
        
        ### Action Items
        1. [Person] requested: [Action requested]
        2. [Person] asked about: [Question that needs a response]
        
        ### Follow-ups Required
        1. Respond to [Person] about [Topic]
        """
        
        messages_text = "\n\n".join([
            f"Channel: {msg.get('channel', 'Unknown')}\n"
            f"User: {msg.get('user', 'Unknown')}\n"
            f"Time: {msg.get('time', 'Unknown')}\n"
            f"Message: {msg.get('text', '')}"
            for msg in messages if msg
        ])
        
        return self.analyze_text(messages_text, prompt)

    @observe(name="daily_summary")
    def create_daily_summary(self, email_summary, meetings_summary, jira_summary, slack_summary):
        """
        Create a comprehensive daily summary from all sources
        
        Args:
            email_summary (str): Summary of emails
            meetings_summary (str): Summary of calendar events
            jira_summary (str): Summary of JIRA tickets
            slack_summary (str): Summary of Slack messages
        
        Returns:
            str: Comprehensive daily summary with action items
        """
        prompt = """
        Create a comprehensive daily summary based on the following information from different sources:
        
        ## Email Summary:
        {email_summary}
        
        ## Meeting Schedule:
        {meetings_summary}
        
        ## JIRA Tickets:
        {jira_summary}
        
        ## Slack Messages:
        {slack_summary}
        
        Please create a well-organized daily briefing with:
        1. An executive summary of the most important items across all platforms
        2. A consolidated list of all action items, sorted by priority
        3. A timeline for today and tomorrow with all meetings and deadlines
        4. Areas requiring immediate attention
        
        Format your response as a professional daily briefing.
        """
        
        return self.analyze_text(
            "",
            prompt.format(
                email_summary=email_summary,
                meetings_summary=meetings_summary,
                jira_summary=jira_summary,
                slack_summary=slack_summary
            )
        )
