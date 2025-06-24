import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.integrations.jira_client import JiraClient
from src.helpers.llm_client import GeminiClient

class JiraAgent:
    def __init__(self):
        self.jira_client = JiraClient()
        self.llm_client = GeminiClient()
        
    def run(self, days_back=7):
        """
        Run JIRA agent to collect and analyze JIRA tickets
        
        Args:
            days_back (int): Number of days to look back for JIRA tickets
            
        Returns:
            dict: JIRA issues data and summary
        """
        try:
            print("🎫 JIRA Agent: Retrieving assigned tickets...")
            
            assigned_issues = self.jira_client.get_assigned_issues(days_back=days_back)
            
            created_issues = self.jira_client.get_created_issues(days_back=days_back)
            
            updated_issues = self.jira_client.get_updated_issues(days_back=days_back)
            
            all_issues = {}
            for issue in list(assigned_issues) + list(created_issues) + list(updated_issues):
                if issue.key not in all_issues:
                    all_issues[issue.key] = issue
            
            issues_list = list(all_issues.values())
            
            if not issues_list:
                return {"summary": "No recent JIRA activity found.", "issues": []}
            
            summary = self.llm_client.summarize_jira_tickets(issues_list)
            
            return {
                "summary": summary,
                "issues": issues_list
            }
        except Exception as e:
            error_msg = f"Error in JIRA Agent: {str(e)}"
            print(error_msg)
            return {"summary": error_msg, "issues": []}
