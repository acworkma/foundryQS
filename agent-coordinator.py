import os
import asyncio
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition

load_dotenv()

# Coordinator agent configuration
AGENT_NAME = "agent-coordinator"
MODEL_DEPLOYMENT_NAME = "gpt-5.2"  # Use GPT for orchestration

# Target agents to coordinate
TARGET_AGENTS = [
    {"name": "agent-deepseek", "model": "DeepSeek-V3.2"},
    {"name": "agent-gpt", "model": "gpt-5.2"}, 
    {"name": "agent-mistral", "model": "Mistral-Large-3"}
]

print(f"Using PROJECT_ENDPOINT: {os.environ['PROJECT_ENDPOINT']}")
print(f"Using MODEL_DEPLOYMENT_NAME: {MODEL_DEPLOYMENT_NAME}")

project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

# Create coordinator agent using NEW Foundry Agent Service
coordinator_agent = project_client.agents.create_version(
    agent_name=AGENT_NAME,
    definition=PromptAgentDefinition(
        model=MODEL_DEPLOYMENT_NAME,
        instructions="You are a coordinator agent that orchestrates storytelling from multiple AI agents. You present their responses in a clear, side-by-side format for comparison.",
    ),
)
print(f"NEW Foundry Coordinator Agent created (id: {coordinator_agent.id}, name: {coordinator_agent.name}, version: {coordinator_agent.version})")

# Get OpenAI client for NEW Foundry Responses API
openai_client = project_client.get_openai_client()

async def call_agent_async(agent_info, user_input, timeout=30):
    """Call a specific agent asynchronously with error handling"""
    try:
        print(f"Calling {agent_info['name']}...")
        
        # Create conversation for this agent
        conversation = openai_client.conversations.create()
        
        # Use NEW Foundry Responses API with agent reference
        response = openai_client.responses.create(
            conversation=conversation.id,
            extra_body={"agent": {"name": agent_info['name'], "type": "agent_reference"}},
            input=user_input
        )
        
        return {
            "agent": agent_info['name'],
            "model": agent_info['model'],
            "response": response.output_text,
            "status": "success"
        }
    except Exception as e:
        return {
            "agent": agent_info['name'],
            "model": agent_info['model'], 
            "response": f"Sorry, {agent_info['name']} is currently unavailable. Error: {str(e)}",
            "status": "error"
        }

def call_agent_sync(agent_info, user_input):
    """Synchronous fallback for calling agents"""
    try:
        print(f"Calling {agent_info['name']} (sync)...")
        
        conversation = openai_client.conversations.create()
        response = openai_client.responses.create(
            conversation=conversation.id,
            extra_body={"agent": {"name": agent_info['name'], "type": "agent_reference"}},
            input=user_input
        )
        
        return {
            "agent": agent_info['name'],
            "model": agent_info['model'],
            "response": response.output_text,
            "status": "success"
        }
    except Exception as e:
        return {
            "agent": agent_info['name'],
            "model": agent_info['model'],
            "response": f"Sorry, {agent_info['name']} is currently unavailable. Error: {str(e)}",
            "status": "error"
        }

async def orchestrate_agents_parallel(user_input):
    """Try parallel execution first"""
    try:
        print("Attempting parallel execution...")
        tasks = [call_agent_async(agent, user_input) for agent in TARGET_AGENTS]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Convert exceptions to error responses
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append({
                    "agent": TARGET_AGENTS[i]['name'],
                    "model": TARGET_AGENTS[i]['model'],
                    "response": f"Sorry, {TARGET_AGENTS[i]['name']} failed during parallel execution.",
                    "status": "error"
                })
            else:
                processed_results.append(result)
        
        return processed_results
    except Exception as e:
        print(f"Parallel execution failed: {e}")
        return None

def orchestrate_agents_sequential(user_input):
    """Sequential fallback execution"""
    print("Using sequential execution...")
    results = []
    for agent in TARGET_AGENTS:
        result = call_agent_sync(agent, user_input)
        results.append(result)
    return results

def format_responses_side_by_side(results):
    """Format agent responses in side-by-side layout"""
    output = "\n" + "="*80 + "\n"
    output += "🤖 MULTI-AGENT STORYTELLING RESPONSES\n"
    output += "="*80 + "\n\n"
    
    for result in results:
        status_emoji = "✅" if result['status'] == 'success' else "❌"
        output += f"{status_emoji} {result['agent'].upper()} ({result['model']})\n"
        output += "-" * 60 + "\n"
        output += f"{result['response']}\n\n"
    
    output += "="*80 + "\n"
    return output

# Main orchestration workflow
async def run_coordinator_workflow():
    user_input = "Tell me a story about a robot who dreams of becoming a chef"
    
    print(f"🚀 Starting multi-agent orchestration for: '{user_input}'")
    
    # Try parallel execution first
    results = await orchestrate_agents_parallel(user_input)
    
    # Fallback to sequential if parallel fails
    if results is None:
        results = orchestrate_agents_sequential(user_input)
    
    # Format and display results
    formatted_output = format_responses_side_by_side(results)
    print(formatted_output)
    
    # Create coordinator conversation to show workflow completion
    coordinator_conversation = openai_client.conversations.create()
    coordinator_response = openai_client.responses.create(
        conversation=coordinator_conversation.id,
        extra_body={"agent": {"name": coordinator_agent.name, "type": "agent_reference"}},
        input=f"Summarize this multi-agent coordination result: {formatted_output}"
    )
    
    print("🎯 Coordinator Summary:")
    print("-" * 40)
    print(coordinator_response.output_text)
    
    return results

if __name__ == "__main__":
    # Run the async orchestration
    results = asyncio.run(run_coordinator_workflow())
    print(f"\n✨ Multi-agent workflow completed! All agents should appear in the Microsoft Foundry portal.")
    print(f"📊 Coordination Results: {len([r for r in results if r['status'] == 'success'])}/{len(results)} agents responded successfully")