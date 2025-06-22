import os
from dotenv import load_dotenv
from jira import JIRA
from datetime import datetime, timedelta
from src.helpers.mock_data import MockJiraData

load_dotenv()

class JiraClient:
    def __init__(self, use_mock_data=False):
        """
        Initialize the JIRA Client
        
        Args:
            use_mock_data (bool): If True, use mock data instead of real API calls
        """
        self.jira_url = os.getenv("JIRA_URL")
        self.jira_username = os.getenv("JIRA_USERNAME")
        self.jira_api_token = os.getenv("JIRA_API_TOKEN")
        self.use_mock_data = use_mock_data
        
        if not all([self.jira_url, self.jira_username, self.jira_api_token]):
            print("Warning: Missing JIRA API credentials. Using mock data instead.")
            self.use_mock_data = True
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
            self.use_mock_data = True
            return None
            
    def get_assigned_issues(self, days_back=7):
        """Get assigned JIRA issues."""
        if self.use_mock_data:
            print("Using mock JIRA data")
            return MockJiraData.get_mock_issues()
            
        try:
            since_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
            jql = f'assignee = currentUser() AND updated >= "{since_date}" ORDER BY updated DESC'
            
            issues = self.client.search_issues(jql, maxResults=50)
            return issues
        except Exception as e:
            print(f"Error fetching JIRA issues: {str(e)}. Using mock data instead.")
            return MockJiraData.get_mock_issues()
        

    def get_created_issues(self, days_back=7):
        """Get issues created by the user."""
        if self.use_mock_data:
            print("Using mock JIRA data")
            return MockJiraData.get_mock_issues()
            
        try:
            since_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
            jql = f'reporter = currentUser() AND created >= "{since_date}" ORDER BY created DESC'
            
            issues = self.client.search_issues(jql, maxResults=50)
            return issues
        except Exception as e:
            print(f"Error fetching created JIRA issues: {str(e)}. Using mock data instead.")
            return MockJiraData.get_mock_issues()
    
    def get_updated_issues(self, days_back=1):
        """Get issues updated recently that the user is watching or involved in."""
        if self.use_mock_data:
            print("Using mock JIRA data")
            return MockJiraData.get_mock_issues()
            
        try:
            since_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
            jql = f'(watcher = currentUser() OR assignee = currentUser() OR reporter = currentUser()) AND updated >= "{since_date}" ORDER BY updated DESC'
            
            issues = self.client.search_issues(jql, maxResults=50)
            return issues
        except Exception as e:
            print(f"Error fetching updated JIRA issues: {str(e)}. Using mock data instead.")
            return MockJiraData.get_mock_issues()
            
    def get_issue_details(self, issue_key):
        """Get detailed information about a specific issue."""
        if self.use_mock_data:
            print("Using mock JIRA data")
            return next((issue for issue in MockJiraData.get_mock_issues() if issue.key == issue_key), None)
            
        try:
            issue = self.client.issue(issue_key)
            return issue
        except Exception as e:
            print(f"Error fetching issue details: {str(e)}. Using mock data instead.")
            return next((issue for issue in MockJiraData.get_mock_issues() if issue.key == issue_key), None)
