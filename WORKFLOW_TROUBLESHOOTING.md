# Microsoft Foundry Visual Workflow Troubleshooting Guide

## 🚨 CRITICAL ISSUE IDENTIFIED: Agent Name Mismatches

### Problem Summary
Your visual workflow references agent names that **don't match** your deployed agent names:

**Deployed Agents:**
- `agent-deepseek` (from agent-deepseek.py)
- `agent-gpt` (from agent-gpt.py) 
- `agent-mistral` (from agent-mistral.py)
- `agent-coordinator` (from agent-coordinator.py)

**Workflow References:**
- `deepseek-storyteller` ❌ (should be `agent-deepseek`)
- `gpt-storyteller` ❌ (should be `agent-gpt`)
- `mistral-storyteller` ❌ (should be `agent-mistral`)
- `story-coordinator` ❌ (should be `agent-coordinator`)

## 🔧 Common Microsoft Foundry Workflow Execution Issues

### 1. Agent Name Mismatches (MOST COMMON)
**Symptoms:** Workflow appears correctly in portal but fails to execute
**Cause:** Agent names in workflow YAML don't match deployed agent names
**Fix:** Ensure exact name matching (case-sensitive)

### 2. Variable Reference Syntax Errors
**Common Issues:**
- Missing `=` prefix for expressions: Use `"=Local.VariableName"` 
- Incorrect variable scoping: Use `Local.`, `System.`, or `Global.`
- Case sensitivity: `Local.UserPrompt` vs `Local.userprompt`

### 3. Model Deployment Availability
**Symptoms:** Agents exist but workflow fails when invoking specific models
**Check:**
- Verify model deployment names exactly match: `DeepSeek-V3.2`, `gpt-5.2`, `Mistral-Large-3`
- Ensure models are deployed and available in your Azure AI Foundry project
- Check quota and rate limits for each model

### 4. Conversation Flow Issues
**Common Problems:**
- Missing CreateConversation steps
- Incorrect conversationId references
- Using wrong conversation IDs in agent invocations

### 5. Input/Output Parameter Problems
**Issues:**
- Incorrect message formatting in input
- Wrong output variable assignments
- Missing or malformed `messages` parameters

### 6. Authentication & Permissions
**Check:**
- Azure credentials have proper permissions
- PROJECT_ENDPOINT is correct and accessible
- All agents were created with same credential context

## 🔍 Debugging Steps

### Step 1: Verify Agent Names
```bash
# Run each agent creation script to confirm names
python agent-deepseek.py
python agent-gpt.py  
python agent-mistral.py
python agent-coordinator.py
```

### Step 2: Check Model Deployments
- Log into Azure AI Foundry portal
- Navigate to Deployments section
- Verify exact model deployment names

### Step 3: Test Individual Agents
```bash
# Test each agent individually
python -c "
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
import os
from dotenv import load_dotenv

load_dotenv()
client = AIProjectClient(endpoint=os.environ['PROJECT_ENDPOINT'], credential=DefaultAzureCredential())

# List all agents to see exact names
agents = client.agents.list()
for agent in agents:
    print(f'Agent Name: {agent.name}, ID: {agent.id}')
"
```

### Step 4: Validate Workflow YAML Syntax
- Check for proper indentation (YAML is indent-sensitive)
- Verify all variable references use correct syntax
- Ensure agent names match exactly

## 🛠️ Quick Fixes

### Option 1: Update Workflow to Match Existing Agents
Change workflow agent names from:
- `deepseek-storyteller` → `agent-deepseek`
- `gpt-storyteller` → `agent-gpt`
- `mistral-storyteller` → `agent-mistral`
- `story-coordinator` → `agent-coordinator`

### Option 2: Update Agents to Match Workflow
Change agent creation names to match workflow expectations:
- `agent-deepseek` → `deepseek-storyteller`
- `agent-gpt` → `gpt-storyteller`
- `agent-mistral` → `mistral-storyteller`
- `agent-coordinator` → `story-coordinator`

## 🔄 Testing Workflow Execution

1. **Portal Testing:** Use the "Test" button in Microsoft Foundry portal
2. **Programmatic Testing:** Run workflow via API with debug mode enabled
3. **Check Logs:** Monitor execution logs for specific error messages
4. **Step-by-step:** Test each workflow node individually

## 📊 Workflow Validation Checklist

- [ ] All agent names match exactly (case-sensitive)
- [ ] Model deployments are available and accessible
- [ ] Variable references use correct syntax (`=Local.VariableName`)
- [ ] All CreateConversation nodes have unique IDs
- [ ] Input/output parameters are correctly formatted
- [ ] Workflow YAML syntax is valid
- [ ] Authentication credentials are properly configured
- [ ] No circular dependencies in workflow flow

## ⚡ Emergency Recovery

If workflow is completely broken:
1. Delete the workflow agent
2. Recreate individual agents with consistent naming
3. Recreate workflow with corrected agent references
4. Test step-by-step execution

## 📝 Prevention Tips

1. **Consistent Naming:** Use a standard naming convention across all agents
2. **Environment Variables:** Use .env for agent names to avoid hardcoding
3. **Version Control:** Track workflow YAML changes
4. **Testing:** Always test individual agents before workflow integration
5. **Documentation:** Keep agent names and purposes documented