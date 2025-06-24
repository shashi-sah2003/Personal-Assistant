import os
from dotenv import load_dotenv
from jira import JIRA
from datetime import datetime, timedelta

load_dotenv()

class JiraClient:
    def __init__(self):
        """
        Initialize the JIRA Client
        """
        self.jira_url = os.getenv("JIRA_URL")
        self.jira_username = os.getenv("JIRA_USERNAME")
        self.jira_api_token = os.getenv("JIRA_API_TOKEN")
        
        if not all([self.jira_url, self.jira_username, self.jira_api_token]):
            print("Warning: Missing JIRA API credentials. Using mock data instead.")
            self.client = None
        else:
            self.client = self._authenticate()
            
    def _authenticate(self):
        """Authenticate with JIRA."""
        try:
            return JIRA(
                server=self.jira_url,
                basic_auth=(self.jira_username, self.jira_api_token)
            )
        except Exception as e:
            print(f"Failed to authenticate with JIRA: {str(e)}")
            return None
            
    def get_assigned_issues(self, days_back=7):
        """Get assigned JIRA issues."""
        try:
            since_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
            jql = f'assignee = currentUser() AND updated >= "{since_date}" ORDER BY updated DESC'
            
            issues = self.client.search_issues(jql, maxResults=50)
            return issues
        except Exception as e:
            print(f"Error fetching JIRA issues: {str(e)}. Using mock data instead.")
        

    def get_created_issues(self, days_back=7):
        """Get issues created by the user."""
            
        try:
            since_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
            jql = f'reporter = currentUser() AND created >= "{since_date}" ORDER BY created DESC'
            
            issues = self.client.search_issues(jql, maxResults=50)
            return issues
        except Exception as e:
            print(f"Error fetching created JIRA issues: {str(e)}. Using mock data instead.")
    
    def get_updated_issues(self, days_back=1):
        """Get issues updated recently that the user is watching or involved in."""
        
        try:
            since_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
            jql = f'(watcher = currentUser() OR assignee = currentUser() OR reporter = currentUser()) AND updated >= "{since_date}" ORDER BY updated DESC'
            
            issues = self.client.search_issues(jql, maxResults=50)
            return issues
        except Exception as e:
            print(f"Error fetching updated JIRA issues: {str(e)}. Using mock data instead.")
            
    def get_issue_details(self, issue_key):
        """Get detailed information about a specific issue."""
        try:
            issue = self.client.issue(issue_key)
            return issue
        except Exception as e:
            print(f"Error fetching issue details: {str(e)}. Using mock data instead.")
