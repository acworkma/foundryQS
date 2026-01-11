import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition

load_dotenv()

print(f"Using PROJECT_ENDPOINT: {os.environ['PROJECT_ENDPOINT']}")
print(f"Using MODEL_DEPLOYMENT_NAME: {os.environ['MODEL_DEPLOYMENT_NAME']}")

project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

# Create a NEW Foundry agent (not classic)
agent = project_client.agents.create_version(
    agent_name=os.environ["AGENT_NAME"],
    definition=PromptAgentDefinition(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        instructions="You are a helpful assistant that answers general questions",
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
    input="Tell me a fun fact about space",
)
print(f"Response output: {response.output_text}")

print(f"\n✨ NEW Foundry Agent {agent.name} should now appear in the Microsoft Foundry portal!")
