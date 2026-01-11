# Troubleshooting Guide

Common issues and solutions for Azure AI Foundry agent creation and usage.

## Environment Variable Issues

### KeyError: Environment variable not found

**Problem:** Script fails with `KeyError` for `PROJECT_ENDPOINT`, `AGENT_NAME`, or `MODEL_DEPLOYMENT_NAME`

**Solution:**
1. Create `.env` file from template:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your actual values:
   ```bash
   PROJECT_ENDPOINT=https://your-foundry-project.services.ai.azure.com/api/projects/your-project-name
   AGENT_NAME=helpful-assistant  
   MODEL_DEPLOYMENT_NAME=your-model-deployment-name
   ```

3. Verify environment loading:
   ```bash
   uv run python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('PROJECT_ENDPOINT'))"
   ```

### Invalid PROJECT_ENDPOINT format

**Problem:** Connection fails due to malformed endpoint URL

**Correct format:**
```
https://{resource-name}.services.ai.azure.com/api/projects/{project-name}
```

**Common mistakes:**
- Missing `/api/projects/` in path
- Wrong domain (should be `.services.ai.azure.com`)
- Including trailing slash

## Authentication Problems

### DefaultAzureCredential authentication failed

**Problem:** `DefaultAzureCredential` cannot authenticate

**Solutions:**

**Option 1 - Azure CLI (Recommended for development):**
```bash
az login
az account set --subscription "your-subscription-id"
```

**Option 2 - Service Principal:**
```bash
export AZURE_CLIENT_ID="your-client-id"
export AZURE_CLIENT_SECRET="your-client-secret"
export AZURE_TENANT_ID="your-tenant-id"
```

**Option 3 - Verify credentials:**
```bash
uv run python -c "from azure.identity import DefaultAzureCredential; print(DefaultAzureCredential().get_token('https://management.azure.com/.default'))"
```

### Insufficient permissions

**Problem:** Authentication succeeds but agent creation fails with permission errors

**Required roles:**
- **Cognitive Services Contributor** on the AI Foundry project
- **Read access** to model deployments
- **Agent creation permissions** in Foundry portal

**Check permissions:**
1. Log into Azure portal
2. Navigate to your AI Foundry resource
3. Check "Access control (IAM)"
4. Verify your identity has required roles

## Model Deployment Issues

### Model deployment not found

**Problem:** `MODEL_DEPLOYMENT_NAME` doesn't match deployed model

**Solution:**
1. Log into Azure AI Foundry portal
2. Navigate to your project
3. Go to "Model deployments" section
4. Copy exact deployment name (case-sensitive)
5. Update `MODEL_DEPLOYMENT_NAME` in `.env`

### Model deployment not accessible

**Problem:** Model exists but agent creation fails

**Check:**
- Model deployment is in **Active** status
- Model is deployed in same project as agent creation
- Your identity has access to the model deployment

## API Version Compatibility Issues

### Beta API breaking changes

**Problem:** Code works locally but fails in different environments

**This project uses beta versions:**
- `azure-ai-projects>=2.0.0b3` (beta)
- NEW Foundry Agent API (cutting-edge)

**Solutions:**
1. **Pin exact versions:**
   ```bash
   uv lock --upgrade
   ```

2. **Check for updates:**
   ```bash
   uv add azure-ai-projects --pre --upgrade
   ```

3. **Monitor breaking changes:**
   - Check Azure AI Foundry release notes
   - Test in development environment first

### Responses API errors

**Problem:** `agent_reference` parameter not recognized

**This is NEW Foundry specific:**
```python
# Correct NEW Foundry pattern
response = openai_client.beta.threads.runs.create_and_poll(
    thread_id=conversation.id,
    assistant_id=agent.id,
    agent_reference={"type": "agent", "id": agent.id}  # This is key
)
```

**Common mistakes:**
- Using classic OpenAI assistant patterns
- Missing `agent_reference` parameter
- Wrong agent reference format

## Connection and Network Issues

### Connection timeout or SSL errors

**Problem:** Network connectivity to Azure services

**Solutions:**
1. **Check firewall/proxy settings**
2. **Verify Azure service health**
3. **Test basic connectivity:**
   ```bash
   curl -v https://management.azure.com/
   ```

### Regional endpoint issues

**Problem:** Service not available in specified region

**Check:**
- Azure AI Foundry availability in your region
- Model deployment regional restrictions
- Cross-region networking policies

## Python and Dependency Issues

### Python version compatibility

**Problem:** Code fails with older Python versions

**Requirements:**
- **Python 3.12+** (specified in `.python-version`)
- Use `uv` package manager for best compatibility

**Verify version:**
```bash
python --version  # Should show 3.12+
uv python list    # Show available Python versions
```

### Package installation failures

**Problem:** `uv sync` fails or packages conflict

**Solutions:**
1. **Clear cache:**
   ```bash
   uv cache clean
   ```

2. **Reinstall from lock:**
   ```bash
   rm -rf .venv
   uv sync
   ```

3. **Update dependencies:**
   ```bash
   uv lock --upgrade
   ```

## Getting Help

If issues persist:

1. **Check Azure AI Foundry service health**
2. **Review Azure portal logs** for your project
3. **Enable debug logging** in your Python script:
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

4. **Test with minimal example** to isolate the issue