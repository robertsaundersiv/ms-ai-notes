---
title: "Agentic Workflow Modeling – Flashcards"
course: Agentic AI (Cd14526) – Course 1
type: flashcards
source: "[[Agentic Workflow Modeling]]"
created: 2026-09-27
---

#flashcards/agentic-ai/workflow-modeling

Flashcards for [[Agentic Workflow Modeling]].

What is agentic workflow modeling?
?
Designing the blueprint for a team of AI agents that work together to complete a complex job: what each agent does, how they connect, and how the system adapts to change.

What is deterministic automation?
?
A process that follows a fixed script with the same steps in the same order, such as an email auto-responder or a simple data-processing routine.

What happens when you first replace each step of a deterministic process with an agent?
?
The result is still essentially deterministic: agents do what they're told in the order they're told. That is an acceptable starting point.

What is generalization in agentic workflow design?
?
Making the system handle more types of tasks and find smarter ways to do them without reprogramming every detail, for example by adding a planning agent, tools, and decision-making.

When is deterministic automation all you need?
?
When you only need to execute one specific, unchanging process efficiently.

How does an agentic workflow differ from a conversational chatbot?
?
A workflow has a defined start and end and aims to complete a job. A chatbot continues until the user stops.

What two strengths keep agentic workflows from being rigid?
?
They can reflect and iterate on their own or others' work, and they can find different paths (sequences of actions) to a goal.

What does process-centric (deterministic) workflow modeling specify?
?
Tasks, their sequence and dependencies, inputs and outputs, simple rule-based decision points, visualized as a flowchart.

What six elements does agent-centric workflow modeling define?
?
Agent capabilities, goal structure, decision-making frameworks, adaptation rules, environment constraints, and feedback loops.

What three things were added to generalize the code assistant example?
?
A planning capability (understand different coding question types), access to tools (code-example KB, validator, web search), and decision-making power (answer, use a tool, or ask for clarification).

What does a Knowledge Augmented Prompt Agent do?
?
It uses a defined persona and a specific, curated knowledge base to answer, and is instructed to ignore the LLM's general knowledge.

What does a RAG Knowledge Prompt Agent do?
?
It dynamically retrieves relevant information from a large dataset before answering, which makes it flexible and less prone to making things up.

What does an Evaluation Agent do?
?
It acts as a quality controller: it assesses other agents' output against criteria and can prompt revisions.

What does a Routing Agent do?
?
It acts as the project manager, directing each incoming task to the most suitable specialized agent.

What does an Action Planning Agent do?
?
It takes a complex goal and breaks it into a sequence of smaller, executable steps.

How do the building-block agents differ from the four spectrum agent types?
?
The spectrum types classify agents by how they manage the LLM's context. The building blocks classify them by the job they do in the workflow; routing, evaluation, and planning are roles that can be built at different spectrum levels.

Router accuracy 0.9, specialist accuracy 0.8, perfect evaluator, 3 attempts. What is the success rate?
?
One pass is 0.72; with 3 attempts it is 1 − 0.28³ ≈ 0.98. Real evaluators and correlated retries lower this.
