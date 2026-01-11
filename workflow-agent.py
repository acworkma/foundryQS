import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import WorkflowAgentDefinition

load_dotenv()

# Workflow agent configuration
WORKFLOW_AGENT_NAME = "story-teller-multi-agent-workflow"
MODEL_DEPLOYMENT_NAME = "gpt-5.2"

print(f"Using PROJECT_ENDPOINT: {os.environ['PROJECT_ENDPOINT']}")
print(f"Creating workflow: {WORKFLOW_AGENT_NAME}")

project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

# Define the multi-agent workflow using the exact working YAML format
workflow_definition = """
kind: workflow
trigger:
  kind: OnConversationStart
  id: story_teller_multi_agent_workflow
  actions:
    - kind: SetVariable
      id: set_user_prompt
      variable: Local.UserPrompt
      value: =UserMessage(System.LastMessageText)
    - kind: InvokeAzureAgent
      id: deepseek_storyteller
      description: DeepSeek creates a story
      agent:
        name: agent-deepseek
      input:
        messages: =Local.UserPrompt
      output:
        messages: Local.DeepSeekStory
    - kind: InvokeAzureAgent
      id: gpt_storyteller
      description: GPT creates a story
      agent:
        name: agent-gpt
      input:
        messages: =Local.UserPrompt
      output:
        messages: Local.GPTStory
    - kind: InvokeAzureAgent
      id: mistral_storyteller
      description: Mistral creates a story
      agent:
        name: agent-mistral
      input:
        messages: =Local.UserPrompt
      output:
        messages: Local.MistralStory
    - kind: SendActivity
      id: send_results_summary
      activity: "🎯 Multi-Agent Storytelling Results - All three agents have completed their stories"
    - kind: SendActivity
      id: send_deepseek_story
      activity: "🔷 DeepSeek: {Last(Local.DeepSeekStory).Text}"
    - kind: SendActivity
      id: send_gpt_story
      activity: "🟢 GPT: {Last(Local.GPTStory).Text}"
    - kind: SendActivity
      id: send_mistral_story
      activity: "🔶 Mistral: {Last(Local.MistralStory).Text}"
    - kind: EndConversation
      id: end_workflow
name: story-teller-multi-agent-workflow
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