# agentic_workflow.py

import os
import re
from dotenv import load_dotenv
from workflow_agents.base_agents import ActionPlanningAgent, KnowledgeAugmentedPromptAgent, EvaluationAgent, RoutingAgent

load_dotenv()


openai_api_key = os.getenv("OPENAI_API_KEY")

# load the product spec from the same folder as this script, so it runs from any working directory
spec_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Product-Spec-Email-Router.txt")
with open(spec_path, "r", encoding="utf-8") as f:
    product_spec = f.read()

# Instantiate all the agents

# Action Planning Agent
knowledge_action_planning = (
    "Stories are defined from a product spec by identifying a "
    "persona, an action, and a desired outcome for each story. "
    "Each story represents a specific functionality of the product "
    "described in the specification. \n"
    "Features are defined by grouping related user stories. \n"
    "Tasks are defined for each story and represent the engineering "
    "work required to develop the product. \n"
    "A development Plan for a product contains all these components"
)

action_planning_agent = ActionPlanningAgent(openai_api_key=openai_api_key, knowledge=knowledge_action_planning)

# Product Manager - Knowledge Augmented Prompt Agent
persona_product_manager = "You are a Product Manager, you are responsible for defining the user stories for a product."
knowledge_product_manager = (
    "Stories are defined by writing sentences with a persona, an action, and a desired outcome. "
    "The sentences always start with: As a "
    "Write several stories for the product spec below, where the personas are the different users of the product. "
    f"{product_spec}"
)

product_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key=openai_api_key, persona=persona_product_manager, knowledge=knowledge_product_manager)

# Product Manager - Evaluation Agent

evaluation_criteria = (
    "The answer should be stories that follow the following structure: As a [type of user], I want [an action or feature] so that [benefit/value]."
)
persona_product_manager_eval = "You are an evaluation agent that checks the answers of other worker agents."
product_manager_evaluation_agent = EvaluationAgent(worker_agent=product_manager_knowledge_agent, max_interactions=5, openai_api_key=openai_api_key, persona=persona_product_manager_eval, evaluation_criteria=evaluation_criteria)


# Program Manager - Knowledge Augmented Prompt Agent
persona_program_manager = "You are a Program Manager, you are responsible for defining the features for a product."
knowledge_program_manager = "Features of a product are defined by organizing similar user stories into cohesive groups."

program_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key=openai_api_key, persona=persona_program_manager, knowledge=knowledge_program_manager)


# Program Manager - Evaluation Agent
persona_program_manager_eval = "You are an evaluation agent that checks the answers of other worker agents."


pm_evaluation_criteria = ("The answer should be product features that follow the following structure: " \
                        "Feature Name: A clear, concise title that identifies the capability\n" \
                        "Description: A brief explanation of what the feature does and its purpose\n" \
                        "Key Functionality: The specific capabilities or actions the feature provides\n" \
                        "User Benefit: How this feature creates value for the user")
program_manager_evaluation_agent = EvaluationAgent(worker_agent=program_manager_knowledge_agent, max_interactions=5, openai_api_key=openai_api_key, persona=persona_program_manager_eval, evaluation_criteria=pm_evaluation_criteria)


# Development Engineer - Knowledge Augmented Prompt Agent
persona_dev_engineer = "You are a Development Engineer, you are responsible for defining the development tasks for a product."
knowledge_dev_engineer = "Development tasks are defined by identifying what needs to be built to implement each user story."
development_engineer_knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key=openai_api_key, persona=persona_dev_engineer, knowledge=knowledge_dev_engineer)

# Development Engineer - Evaluation Agent
persona_dev_engineer_eval = "You are an evaluation agent that checks the answers of other worker agents."

development_engineer_evaluation_criteria = ("The answer should be tasks following this exact structure: " \
                     "Task ID: A unique identifier for tracking purposes\n" \
                     "Task Title: Brief description of the specific development work\n" \
                     "Related User Story: Reference to the parent user story\n" \
                     "Description: Detailed explanation of the technical work required\n" \
                     "Acceptance Criteria: Specific requirements that must be met for completion\n" \
                     "Estimated Effort: Time or complexity estimation\n" \
                     "Dependencies: Any tasks that must be completed first")
development_engineer_evaluation_agent = EvaluationAgent(worker_agent=development_engineer_knowledge_agent, max_interactions=5, openai_api_key=openai_api_key, persona=persona_dev_engineer_eval, evaluation_criteria=development_engineer_evaluation_criteria)

# Collected results for each section of the final project plan
project_plan = {
    "User Stories": [],
    "Product Features": [],
    "Engineering Tasks": [],
}


def with_context(step, output_format, *section_names):
    """Attach the required output format and earlier sections of the plan to a step, so
    each role answers in its evaluator's structure and builds on the previous results
    (features group the actual user stories; tasks reference the actual stories)."""
    query = f"{step}\n\nWrite your answer in this exact format: {output_format}"
    context = "\n\n".join(
        f"{name}:\n" + "\n\n".join(project_plan[name])
        for name in section_names
        if project_plan[name]
    )
    if context:
        query += f"\n\nBase your answer on these results from earlier steps:\n\n{context}"
    return query


# Routing Agent

agents = [
    {
        "name": "Product Manager",
        "description": "Responsible for defining product personas and user stories only. Does not define features or tasks. Does not group stories.",
        "func": lambda x: product_manager_support_function(with_context(x, evaluation_criteria))
    },
    {
        "name": "Program Manager",
        "description": "Responsible for defining product features by grouping related user stories. Does not define user stories or development tasks.",
        "func": lambda x: program_manager_support_function(with_context(x, pm_evaluation_criteria, "User Stories"))
    },
    {
        "name": "Development Engineer",
        "description": "Responsible for defining the engineering and development tasks needed to implement each user story. Does not define user stories or features.",
        "func": lambda x: development_engineer_support_function(
            with_context(x, development_engineer_evaluation_criteria, "User Stories", "Product Features")
        )
    }
]
routing_agent = RoutingAgent(openai_api_key=openai_api_key, agents=agents)

# Job function persona support functions


def product_manager_support_function(query):
    """Have the Product Manager evaluation agent produce validated user stories for a step."""
    result = product_manager_evaluation_agent.evaluate(query)["final_response"]
    project_plan["User Stories"].append(result)
    return result


def program_manager_support_function(query):
    """Have the Program Manager evaluation agent produce validated product features for a step."""
    result = program_manager_evaluation_agent.evaluate(query)["final_response"]
    project_plan["Product Features"].append(result)
    return result


def development_engineer_support_function(query):
    """Have the Development Engineer evaluation agent produce validated engineering tasks for a step."""
    result = development_engineer_evaluation_agent.evaluate(query)["final_response"]
    project_plan["Engineering Tasks"].append(result)
    return result


# Run the workflow

print("\n*** Workflow execution started ***\n")
# Workflow Prompt
# ****
workflow_prompt = (
    "Create a complete development plan for the Email Router product: "
    "define the user stories, group the user stories into product features, "
    "and define the engineering tasks for each user story."
)
# ****
print(f"Task to complete in this workflow, workflow prompt = {workflow_prompt}")

print("\nDefining workflow steps from the workflow prompt")
extracted_lines = action_planning_agent.extract_steps_from_prompt(workflow_prompt)

# The planner sometimes drafts sub-items under each step; route only the numbered
# top-level steps so each role runs once. Fall back to every line if none are numbered.
workflow_steps = [line for line in extracted_lines if re.match(r"^\d+[.)]", line)] or extracted_lines
print("Workflow steps:")
for step in workflow_steps:
    print(f"  {step}")

completed_steps = []
for step_number, step in enumerate(workflow_steps, start=1):
    print(f"\n{'=' * 80}\nStep {step_number}/{len(workflow_steps)}: {step}\n{'=' * 80}")
    result = routing_agent.route(step)
    completed_steps.append(result)
    print(f"\nResult of step {step_number}:\n{result}")

# Print the consolidated project plan, one labelled section per role
print(f"\n{'#' * 80}\n# EMAIL ROUTER PROJECT PLAN\n{'#' * 80}")
for section_name, section_results in project_plan.items():
    print(f"\n{'=' * 80}\n{section_name.upper()}\n{'=' * 80}")
    if section_results:
        print("\n\n".join(section_results))
    else:
        print("(No step in the action plan was routed to this role.)")
