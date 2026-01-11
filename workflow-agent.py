import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import WorkflowAgentDefinition

load_dotenv()

# Workflow agent configuration
WORKFLOW_AGENT_NAME = "multi-agent-storytelling-workflow"
MODEL_DEPLOYMENT_NAME = "gpt-5.2"

print(f"Using PROJECT_ENDPOINT: {os.environ['PROJECT_ENDPOINT']}")
print(f"Creating workflow: {WORKFLOW_AGENT_NAME}")

project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

# Define the multi-agent workflow using NEW Foundry YAML schema
workflow_definition = """
trigger:
  kind: OnConversationStart
  actions:
    - kind: SetVariable
      id: set_user_input
      variable_name: UserInput
      variable_value: "=UserMessage(System.LastMessageText)"
      
    - kind: InvokeAzureAgent
      id: call_deepseek
      agent_name: agent-deepseek
      input: "=Local.UserInput"
      output_variable: DeepSeekResult
      
    - kind: InvokeAzureAgent
      id: call_gpt
      agent_name: agent-gpt
      input: "=Local.UserInput"
      output_variable: GPTResult
      
    - kind: InvokeAzureAgent
      id: call_mistral
      agent_name: agent-mistral
      input: "=Local.UserInput"
      output_variable: MistralResult
      
    - kind: SetVariable
      id: format_output
      variable_name: FinalOutput
      variable_value: "=Concat('🤖 MULTI-AGENT RESPONSES\\n\\n✅ DEEPSEEK:\\n', Local.DeepSeekResult, '\\n\\n✅ GPT:\\n', Local.GPTResult, '\\n\\n✅ MISTRAL:\\n', Local.MistralResult)"
      
    - kind: SendActivity
      id: send_response
      activity:
        type: message
        text: "=Local.FinalOutput"
"""

# Create NEW Foundry workflow agent with YAML definition
workflow_agent = project_client.agents.create_version(
    agent_name=WORKFLOW_AGENT_NAME,
    definition=WorkflowAgentDefinition(
        workflow=workflow_definition
    ),
)

print(f"✅ NEW Foundry Workflow Agent created!")
print(f"   ID: {workflow_agent.id}")
print(f"   Name: {workflow_agent.name}")
print(f"   Version: {workflow_agent.version}")

# Test the workflow
openai_client = project_client.get_openai_client()

# Create conversation for the workflow
workflow_conversation = openai_client.conversations.create()
print(f"Created workflow conversation: {workflow_conversation.id}")

# Trigger the multi-agent workflow
test_input = "Tell me a story about a time-traveling librarian who discovers a book that writes itself"

print(f"\n🚀 Testing workflow with: '{test_input}'")

response = openai_client.responses.create(
    conversation=workflow_conversation.id,
    extra_body={"agent": {"name": workflow_agent.name, "type": "agent_reference"}},
    input=test_input
)

print(f"\n🎯 Workflow Response:")
print("=" * 60)
print(response.output_text)
print("=" * 60)

print(f"\n✨ Visual workflow '{WORKFLOW_AGENT_NAME}' should now appear in the Microsoft Foundry portal's Workflows section!")