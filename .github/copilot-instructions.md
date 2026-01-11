# GitHub Copilot Instructions

## Project Context
This is an Azure AI Foundry project for creating agents using the NEW Foundry Agent API. The project demonstrates how to create multiple agents with different language models.


### Dependencies and Installation
- Use `azure-ai-projects>=2.0.0b3` (beta version - **requires --pre flag**)
- Always use `uv` package manager for dependency management
- Install beta versions with: `uv add azure-ai-projects --pre`
- Load environment variables with `python-dotenv` and `load_dotenv()`

### Authentication
- Use `DefaultAzureCredential` for Azure authentication
- Requires `PROJECT_ENDPOINT` environment variable
- No API keys needed - uses Azure identity

### NEW Microsoft Foundry SDK Patterns (CRITICAL)
- **ALWAYS use NEW Foundry patterns** - NOT classic OpenAI assistant patterns
- Use `AIProjectClient` from `azure-ai-projects>=2.0.0b3` 
- Get OpenAI client with `project.get_openai_client()` - NOT direct OpenAI client
- Use `openai_client.responses.create()` - NOT `chat.completions.create()`
- Use NEW Foundry Agent Service - NOT classic assistants API

### Correct NEW Foundry Patterns
```python
# Correct project setup
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition
project = AIProjectClient(endpoint=os.environ["PROJECT_ENDPOINT"], credential=DefaultAzureCredential())

# Correct agent creation
agent = project.agents.create_version(
    agent_name=AGENT_NAME,
    definition=PromptAgentDefinition(
        model=MODEL_DEPLOYMENT_NAME,
        instructions="You are a storytelling agent. You craft engaging one-line stories based on user prompts and context.",
    ),
)

# Correct OpenAI client (from project)
openai_client = project.get_openai_client()

# Correct API calls - use responses.create()
response = openai_client.responses.create(
    conversation=conversation.id,
    extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
    input="Your prompt here"
)
```

### AVOID These Classic Patterns
- Do NOT use direct `from openai import OpenAI`
- Do NOT use `client.chat.completions.create()`
- Do NOT use `client.beta.assistants.create()`
- Do NOT use classic OpenAI assistant workflows
- Do NOT use `openai_client.beta.threads.runs.create()`


## File Naming Conventions
- Agent files: `agent-{model}.py` (e.g., `agent-deepseek.py`, `agent-gpt.py`)
- Agent names should match file names (e.g., "agent-mistral")
- Use hardcoded model deployment names in each agent file
- Environment configuration: `.env` file (excluded from git)

## Model-Specific Configurations
- **DeepSeek**: `MODEL_DEPLOYMENT_NAME = "DeepSeek-V3.2"`
- **GPT**: `MODEL_DEPLOYMENT_NAME = "gpt-5.2"`
- **Mistral**: `MODEL_DEPLOYMENT_NAME = "Mistral-Large-3"`

## Environment Variables
Required in `.env` file:
- `PROJECT_ENDPOINT` - Azure AI Foundry project endpoint
- Optional: `AGENT_NAME`, `MODEL_DEPLOYMENT_NAME` (for environment-driven agents)

## Documentation Standards
- Update README.md for new agent patterns
- Update USAGE.md for new API examples
- Add troubleshooting steps for new issues
- Emphasize beta version requirements and --pre flag usage

## Important Notes
- **CRITICAL**: Always use NEW Foundry Agent API patterns, NOT classic OpenAI assistants
- Agents appear in Microsoft Foundry portal after creation
- Beta APIs may have breaking changes - always test thoroughly
- Use `uv sync` to install dependencies from lockfile