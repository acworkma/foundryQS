import os
import asyncio
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    PromptAgentDefinition, 
    WorkflowAgentDefinition,
    ResponseStreamEventType,
    ItemType
)

load_dotenv()

# Configuration
PROJECT_ENDPOINT = os.environ["PROJECT_ENDPOINT"]
MODEL_DEPLOYMENT_NAME = "gpt-5.2"  # Use your model deployment

print(f"Using PROJECT_ENDPOINT: {PROJECT_ENDPOINT}")
print(f"Using MODEL_DEPLOYMENT_NAME: {MODEL_DEPLOYMENT_NAME}")

project_client = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
)

async def create_visual_workflow():
    """Create a visual workflow that appears in Microsoft Foundry portal"""
    
    # First, create the individual agents that will be used in the workflow
    storytelling_agents = []
    
    # Create DeepSeek storytelling agent
    deepseek_agent = project_client.agents.create_version(
        agent_name="deepseek-storyteller",
        definition=PromptAgentDefinition(
            model="DeepSeek-V3.2",
            instructions="You are a creative storyteller specializing in science fiction and technology themes. Write engaging, imaginative stories.",
        ),
    )
    storytelling_agents.append(deepseek_agent)
    print(f"Created DeepSeek Agent (id: {deepseek_agent.id}, name: {deepseek_agent.name})")
    
    # Create GPT storytelling agent
    gpt_agent = project_client.agents.create_version(
        agent_name="gpt-storyteller",
        definition=PromptAgentDefinition(
            model="gpt-5.2",
            instructions="You are a storyteller focused on character development and emotional narratives. Create compelling stories with deep character arcs.",
        ),
    )
    storytelling_agents.append(gpt_agent)
    print(f"Created GPT Agent (id: {gpt_agent.id}, name: {gpt_agent.name})")
    
    # Create Mistral storytelling agent
    mistral_agent = project_client.agents.create_version(
        agent_name="mistral-storyteller", 
        definition=PromptAgentDefinition(
            model="Mistral-Large-3",
            instructions="You are a storyteller specializing in adventure and action narratives. Write thrilling, fast-paced stories.",
        ),
    )
    storytelling_agents.append(mistral_agent)
    print(f"Created Mistral Agent (id: {mistral_agent.id}, name: {mistral_agent.name})")
    
    # Create Coordinator Agent
    coordinator_agent = project_client.agents.create_version(
        agent_name="story-coordinator",
        definition=PromptAgentDefinition(
            model=MODEL_DEPLOYMENT_NAME,
            instructions="You are a story coordinator that evaluates and selects the best story from multiple AI storytellers. Provide analysis and pick the winner.",
        ),
    )
    print(f"Created Coordinator Agent (id: {coordinator_agent.id}, name: {coordinator_agent.name})")

    # Define the visual workflow YAML
    workflow_yaml = f"""
kind: workflow
trigger:
  kind: OnConversationStart
  id: multi_agent_storytelling_workflow
  actions:
    - kind: SetVariable
      id: set_user_prompt
      variable: Local.UserPrompt
      value: "=UserMessage(System.LastMessageText)"

    - kind: SetVariable
      id: set_story_count
      variable: Local.StoryCount
      value: "=0"

    # Create separate conversations for each storytelling agent
    - kind: CreateConversation
      id: create_deepseek_conversation
      conversationId: Local.DeepSeekConversationId

    - kind: CreateConversation
      id: create_gpt_conversation
      conversationId: Local.GPTConversationId

    - kind: CreateConversation
      id: create_mistral_conversation
      conversationId: Local.MistralConversationId

    - kind: CreateConversation
      id: create_coordinator_conversation
      conversationId: Local.CoordinatorConversationId

    # Invoke DeepSeek Storyteller
    - kind: InvokeAzureAgent
      id: deepseek_storyteller
      description: "DeepSeek creates a sci-fi story"
      conversationId: "=Local.DeepSeekConversationId"
      agent:
        name: {deepseek_agent.name}
      input:
        messages: "=Local.UserPrompt"
      output:
        messages: Local.DeepSeekStory

    # Invoke GPT Storyteller
    - kind: InvokeAzureAgent
      id: gpt_storyteller
      description: "GPT creates a character-driven story"
      conversationId: "=Local.GPTConversationId"
      agent:
        name: {gpt_agent.name}
      input:
        messages: "=Local.UserPrompt"
      output:
        messages: Local.GPTStory

    # Invoke Mistral Storyteller
    - kind: InvokeAzureAgent
      id: mistral_storyteller
      description: "Mistral creates an adventure story"
      conversationId: "=Local.MistralConversationId"
      agent:
        name: {mistral_agent.name}
      input:
        messages: "=Local.UserPrompt"
      output:
        messages: Local.MistralStory

    # Coordinator evaluates all stories
    - kind: InvokeAzureAgent
      id: story_coordinator
      description: "Coordinator evaluates and selects the best story"
      conversationId: "=Local.CoordinatorConversationId"
      agent:
        name: {coordinator_agent.name}
      input:
        messages: "=Concat('Evaluate these three stories and select the best one:\\n\\n**DeepSeek Story:**\\n', Last(Local.DeepSeekStory).Text, '\\n\\n**GPT Story:**\\n', Last(Local.GPTStory).Text, '\\n\\n**Mistral Story:**\\n', Last(Local.MistralStory).Text, '\\n\\nProvide your analysis and selection.')"
      output:
        messages: Local.FinalEvaluation

    # Send final results
    - kind: SendActivity
      id: send_final_results
      activity: "=Concat('🎯 **MULTI-AGENT STORYTELLING RESULTS**\\n\\n', '📚 **Stories Generated:**\\n\\n', '🤖 **DeepSeek (Sci-Fi):** ', Last(Local.DeepSeekStory).Text, '\\n\\n', '🤖 **GPT (Character-Driven):** ', Last(Local.GPTStory).Text, '\\n\\n', '🤖 **Mistral (Adventure):** ', Last(Local.MistralStory).Text, '\\n\\n', '🏆 **Coordinator Evaluation:**\\n', Last(Local.FinalEvaluation).Text)"

    - kind: EndConversation
      id: end_workflow
"""

    # Create the visual workflow
    visual_workflow = project_client.agents.create_version(
        agent_name="visual-multi-agent-storytelling-workflow",
        definition=WorkflowAgentDefinition(workflow=workflow_yaml),
    )

    print(f"✅ Visual Workflow Created!")
    print(f"   - ID: {visual_workflow.id}")
    print(f"   - Name: {visual_workflow.name}")
    print(f"   - Version: {visual_workflow.version}")
    print(f"   - This workflow should now appear in the Microsoft Foundry portal under 'Workflows' section")
    
    return visual_workflow, storytelling_agents, coordinator_agent

async def run_visual_workflow(workflow):
    """Execute the visual workflow"""
    print(f"\n🚀 Running Visual Workflow: {workflow.name}")
    
    # Get OpenAI client for running the workflow
    openai_client = project_client.get_openai_client()
    
    # Create conversation for the workflow
    conversation = openai_client.conversations.create()
    print(f"Created conversation (id: {conversation.id})")
    
    # Run the workflow with streaming
    user_input = "Write a story about a robot chef who discovers the secret ingredient to happiness"
    
    stream = openai_client.responses.create(
        conversation=conversation.id,
        extra_body={"agent": {"name": workflow.name, "type": "agent_reference"}},
        input=user_input,
        stream=True,
        metadata={"x-ms-debug-mode-enabled": "1"},
    )

    print(f"🎬 Executing workflow with prompt: '{user_input}'\n")
    
    # Process streaming events
    for event in stream:
        print(f"Event {event.sequence_number} type '{event.type}'", end="")
        if (
            event.type == ResponseStreamEventType.RESPONSE_OUTPUT_ITEM_ADDED
            or event.type == ResponseStreamEventType.RESPONSE_OUTPUT_ITEM_DONE
        ) and event.item.type == ItemType.WORKFLOW_ACTION:
            print(
                f": action ID '{event.item.action_id}' is '{event.item.status}' (previous: '{event.item.previous_action_id}')",
                end="",
            )
        print("", flush=True)

    # Clean up
    openai_client.conversations.delete(conversation_id=conversation.id)
    print("\n✅ Workflow execution completed!")

async def main():
    """Main execution function"""
    print("🎭 Creating Visual Multi-Agent Storytelling Workflow for Microsoft Foundry")
    print("=" * 80)
    
    try:
        # Create the visual workflow and agents
        workflow, agents, coordinator = await create_visual_workflow()
        
        print("\n" + "=" * 80)
        print("📊 SUMMARY:")
        print(f"✅ Created {len(agents)} storytelling agents")
        print(f"✅ Created 1 coordinator agent") 
        print(f"✅ Created 1 visual workflow")
        print(f"🌐 Workflow '{workflow.name}' should now be visible in Microsoft Foundry portal")
        print("=" * 80)
        
        # Optionally run the workflow
        run_workflow = input("\n🤔 Would you like to execute the workflow now? (y/n): ")
        if run_workflow.lower() in ['y', 'yes']:
            await run_visual_workflow(workflow)
            
        print(f"\n🎉 Visual Workflow Setup Complete!")
        print(f"👀 Check the Microsoft Foundry portal under 'Workflows' to see your visual workflow diagram")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())