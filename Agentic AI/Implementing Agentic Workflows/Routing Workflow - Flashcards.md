---
title: "Routing Workflow – Flashcards"
course: Agentic AI (Cd14526) – Course 1
type: flashcards
source: "[[Routing Workflow]]"
created: 2026-09-27
---

#flashcards/agentic-ai/workflow-patterns/routing

Flashcards for [[Routing Workflow]].

What is the routing pattern?
?
A workflow pattern that directs each incoming task or input to the processing path or specialized agent best suited to it, based on the nature of the input.

What analogy does the reading use for routing?
?
A mail sorting facility, where specialized routes make sure each piece of mail reaches the right destination quickly and correctly.

What are the four benefits of routing?
?
Task specialization, resource optimization, flexibility and adaptability, and scalability.

How does routing enable resource optimization?
?
It sends tasks to different LLMs by complexity, cost, and latency: faster, cheaper models for simple tasks and more powerful models for complex ones.

What are the two core stages of routing?
?
Classification and task dispatch.

What does the classification stage determine?
?
The input's type, category, intent, or complexity, so an informed decision can be made about how to handle it.

What does the task dispatch stage do?
?
It sends the classified input, with its label, to the appropriate specialized agent, prompt chain, function, or processing module.

Classification tells you what; what does dispatch tell you?
?
Where the task goes, based on its classification.

Why does the accuracy of the whole routing process depend on classification?
?
A misclassified task is sent to the wrong agent, leading to inefficiency or incorrect results.

What is rule-based classification?
?
Classification using predefined programmatic logic, such as keyword matching or conditional statements.

What is LLM-based classification?
?
Using an LLM to analyze the input and assign a category based on contextual understanding.

What factors decide between rule-based and LLM-based classification?
?
Input complexity, desired accuracy, and performance needs.

What makes a worker agent appropriate for a dispatched task?
?
Its designated expertise or capability matches the category assigned during classification.

What is routing with context gathering?
?
The router runs a short sub-sequence of calls (e.g. account lookup, document retrieval) to gather context before delegating to the final specialist.

Classifier accuracy 0.9 and specialist accuracy 0.95. What is end-to-end accuracy?
?
About 0.9 × 0.95 = 0.855, assuming misrouted tasks fail.

Why should a router have an "other" or fallback route?
?
So inputs that fit no category, or are classified with low confidence, go to a human or general agent instead of being forced into the wrong specialist.
