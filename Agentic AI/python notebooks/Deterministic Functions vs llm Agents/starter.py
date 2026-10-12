"""
Program Management Knowledge Agent - Starter Code

This program demonstrates two approaches to answering program management questions:
1. Using hardcoded knowledge
2. Using an LLM API

Complete the TODOs to build your knowledge agent.
"""

from openai import OpenAI
import os

# Initialize the OpenAI client only if an API key is available
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(
    base_url="https://openai.vocareum.com/v1",
    api_key=api_key
) if api_key else None

MODEL = "gpt-4o-mini"

def get_hardcoded_answer(question):
    """
    Return answers to program management questions using hardcoded knowledge.

    Args:
        question (str): The question about program management

    Returns:
        str: The answer to the question
    """
    # Convert question to lowercase for easier matching
    q = question.lower()

    # Responses for common program management questions, keyed by trigger keywords
    knowledge_base = [
        (("gantt",),
         "A Gantt chart is a horizontal bar chart that shows a project schedule: "
         "tasks are listed on the vertical axis and time on the horizontal axis, "
         "with bars showing each task's start date, duration, and dependencies."),
        (("agile",),
         "Agile is an iterative approach to project management that delivers work "
         "in small, incremental releases, emphasizing collaboration, customer "
         "feedback, and adapting to change over following a fixed plan."),
        (("sprint",),
         "A sprint is a fixed, short time-box (usually 1-4 weeks) in Scrum during "
         "which the team commits to completing a set of backlog items and produces "
         "a potentially shippable increment."),
        (("critical path",),
         "The critical path is the longest sequence of dependent tasks in a project. "
         "It determines the shortest possible project duration; any delay to a "
         "task on the critical path delays the whole project."),
        (("milestone",),
         "A milestone is a significant point or event in a project, such as the "
         "completion of a key deliverable or phase. Milestones have zero duration "
         "and are used to track progress."),
        (("stakeholder",),
         "A stakeholder is any person or group who is affected by, or can affect, "
         "a project, such as sponsors, customers, team members, and end users."),
        (("scope creep",),
         "Scope creep is the uncontrolled expansion of a project's scope without "
         "corresponding adjustments to time, cost, or resources."),
    ]

    for keywords, answer in knowledge_base:
        if any(keyword in q for keyword in keywords):
            return answer

    # Default response for questions not in the knowledge base
    return ("I don't have information about that in my knowledge base. "
            "Try asking about Gantt charts, Agile, sprints, critical path, "
            "milestones, stakeholders, or scope creep.")

def get_llm_answer(question):
    """
    Get answers to program management questions using an LLM API.

    Args:
        question (str): The question about program management

    Returns:
        str: The answer from the LLM
    """
    # Check if the LLM client is initialized
    if client is None:
        return "LLM unavailable: set the OPENAI_API_KEY environment variable."

    # Call the LLM with a system message that sets its role
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system",
                 "content": "You are an expert program manager. Answer program "
                            "management questions clearly and concisely in 2-4 sentences."},
                {"role": "user", "content": question},
            ],
            temperature=0.3,
        )
        content = response.choices[0].message.content
        return content.strip() if content else "LLM returned an empty response."
    except Exception as e:
        return f"Error calling LLM API: {e}"

# Demo function to compare both approaches
def compare_answers(question):
    """Compare answers from both approaches for a given question."""
    print(f"\nQuestion: {question}")
    print("-" * 50)

    # Get and display the hardcoded answer
    print("Hardcoded answer:")
    print(get_hardcoded_answer(question))
    print()

    # Get and display the LLM answer (or a placeholder message)
    print("LLM answer:")
    print(get_llm_answer(question))

    print("=" * 50)

# Demo with sample questions
if __name__ == "__main__":
    print("PROGRAM MANAGEMENT KNOWLEDGE AGENT DEMO")
    print("=" * 50)

    # Sample program management questions
    questions = [
        "What is a Gantt chart?",
        "How does Agile methodology work?",
        "What is a sprint in Scrum?",
        "Why is the critical path important?",
        "What is a project milestone?",
        "How do I prioritize a product backlog?",  # not in the hardcoded knowledge base
    ]

    # Loop through the questions and compare answers
    for question in questions:
        compare_answers(question)
