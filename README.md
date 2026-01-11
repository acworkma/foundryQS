# Azure AI Foundry Quickstart

A quickstart project for creating and managing AI agents using Microsoft Azure AI Foundry (NEW Foundry Agent API).

## Prerequisites

- **Python 3.12+** (specified in `.python-version`)
- **Azure CLI** installed and authenticated
- **Azure AI Foundry project** with proper permissions
- **Deployed model** accessible via deployment name

## Quick Setup

1. **Install dependencies using uv:**
   ```bash
   # Install beta versions (required for NEW Foundry Agent API)
   uv sync
   
   # Or manually add the beta dependency:
   uv add azure-ai-projects --pre
   ```

2. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your Azure AI Foundry project details
   ```

3. **Run an agent creation script:**
   ```bash
   # Create DeepSeek agent
   uv run python agent-deepseek.py
   
   # Create GPT agent  
   uv run python agent-gpt.py
   
   # Create Mistral agent
   uv run python agent-mistral.py
   ```

## Project Structure

- `agent-deepseek.py` - DeepSeek-V3.2 agent creation
- `agent-gpt.py` - GPT-5.2 agent creation  
- `agent-mistral.py` - Mistral Large 3 agent creation
- `agent.py` - Original agent creation script (environment-driven)
- `main.py` - Direct agent creation example (hardcoded config)
- `quickstart.py` - Basic placeholder script
- `pyproject.toml` - Project dependencies and configuration
- `uv.lock` - Locked dependency versions
- `.env.example` - Environment variable template

## Key Dependencies

- **azure-ai-projects** `>=2.0.0b3` - NEW Foundry Agent creation (**beta - requires --pre flag**)
- **azure-identity** `>=1.25.1` - Azure authentication
- **openai** `>=2.15.0` - Responses API integration
- **python-dotenv** `>=1.2.1` - Environment variable management

## Important Notes

- This project uses **beta versions** of Azure AI Projects SDK (**requires --pre flag**)
- Agents are created using the **NEW Foundry Agent API** (not classic)
- Created agents appear in the Microsoft Foundry portal
- Uses the new **Responses API** with agent references
- **Critical:** Must use `uv add azure-ai-projects --pre` to install beta versions

## Next Steps

- See [AZURE_SETUP.md](AZURE_SETUP.md) for Azure resource configuration
- See [USAGE.md](USAGE.md) for agent creation patterns
- See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues

## Authentication

This project uses `DefaultAzureCredential` for authentication. Ensure you're logged in via Azure CLI:

```bash
az login
```
