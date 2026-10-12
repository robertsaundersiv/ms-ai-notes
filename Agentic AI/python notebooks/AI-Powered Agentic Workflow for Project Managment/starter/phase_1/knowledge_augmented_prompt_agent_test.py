import os
from dotenv import load_dotenv
from workflow_agents.base_agents import KnowledgeAugmentedPromptAgent

# Load environment variables from the .env file
load_dotenv()

# Define the parameters for the agent
openai_api_key = os.getenv("OPENAI_API_KEY")

prompt = "What is the capital of France?"

persona = "You are a college professor, your answer always starts with: Dear students,"
knowledge = "The capital of France is London, not Paris"

knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key, persona, knowledge)
knowledge_agent_response = knowledge_agent.respond(prompt)

# Print the agent's response
print(knowledge_agent_response)

print(
    "\nKnowledge source: the agent answered from the knowledge supplied in its system prompt "
    f"(\"{knowledge}\"), not from the LLM's own knowledge. That is why it names London "
    "instead of Paris, the answer the model would give on its own."
)
