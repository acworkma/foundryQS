# Agent Usage Guide

This project demonstrates two patterns for creating and using Azure AI Foundry agents using the NEW Foundry Agent API.

## Agent Creation Patterns

### Pattern 1: Environment-Driven (agent.py)

**Configuration via environment variables:**

```python
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import Agent
from azure.identity import DefaultAzureCredential
import os

# Load configuration from environment
endpoint = os.getenv("PROJECT_ENDPOINT")
agent_name = os.getenv("AGENT_NAME") 
model_deployment_name = os.getenv("MODEL_DEPLOYMENT_NAME")

# Create project client
project = AIProjectClient(
    endpoint=endpoint,
    credential=DefaultAzureCredential()
)

# Create NEW Foundry agent
agent = project.agents.create_agent(
    model=model_deployment_name,
    name=agent_name,
    instructions="You are a helpful assistant."
)
```

### Pattern 2: Direct Configuration (main.py)

**Hardcoded configuration for specific use cases:**

```python
# Direct endpoint and model specification
project = AIProjectClient(
    endpoint="https://foundry-acw.services.ai.azure.com/api/projects/proj-acw",
    credential=DefaultAzureCredential()
)

# Create specialized agent
agent = project.agents.create_agent(
    model="DeepSeek-V3.2",
    name="storytelling-agent", 
    instructions="You are a creative storytelling agent. Generate one-line stories."
)
```

## Agent Interaction Workflow

### Step 1: Create Agent
```python
agent = project.agents.create_agent(
    model=model_deployment_name,
    name=agent_name,
    instructions="Your agent instructions here"
)
```

### Step 2: Get OpenAI Client
```python
# Get project's OpenAI client
openai_client = project.inference.get_openai_client()
```

### Step 3: Create Conversation
```python
# Create conversation context
conversation = openai_client.beta.threads.create()
```

### Step 4: Send Messages
```python
# Add user message
message = openai_client.beta.threads.messages.create(
    thread_id=conversation.id,
    role="user",
    content="Your question here"
)

# Use NEW Responses API with agent reference
response = openai_client.beta.threads.runs.create_and_poll(
    thread_id=conversation.id,
    assistant_id=agent.id,
    # This is the key difference - agent reference
    agent_reference={"type": "agent", "id": agent.id}
)
```

### Step 5: Get Response
```python
# Retrieve assistant's response
messages = openai_client.beta.threads.messages.list(
    thread_id=conversation.id
)
```

## Key Features

### NEW Foundry Agent Integration
- **Portal visibility:** Agents appear in Microsoft Foundry portal
- **Agent references:** Use `agent_reference` in Responses API calls
- **Model deployment:** Agents use deployed models, not direct API access

### Environment Variable Support
Configure via `.env` file:
```bash
PROJECT_ENDPOINT=https://your-project.services.ai.azure.com/api/projects/your-project
AGENT_NAME=your-agent-name
MODEL_DEPLOYMENT_NAME=your-model-deployment
```

### Authentication
Uses `DefaultAzureCredential` - automatically detects:
- Azure CLI credentials
- Managed Identity (in Azure)
- Service Principal environment variables

## Agent Instructions

Customize agent behavior through the `instructions` parameter:

```python
# General assistant
instructions="You are a helpful assistant."

# Specialized agent
instructions="You are a creative storytelling agent. Generate one-line stories based on user input."

# Domain expert
instructions="You are a Python programming expert. Provide clear, concise code examples and explanations."
```

## Portal Integration

After creation, agents are available in:
1. **Azure AI Foundry portal**
2. **Project dashboard**
3. **Agent management interface**

Agents created via this API integrate seamlessly with the Foundry platform ecosystem.