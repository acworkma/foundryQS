import os
import asyncio
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    WorkflowAgentDefinition,
    ResponseStreamEventType,
    ItemType
)

load_dotenv()

# Configuration
PROJECT_ENDPOINT = os.environ["PROJECT_ENDPOINT"]

print(f"Using PROJECT_ENDPOINT: {PROJECT_ENDPOINT}")

project_client = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
)

async def create_fixed_visual_workflow():
    """Create a corrected visual workflow with proper agent name references"""
    
    print("🔧 Creating corrected visual workflow with matching agent names...")

    # Define the CORRECTED visual workflow YAML with proper agent names
    workflow_yaml = """
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

    # Invoke DeepSeek Storyteller (CORRECTED AGENT NAME)
    - kind: InvokeAzureAgent
      id: deepseek_storyteller
      description: "DeepSeek creates a sci-fi story"
      conversationId: "=Local.DeepSeekConversationId"
      agent:
        name: agent-deepseek
      input:
        messages: "=Local.UserPrompt"
      output:
        messages: Local.DeepSeekStory

    # Invoke GPT Storyteller (CORRECTED AGENT NAME)
    - kind: InvokeAzureAgent
      id: gpt_storyteller
      description: "GPT creates a character-driven story"
      conversationId: "=Local.GPTConversationId"
      agent:
        name: agent-gpt
      input:
        messages: "=Local.UserPrompt"
      output:
        messages: Local.GPTStory

    # Invoke Mistral Storyteller (CORRECTED AGENT NAME)
    - kind: InvokeAzureAgent
      id: mistral_storyteller
      description: "Mistral creates an adventure story"
      conversationId: "=Local.MistralConversationId"
      agent:
        name: agent-mistral
      input:
        messages: "=Local.UserPrompt"
      output:
        messages: Local.MistralStory

    # Coordinator evaluates all stories (CORRECTED AGENT NAME)
    - kind: InvokeAzureAgent
      id: story_coordinator
      description: "Coordinator evaluates and selects the best story"
      conversationId: "=Local.CoordinatorConversationId"
      agent:
        name: agent-coordinator
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

    try:
        # Create the corrected visual workflow
        visual_workflow = project_client.agents.create_version(
            agent_name="visual-multi-agent-storytelling-workflow-fixed",
            definition=WorkflowAgentDefinition(workflow=workflow_yaml),
        )

        print(f"✅ CORRECTED Visual Workflow Created!")
        print(f"   - ID: {visual_workflow.id}")
        print(f"   - Name: {visual_workflow.name}")
        print(f"   - Version: {visual_workflow.version}")
        print(f"   - This corrected workflow should now appear in the Microsoft Foundry portal")
        print(f"   - Agent names now match your deployed agents:")
        print(f"     • agent-deepseek ✅")
        print(f"     • agent-gpt ✅")
        print(f"     • agent-mistral ✅") 
        print(f"     • agent-coordinator ✅")
        
        return visual_workflow

    except Exception as e:
        print(f"❌ Error creating workflow: {e}")
        print("💡 Common causes:")
        print("   1. One or more agents don't exist - run individual agent scripts first")
        print("   2. Agent names don't match exactly")
        print("   3. Model deployments not available")
        raise

async def test_workflow_execution(workflow):
    """Test the corrected workflow execution"""
    print(f"\n🚀 Testing Corrected Visual Workflow: {workflow.name}")
    
    try:
        # Get OpenAI client for running the workflow
        openai_client = project_client.get_openai_client()
        
        # Create conversation for the workflow
        conversation = openai_client.conversations.create()
        print(f"Created conversation (id: {conversation.id})")
        
        # Run the workflow with a test prompt
        user_input = "Write a story about a robot chef who discovers the secret ingredient to happiness"
        
        print(f"Sending input: {user_input}")
        
        # Test with streaming to see execution progress
        stream = openai_client.responses.create(
            conversation=conversation.id,
            extra_body={"agent": {"name": workflow.name, "type": "agent_reference"}},
            input=user_input,
            stream=True,
        )
        
        print("\n📡 Workflow Execution Stream:")
        full_response = ""
        
        for event in stream:
            if event.type == ResponseStreamEventType.RESPONSE_DELTA:
                if hasattr(event, 'delta') and hasattr(event.delta, 'content'):
                    content = event.delta.content
                    print(content, end='', flush=True)
                    full_response += content
            elif event.type == ResponseStreamEventType.RESPONSE_DONE:
                print(f"\n\n✅ Workflow Execution Completed!")
                break
                
        return full_response
        
    except Exception as e:
        print(f"❌ Workflow execution failed: {e}")
        print("\n🔍 Troubleshooting steps:")
        print("1. Verify all agents exist by running individual agent scripts")
        print("2. Check model deployments are available")
        print("3. Verify Azure credentials and permissions")
        print("4. Test individual agents before workflow")
        raise

async def verify_agents_exist():
    """Verify all required agents exist before running workflow"""
    print("\n🔍 Verifying required agents exist...")
    
    try:
        # List all agents
        agents = project_client.agents.list()
        agent_names = [agent.name for agent in agents.data if hasattr(agents, 'data') and agents.data]
        
        required_agents = ["agent-deepseek", "agent-gpt", "agent-mistral", "agent-coordinator"]
        missing_agents = []
        
        for required_agent in required_agents:
            if required_agent in agent_names:
                print(f"   ✅ {required_agent}")
            else:
                print(f"   ❌ {required_agent} (MISSING)")
                missing_agents.append(required_agent)
        
        if missing_agents:
            print(f"\n⚠️  Missing agents: {missing_agents}")
            print("Run the corresponding agent scripts first:")
            for missing in missing_agents:
                print(f"   python {missing}.py")
            return False
        else:
            print("✅ All required agents exist!")
            return True
            
    except Exception as e:
        print(f"❌ Error checking agents: {e}")
        return False

async def main():
    """Main execution function"""
    print("🔧 Microsoft Foundry Visual Workflow Fix Tool")
    print("=" * 50)
    
    # Step 1: Verify agents exist
    if not await verify_agents_exist():
        print("\n❌ Cannot proceed - missing required agents")
        print("Please run the individual agent scripts first, then try again.")
        return
    
    # Step 2: Create corrected workflow
    workflow = await create_fixed_visual_workflow()
    
    # Step 3: Test workflow execution
    print("\n" + "=" * 50)
    response = await test_workflow_execution(workflow)
    
    print("\n" + "=" * 50)
    print("🎉 Workflow troubleshooting complete!")
    print(f"The corrected workflow '{workflow.name}' should now execute properly in the Microsoft Foundry portal.")

if __name__ == "__main__":
    asyncio.run(main())