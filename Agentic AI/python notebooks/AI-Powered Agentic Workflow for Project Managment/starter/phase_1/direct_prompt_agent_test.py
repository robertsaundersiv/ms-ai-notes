# Test script for DirectPromptAgent class

import os
from dotenv import load_dotenv
from workflow_agents.base_agents import DirectPromptAgent

# Load environment variables from .env file
load_dotenv()

# Retrieve OpenAI API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")

prompt = "What is the Capital of France?"

# Instantiate the DirectPromptAgent
direct_agent = DirectPromptAgent(openai_api_key)

# Send the prompt to the agent and store the response
direct_agent_response = direct_agent.respond(prompt)

# Print the response from the agent
print(f"Prompt: {prompt}")
print(f"Response: {direct_agent_response}")

# Explain the source of the knowledge used to answer
print(
    "\nKnowledge source: the DirectPromptAgent sends the prompt straight to gpt-3.5-turbo "
    "with no system prompt, persona, or supplied knowledge, so the answer comes solely "
    "from the general knowledge the LLM learned during pretraining."
)
