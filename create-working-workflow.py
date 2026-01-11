import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import WorkflowAgentDefinition

load_dotenv()

project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

# Create a corrected workflow that matches our deployed agents exactly
corrected_workflow = """
trigger:
  kind: OnConversationStart
  actions:
    - kind: SetVariable
      id: capture_input
      variable_name: UserPrompt
      variable_value: "=UserMessage(System.LastMessageText)"
      
    - kind: InvokeAzureAgent
      id: call_deepseek
      agent_name: "agent-deepseek"
      input: "=Local.UserPrompt"
      output_variable: DeepSeekStory
      
    - kind: InvokeAzureAgent
      id: call_gpt
      agent_name: "agent-gpt"
      input: "=Local.UserPrompt"
      output_variable: GPTStory
      
    - kind: InvokeAzureAgent
      id: call_mistral
      agent_name: "agent-mistral"
      input: "=Local.UserPrompt"
      output_variable: MistralStory
      
    - kind: SendActivity
      id: send_results
      activity:
        type: message
        text: "=Concat('🤖 MULTI-AGENT STORYTELLING RESULTS\\n\\n', '✅ DEEPSEEK STORY:\\n', Local.DeepSeekStory, '\\n\\n', '✅ GPT STORY:\\n', Local.GPTStory, '\\n\\n', '✅ MISTRAL STORY:\\n', Local.MistralStory)"
"""

try:
    # Create a new working workflow agent
    working_workflow = project_client.agents.create_version(
        agent_name="working-multi-agent-workflow", 
        definition=WorkflowAgentDefinition(workflow=corrected_workflow)
    )
    
    print(f"✅ Created working workflow: {working_workflow.name}")
    print(f"   ID: {working_workflow.id}")
    
    # Test the new workflow
    openai_client = project_client.get_openai_client()
    conversation = openai_client.conversations.create()
    
    print("Testing the new working workflow...")
    
    response = openai_client.responses.create(
        conversation=conversation.id,
        extra_body={"agent": {"name": working_workflow.name, "type": "agent_reference"}},
        input="Tell me a story about a robot who learns to paint"
    )
    
    print("✅ Working workflow executed successfully!")
    print("\n" + "="*60)
    print(response.output_text)
    print("="*60)
    
except Exception as e:
    print(f"❌ Failed to create/test working workflow: {e}")
    print("\nThe existing workflow might have syntax errors.")
    print("Try manually editing it in the portal YAML tab to fix the agent references.")