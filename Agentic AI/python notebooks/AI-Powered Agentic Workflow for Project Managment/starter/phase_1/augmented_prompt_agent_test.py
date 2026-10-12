# Test script for AugmentedPromptAgent class

import os
from dotenv import load_dotenv
from workflow_agents.base_agents import AugmentedPromptAgent

# Load environment variables from .env file
load_dotenv()

# Retrieve OpenAI API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")

prompt = "What is the capital of France?"
persona = "You are a college professor; your answers always start with: 'Dear students,'"

# Instantiate the AugmentedPromptAgent with the API key and persona
augmented_agent = AugmentedPromptAgent(openai_api_key, persona)

# Send the prompt to the agent and store the result
augmented_agent_response = augmented_agent.respond(prompt)

# Print the agent's response
print(f"Prompt: {prompt}")
print(f"Response: {augmented_agent_response}")

print(f"Knowledge used: no external knowledge was supplied, so the agent answered from the\n" \
      f"general knowledge learned during the LLM's pretraining (that Paris is the capital of France).\n\n" \
      f"Persona effect: the system prompt told the model to act as a college professor, so the\n" \
      f"response opens with \"Dear students,\" and takes an explanatory, teaching tone. The persona\n" \
      f"changes the style and framing of the answer, not the underlying fact.")
