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
   uv sync
   ```

2. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your Azure AI Foundry project details
   ```

3. **Run the agent creation script:**
   ```bash
   uv run python agent.py
   ```

## Project Structure

- `agent.py` - Main agent creation script (environment-driven)
- `main.py` - Direct agent creation example (hardcoded config)
- `quickstart.py` - Basic placeholder script
- `pyproject.toml` - Project dependencies and configuration
- `uv.lock` - Locked dependency versions
- `.env.example` - Environment variable template

## Key Dependencies

- **azure-ai-projects** `>=2.0.0b3` - NEW Foundry Agent creation (beta)
- **azure-identity** `>=1.25.1` - Azure authentication
- **openai** `>=2.15.0` - Responses API integration
- **python-dotenv** `>=1.2.1` - Environment variable management

## Important Notes

- This project uses **beta versions** of Azure AI Projects SDK
- Agents are created using the **NEW Foundry Agent API** (not classic)
- Created agents appear in the Microsoft Foundry portal
- Uses the new **Responses API** with agent references

## Next Steps

- See [AZURE_SETUP.md](AZURE_SETUP.md) for Azure resource configuration
- See [USAGE.md](USAGE.md) for agent creation patterns
- See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues

## Authentication

This project uses `DefaultAzureCredential` for authentication. Ensure you're logged in via Azure CLI:

```bash
az login
```
