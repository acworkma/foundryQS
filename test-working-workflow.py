import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

load_dotenv()

project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

openai_client = project_client.get_openai_client()

print("🚀 Testing the working workflow: working-multi-agent-workflow-v2")

# Create fresh conversation
conversation = openai_client.conversations.create()
print(f"Created conversation: {conversation.id}")

# Test the workflow with a storytelling prompt
test_prompt = "Tell me a story about a robot who discovers music for the first time"

try:
    response = openai_client.responses.create(
        conversation=conversation.id,
        extra_body={"agent": {"name": "working-multi-agent-workflow-v2", "type": "agent_reference"}},
        input=test_prompt
    )
    
    print("✅ Workflow executed successfully!")
    print("\n" + "="*80)
    print("WORKFLOW RESPONSE:")
    print("="*80)
    print(response.output_text)
    print("="*80)
    
except Exception as e:
    print(f"❌ Workflow failed: {e}")
    
    # Try to get more details about the failure
    print("Let's check if there are any specific error details...")