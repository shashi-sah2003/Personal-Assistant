import os
import sys
from typing import Dict, Any, TypedDict, Optional
from langgraph.graph import StateGraph, END, START
from src.agents.email_agent.agent import EmailAgent
from src.agents.calendar_agent.agent import CalendarAgent
from src.agents.teams_agent.agent import TeamsAgent
from src.agents.jira_agent.agent import JiraAgent
from src.helpers.llm_client import GeminiClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class AgentState(TypedDict):
    email_data: Optional[Dict]
    calendar_data: Optional[Dict]
    teams_data: Optional[Dict]
    jira_data: Optional[Dict]
    final_summary: Optional[str]
    error: Optional[str]
    use_mock_data: Optional[bool]

def create_personal_assistant_workflow(use_mock_data=False):
    """Create the langgraph workflow for the personal assistant
    
    Args:
        use_mock_data (bool): Whether to use mock data instead of real API calls
    """
    
    workflow = StateGraph(AgentState)
    
    # Define the nodes for the workflow
      # Email Agent Node
    def email_agent(state: AgentState) -> AgentState:
        try:
            use_mock = state.get("use_mock_data", False)
            email_agent = EmailAgent(use_mock_data=use_mock)
            email_data = email_agent.run(top=20, days=1)
            return {"email_data": email_data}
        except Exception as e:
            return {"error": f"Error in email agent: {str(e)}"}
        
      # Calendar Agent Node
    def calendar_agent(state: AgentState) -> AgentState:
        try:
            use_mock = state.get("use_mock_data", False)
            calendar_agent = CalendarAgent(use_mock_data=use_mock)
            calendar_data = calendar_agent.run(days_ahead=2)
            return {"calendar_data": calendar_data}
        except Exception as e:
            return {"error": f"Error in calendar agent: {str(e)}"}
        
      # Teams Agent Node
    def teams_agent(state: AgentState) -> AgentState:
        try:
            use_mock = state.get("use_mock_data", False)
            teams_agent = TeamsAgent(use_mock_data=use_mock)
            teams_data = teams_agent.run(top=20)
            return {"teams_data": teams_data}
        except Exception as e:
            return {"error": f"Error in teams agent: {str(e)}"}
        
      # JIRA Agent Node
    def jira_agent(state: AgentState) -> AgentState:
        try:
            use_mock = state.get("use_mock_data", False)
            jira_agent = JiraAgent(use_mock_data=use_mock)
            jira_data = jira_agent.run(days_back=7)
            return {"jira_data": jira_data}
        except Exception as e:
            return {"error": f"Error in JIRA agent: {str(e)}"}
    
    # Summary Agent Node
    def summary_agent(state: AgentState) -> AgentState:
        try:
            llm_client = GeminiClient()
            
            email_summary = state.get("email_data", {}).get("summary", "No email data available.")
            calendar_summary = state.get("calendar_data", {}).get("summary", "No calendar data available.")
            jira_summary = state.get("jira_data", {}).get("summary", "No JIRA data available.")
            teams_summary = state.get("teams_data", {}).get("summary", "No Teams data available.")
            
            # Create a comprehensive daily summary
            final_summary = llm_client.create_daily_summary(
                email_summary=email_summary,
                meetings_summary=calendar_summary,
                jira_summary=jira_summary,
                teams_summary=teams_summary
            )
            
            return {"final_summary": final_summary}
        except Exception as e:
            return {"error": f"Error in summary agent: {str(e)}"}
    
    # Add nodes to the workflow
    workflow.add_node("email_agent", email_agent)
    workflow.add_node("calendar_agent", calendar_agent)
    workflow.add_node("teams_agent", teams_agent)
    workflow.add_node("jira_agent", jira_agent)
    workflow.add_node("summary_agent", summary_agent)
    
    workflow.add_edge("email_agent", "summary_agent")
    workflow.add_edge("calendar_agent", "summary_agent")
    workflow.add_edge("teams_agent", "summary_agent")
    workflow.add_edge("jira_agent", "summary_agent")
    workflow.add_edge("summary_agent", END)

    workflow.add_edge(START, "email_agent")
    workflow.add_edge(START, "calendar_agent")
    workflow.add_edge(START, "teams_agent")
    workflow.add_edge(START, "jira_agent")
    
    return workflow.compile()

def run_personal_assistant(use_mock_data=False) -> Dict[str, Any]:
    """Run the personal assistant workflow and return the results
    
    Args:
        use_mock_data (bool): Whether to use mock data instead of real API calls
    """
    
    executor = create_personal_assistant_workflow(use_mock_data)
    
    # Define the initial state
    initial_state = {
        "email_data": None,
        "calendar_data": None,
        "teams_data": None,
        "jira_data": None,
        "final_summary": None,
        "error": None,
        "use_mock_data": use_mock_data
    }
    
    # Execute the workflow
    print("Starting personal assistant workflow...")
    result = executor.invoke(initial_state)
    
    return {
        "email_summary": result.get("email_data", {}).get("summary", "No email data available."),
        "calendar_summary": result.get("calendar_data", {}).get("summary", "No calendar data available."),
        "jira_summary": result.get("jira_data", {}).get("summary", "No JIRA data available."),
        "teams_summary": result.get("teams_data", {}).get("summary", "No Teams data available."),
        "final_summary": result.get("final_summary", "No summary available."),
        "error": result.get("error")
    }
