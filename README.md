# Personal Assistant

An AI-powered personal assistant that integrates with multiple workplace services to provide daily summaries, task management, and automated workflows. The assistant helps streamline your productivity by aggregating information from Gmail, Google Calendar, Jira, and Slack.


## 🏗️ Architecture

## System Diagrams

![Personal Assistant - Summarizer Architecture](src/assets/summarizer_todolist_agent.png)

*Figure: High-level architecture of the Personal Assistant - Summarizer system.*

![Personal Assistant Orchestrator Agent Architecture](src/assets/orchestrator%20agent.png)

*Figure: Flowchart diagram showing the architecture of the Personal Assistant Orchestrator Agent. The diagram starts with a User Query, which is processed by an LLM labeled gpt-4o-mini. The Tool Selector chooses relevant tools, and the Agent Orchestrator coordinates actions. The flow splits into two paths: one for LLM Response leading to Final Response, and another for LLM Task Planning, which routes tasks to various tools including Jira Tool, Calendar Tool, Gmail Tool, and Slack Tool via APIs. Results from these tools are collected and sent back to the Agent Orchestrator and Final Response.*


## 🛠️ Technologies Used

- **Python 3.8+**
- **FastAPI** - Web framework for API endpoints
- **LangChain & LangGraph** - AI workflow orchestration
- **Google Gemini AI** - Language model for intelligent summaries
- **Google APIs** - Gmail and Calendar integration
- **Atlassian API** - Jira integration
- **Slack SDK** - Slack integration
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation

## 📋 Prerequisites

Before you begin, ensure you have:

1. **Python 3.8 or higher** installed
2. **Google Cloud Project** with Gmail and Calendar APIs enabled
3. **Jira Cloud instance** with API access
4. **Slack workspace** with bot permissions
5. **Google Gemini API key**
6. **Azure OpenAI key**

## 🔧 Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Personal-Assistant
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install the package in development mode**:
   ```bash
   pip install -e .
   ```

## ⚙️ Configuration

1. **Create a `.env` file** in the project root with the following variables:

```env
# Google Gemini AI
GEMINI_API_KEY=your_gemini_api_key

# Jira Configuration
JIRA_URL=https://your-domain.atlassian.net/
JIRA_USERNAME=your_email@domain.com
JIRA_API_TOKEN=your_jira_api_token

# User Configuration
USER_ID=your_email@domain.com

# Langfuse (Optional - for LLM observability)
LANGFUSE_PUBLIC_KEY=your_langfuse_public_key
LANGFUSE_SECRET_KEY=your_langfuse_secret_key
LANGFUSE_HOST=https://cloud.langfuse.com

# Slack Configuration
SLACK_BOT_TOKEN=xoxb-your-slack-bot-token
SLACK_USER_TOKEN=xoxb-your-slack-user-token

# Azure OpenAI (Alternative to Gemini)
AZURE_OPENAI_API_KEY=your_azure_openai_key
AZURE_OPENAI_ENDPOINT=your_azure_endpoint
AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name
AZURE_OPENAI_API_VERSION=2024-12-01-preview
```

2. **Set up Google Cloud credentials**:
   - Download your Google Cloud service account JSON file
   - Place it in your project directory at src/config/credentials.json


## 🚀 Usage

### Running the API Server

Start the FastAPI server:

```bash
uvicorn main:app --port 8000
```

The API will be available at `http://localhost:8000`


### Automated Daily Summaries

The system automatically generates daily summaries by:

1. Collecting data from all integrated services
2. Processing information through AI agents
3. Generating comprehensive summaries using Gemini AI
4. Saving results to daily summary files

