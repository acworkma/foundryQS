import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

load_dotenv()

project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

# Let's test the existing workflow by triggering it
openai_client = project_client.get_openai_client()

# Test the visual workflow that's already created
print("Testing the existing visual workflow...")

# The issue might be that the workflow references agents that don't exist
# Let's test our individual agents first to make sure they work
print("Testing individual agents...")

individual_agents = ["agent-deepseek", "agent-gpt", "agent-mistral"]

for agent_name in individual_agents:
    try:
        conversation = openai_client.conversations.create()
        print(f"Testing {agent_name}...")
        
        response = openai_client.responses.create(
            conversation=conversation.id,
            extra_body={"agent": {"name": agent_name, "type": "agent_reference"}},
            input="Quick test - tell a short story about a cat"
        )
        
        print(f"✅ {agent_name} works: {response.output_text[:100]}...")
        
    except Exception as e:
        print(f"❌ {agent_name} failed: {e}")

print("\nNow testing the workflow...")

try:
    # Create fresh conversation  
    conversation = openai_client.conversations.create()
    print(f"Created conversation: {conversation.id}")
    
    # The workflow name from the portal screenshot
    response = openai_client.responses.create(
        conversation=conversation.id,
        extra_body={"agent": {"name": "visual-multi-agent-storytelling-workflow", "type": "agent_reference"}},
        input="Tell me a story about a robot who learns to paint"
    )
    
    print("✅ Workflow executed successfully!")
    print("Response:", response.output_text)
    
except Exception as e:
    print(f"❌ Workflow execution failed: {e}")