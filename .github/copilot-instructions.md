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