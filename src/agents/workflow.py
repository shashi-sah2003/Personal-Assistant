import os
import sys
from typing import Dict, Any, TypedDict, Optional
from langgraph.graph import StateGraph, END, START
from src.agents.email_agent.agent import EmailAgent
from src.agents.calendar_agent.agent import CalendarAgent
from src.agents.slack_agent.agent import SlackAgent
from src.agents.jira_agent.agent import JiraAgent
from src.helpers.llm_client import GeminiClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class AgentState(TypedDict):
    email_data: Optional[Dict]
    calendar_data: Optional[Dict]
    slack_data: Optional[Dict]
    jira_data: Optional[Dict]
    todo_list: Optional[str]
    error: Optional[str]

def create_personal_assistant_workflow():
    """Create the langgraph workflow for the personal assistant
    """
    
    workflow = StateGraph(AgentState)
    
    # Define the nodes for the workflow
      # Email Agent Node
    def email_agent(state: AgentState) -> AgentState:
        try:
            email_agent = EmailAgent()
            email_data = email_agent.run()
            return {"email_data": email_data}
        except Exception as e:
            return {"email_error": f"Error in email agent: {str(e)}"}
        
      # Calendar Agent Node
    def calendar_agent(state: AgentState) -> AgentState:
        try:
            calendar_agent = CalendarAgent()
            calendar_data = calendar_agent.run(days_ahead=2)
            return {"calendar_data": calendar_data}
        except Exception as e:
            return {"calendar_error": f"Error in calendar agent: {str(e)}"}
        
      # Slack Agent Node
    def slack_agent(state: AgentState) -> AgentState:
        try:
            slack_agent = SlackAgent()
            slack_data = slack_agent.run(top=20)
            return {"slack_data": slack_data}
        except Exception as e:
            return {"slack_error": f"Error in slack agent: {str(e)}"}
        
      # JIRA Agent Node
    def jira_agent(state: AgentState) -> AgentState:
        try:
            jira_agent = JiraAgent()
            jira_data = jira_agent.run(days_back=7)
            return {"jira_data": jira_data}
        except Exception as e:
            return {"jira_error": f"Error in JIRA agent: {str(e)}"}
    
    # Summary Agent Node
    # def summary_agent(state: AgentState) -> AgentState:
    #     try:
    #         llm_client = GeminiClient()
            
    #         email_summary = state.get("email_data", {}).get("summary", "No email data available.")
    #         calendar_summary = state.get("calendar_data", {}).get("summary", "No calendar data available.")
    #         jira_summary = state.get("jira_data", {}).get("summary", "No JIRA data available.")
    #         slack_summary = state.get("slack_data", {}).get("summary", "No Slack data available.")
            
    #         # Create a comprehensive daily summary
    #         final_summary = llm_client.create_daily_summary(
    #             email_summary=email_summary,
    #             meetings_summary=calendar_summary,
    #             jira_summary=jira_summary,
    #             slack_summary=slack_summary
    #         )
            
    #         return {"final_summary": final_summary}
    #     except Exception as e:
    #         return {"error": f"Error in summary agent: {str(e)}"}

    def summary_agent(state: AgentState) -> AgentState:
        try:
            llm_client = GeminiClient()
            email_summary = state.get("email_data", {}).get("summary", "No email data available.")
            calendar_summary = state.get("calendar_data", {}).get("summary", "No calendar data available.")
            jira_summary = state.get("jira_data", {}).get("summary", "No JIRA data available.")
            slack_summary = state.get("slack_data", {}).get("summary", "No Slack data available.")

            # Use the new todo list method
            todo_list = llm_client.create_todo_list(
                email_summary=email_summary,
                meetings_summary=calendar_summary,
                jira_summary=jira_summary,
                slack_summary=slack_summary
            )
            return {"todo_list": todo_list}
        except Exception as e:
            return {"error": f"Error in summary agent: {str(e)}"}
    
    # Add nodes to the workflow
    workflow.add_node("email_agent", email_agent)
    workflow.add_node("calendar_agent", calendar_agent)
    workflow.add_node("slack_agent", slack_agent)
    workflow.add_node("jira_agent", jira_agent)
    workflow.add_node("summary_agent", summary_agent)
    
    workflow.add_edge("email_agent", "summary_agent")
    workflow.add_edge("calendar_agent", "summary_agent")
    workflow.add_edge("slack_agent", "summary_agent")
    workflow.add_edge("jira_agent", "summary_agent")
    workflow.add_edge("summary_agent", END)

    workflow.add_edge(START, "email_agent")
    workflow.add_edge(START, "calendar_agent")
    workflow.add_edge(START, "slack_agent")
    workflow.add_edge(START, "jira_agent")
    
    return workflow.compile()

def run_personal_assistant() -> Dict[str, Any]:
    """Run the personal assistant workflow and return the results
    """
    
    executor = create_personal_assistant_workflow()
    
    # Define the initial state
    initial_state = {
        "email_data": None,
        "calendar_data": None,
        "slack_data": None,
        "jira_data": None,
        "todo_list": None,
        "error": None,
    }
    
    # Execute the workflow
    print("Starting personal assistant workflow...")
    result = executor.invoke(initial_state)
    
    return {
        "email_summary": result.get("email_data", {}).get("summary", "No email data available."),
        "calendar_summary": result.get("calendar_data", {}).get("summary", "No calendar data available."),
        "jira_summary": result.get("jira_data", {}).get("summary", "No JIRA data available."),
        "slack_summary": result.get("slack_data", {}).get("summary", "No Slack data available."),
        "todo_list": result.get("todo_list", []),
        "error": result.get("error")
    }
