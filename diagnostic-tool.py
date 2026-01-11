#!/usr/bin/env python3
"""
Microsoft Foundry Workflow Diagnostic Tool
Helps identify common issues preventing workflows from executing
"""

import os
import asyncio
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

load_dotenv()

async def run_diagnostic():
    """Run comprehensive diagnostic of your Foundry setup"""
    print("🔍 Microsoft Foundry Workflow Diagnostic Tool")
    print("=" * 60)
    
    # Check 1: Environment Configuration
    print("\n1️⃣ ENVIRONMENT CONFIGURATION")
    print("-" * 30)
    
    project_endpoint = os.environ.get("PROJECT_ENDPOINT")
    if project_endpoint:
        print(f"✅ PROJECT_ENDPOINT: {project_endpoint}")
    else:
        print("❌ PROJECT_ENDPOINT not found in environment")
        return False
    
    # Check 2: Azure Connection
    print("\n2️⃣ AZURE CONNECTION")
    print("-" * 30)
    
    try:
        project_client = AIProjectClient(
            endpoint=project_endpoint,
            credential=DefaultAzureCredential(),
        )
        print("✅ Azure connection successful")
    except Exception as e:
        print(f"❌ Azure connection failed: {e}")
        return False
    
    # Check 3: List All Agents
    print("\n3️⃣ DEPLOYED AGENTS")
    print("-" * 30)
    
    try:
        agents = project_client.agents.list()
        if hasattr(agents, 'data') and agents.data:
            agent_list = agents.data
        else:
            agent_list = agents if isinstance(agents, list) else []
            
        if not agent_list:
            print("❌ No agents found")
            return False
        
        deployed_agents = {}
        for agent in agent_list:
            deployed_agents[agent.name] = {
                'id': agent.id,
                'version': agent.version,
                'model': getattr(agent, 'model', 'Unknown')
            }
            print(f"✅ {agent.name}")
            print(f"   ID: {agent.id}")
            print(f"   Version: {agent.version}")
    
    except Exception as e:
        print(f"❌ Error listing agents: {e}")
        return False
    
    # Check 4: Workflow Agent Analysis
    print("\n4️⃣ WORKFLOW AGENT ANALYSIS")
    print("-" * 30)
    
    expected_agents = ["agent-deepseek", "agent-gpt", "agent-mistral", "agent-coordinator"]
    workflow_agents = ["deepseek-storyteller", "gpt-storyteller", "mistral-storyteller", "story-coordinator"]
    
    print("Expected for workflow execution:")
    missing_agents = []
    
    for expected in expected_agents:
        if expected in deployed_agents:
            print(f"✅ {expected} - EXISTS")
        else:
            print(f"❌ {expected} - MISSING")
            missing_agents.append(expected)
    
    print("\nOriginal workflow references:")
    for workflow_agent in workflow_agents:
        if workflow_agent in deployed_agents:
            print(f"✅ {workflow_agent} - EXISTS")
        else:
            print(f"❌ {workflow_agent} - MISSING (workflow will fail)")
    
    # Check 5: Agent Name Mismatch Detection
    print("\n5️⃣ AGENT NAME MISMATCH DETECTION")
    print("-" * 30)
    
    if missing_agents:
        print(f"🚨 CRITICAL ISSUE: Agent name mismatches detected!")
        print(f"Your workflow expects these agent names:")
        for workflow_agent in workflow_agents:
            print(f"   • {workflow_agent}")
        print(f"\nBut you have these deployed agents:")
        for deployed_agent in deployed_agents.keys():
            print(f"   • {deployed_agent}")
        print(f"\n💡 SOLUTION: Use the corrected workflow in 'workflow-visual-fixed.py'")
    else:
        print("✅ All expected agents found - workflow should execute properly")
    
    # Check 6: Model Deployments
    print("\n6️⃣ MODEL DEPLOYMENT CHECK")
    print("-" * 30)
    
    expected_models = ["DeepSeek-V3.2", "gpt-5.2", "Mistral-Large-3"]
    print("Expected model deployments:")
    for model in expected_models:
        print(f"   • {model} (verify this exists in Azure AI Foundry portal)")
    
    # Check 7: Test Simple Agent Call
    print("\n7️⃣ AGENT CONNECTIVITY TEST")
    print("-" * 30)
    
    if deployed_agents:
        test_agent_name = list(deployed_agents.keys())[0]
        try:
            openai_client = project_client.get_openai_client()
            conversation = openai_client.conversations.create()
            
            response = openai_client.responses.create(
                conversation=conversation.id,
                extra_body={"agent": {"name": test_agent_name, "type": "agent_reference"}},
                input="Hello, this is a connectivity test.",
            )
            print(f"✅ Agent connectivity test passed with {test_agent_name}")
            print(f"   Response preview: {response.output_text[:100]}...")
        except Exception as e:
            print(f"❌ Agent connectivity test failed: {e}")
            print(f"   This may indicate model deployment or permission issues")
    
    # Summary and Recommendations
    print("\n" + "=" * 60)
    print("📋 DIAGNOSTIC SUMMARY & RECOMMENDATIONS")
    print("=" * 60)
    
    if missing_agents:
        print("\n🚨 PRIMARY ISSUE: Agent Name Mismatches")
        print("IMMEDIATE ACTIONS:")
        print("1. Run: python workflow-visual-fixed.py")
        print("2. This creates a corrected workflow with proper agent names")
        print("3. Test the new workflow in Microsoft Foundry portal")
        print("\nALTERNATIVE:")
        print("1. Update your existing agents to use workflow-expected names")
        print("2. Re-deploy agents with names: deepseek-storyteller, gpt-storyteller, etc.")
    else:
        print("✅ No critical issues detected")
        print("Your workflow should execute properly")
    
    print("\nGENERAL TROUBLESHOOTING:")
    print("• Verify all model deployments exist in Azure AI Foundry portal")
    print("• Check quota limits for each model")
    print("• Ensure proper Azure permissions")
    print("• Test individual agents before workflow execution")
    
    return True

def main():
    """Run the diagnostic tool"""
    try:
        asyncio.run(run_diagnostic())
    except Exception as e:
        print(f"\n❌ Diagnostic failed: {e}")
        print("Check your .env file and Azure configuration")

if __name__ == "__main__":
    main()