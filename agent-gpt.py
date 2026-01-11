import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition

load_dotenv()

# GPT-specific configuration
MODEL_DEPLOYMENT_NAME = "gpt-5.2"
AGENT_NAME = "agent-gpt"

print(f"Using PROJECT_ENDPOINT: {os.environ['PROJECT_ENDPOINT']}")
print(f"Using MODEL_DEPLOYMENT_NAME: {MODEL_DEPLOYMENT_NAME}")

project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

# Create a NEW Foundry agent (not classic) using GPT-5.2
agent = project_client.agents.create_version(
    agent_name=AGENT_NAME,
    definition=PromptAgentDefinition(
        model=MODEL_DEPLOYMENT_NAME,
        instructions="You are a storytelling agent. You craft engaging one-line stories based on user prompts and context.",
    ),
)
print(f"NEW Foundry Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")

# Get OpenAI client for the new Responses API
openai_client = project_client.get_openai_client()

# Create a conversation for context
conversation = openai_client.conversations.create()
print(f"Created conversation (id: {conversation.id})")

# Use the new Responses API with agent reference
response = openai_client.responses.create(
    conversation=conversation.id,
    extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
    input="Explain the evolution from GPT-4 to GPT-5.2 and what new capabilities it brings.",
)
print(f"Response output: {response.output_text}")

print(f"\n✨ NEW Foundry Agent {agent.name} should now appear in the Microsoft Foundry portal!")