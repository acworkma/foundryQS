# Azure AI Foundry Setup Guide

This guide covers setting up Azure resources and configuration for the NEW Foundry Agent API.

## Azure Resource Requirements

### 1. Azure AI Foundry Project

You need an existing Azure AI Foundry project with:
- **Project endpoint** in format: `https://{resource-name}.services.ai.azure.com/api/projects/{project-name}`
- **Proper permissions** for agent creation
- **Access to deployed models**

### 2. Model Deployment

Ensure you have a deployed model accessible via:
- **Deployment name** (e.g., "DeepSeek-V3.2", "gpt-4o", etc.)
- **Model must be accessible** from your Foundry project
- **Deployment name must match** the value in `MODEL_DEPLOYMENT_NAME`

### 3. Authentication Setup

This project uses `DefaultAzureCredential` which supports:

**Azure CLI (Recommended for development):**
```bash
az login
```

**Managed Identity (For production):**
- Configure system-assigned or user-assigned managed identity
- Ensure identity has access to your Foundry project

**Service Principal (Alternative):**
```bash
export AZURE_CLIENT_ID="your-client-id"
export AZURE_CLIENT_SECRET="your-client-secret" 
export AZURE_TENANT_ID="your-tenant-id"
```

## Configuration Details

### Project Endpoint Format
```
https://{resource-name}.services.ai.azure.com/api/projects/{project-name}
```

**Example:**
```
https://foundry-acw.services.ai.azure.com/api/projects/proj-acw
```

### Required Permissions

Your Azure identity needs:
- **Cognitive Services Contributor** role on the AI Foundry project
- **Read access** to deployed models
- **Agent creation permissions** in Foundry portal

## Verification Steps

1. **Test authentication:**
   ```bash
   uv run python -c "from azure.identity import DefaultAzureCredential; DefaultAzureCredential().get_token('https://management.azure.com/.default')"
   ```

2. **Verify project access:**
   ```bash
   uv run python -c "from azure.ai.projects import AIProjectClient; from azure.identity import DefaultAzureCredential; client = AIProjectClient(endpoint='YOUR_ENDPOINT', credential=DefaultAzureCredential())"
   ```

3. **Check model deployment:**
   - Log into Azure AI Foundry portal
   - Navigate to your project
   - Verify model deployment is active and accessible

## NEW Foundry vs Classic Agents

This project specifically uses:
- **NEW Foundry Agent API** via `azure-ai-projects>=2.0.0b3` (**beta - requires --pre flag**)
- **Agent creation** with `client.agents.create_version()`
- **Responses API** with agent references
- **Portal integration** - agents appear in Foundry dashboard

**Installation requirement:**
```bash
uv add azure-ai-projects --pre
```

**Note:** This is different from classic Azure OpenAI assistant creation patterns.