---
title: "Implementing Agentic Workflows in Python – Flashcards"
course: Agentic AI (Cd14526) – Course 1
type: flashcards
source: "[[Implementing Agentic Workflows in Python]]"
created: 2026-09-27
---

#flashcards/agentic-ai/workflow-implementation

Flashcards for [[Implementing Agentic Workflows in Python]].

What are the two main paths for building AI agents in practice?
?
Using an existing agent framework with pre-built components, or building the core logic from scratch with Python and an LLM directly.

What is the main benefit of building agents from scratch?
?
Maximum control and deep insight into how agents work and work together, at the cost of more effort.

What three layers make up an agentic system in Python?
?
LLM models (the engine), agent logic and prompting (custom Python behavior and prompts), and workflow orchestration (connecting agents).

Why should the LLM layer be swappable?
?
So different or newer models can be connected without rewriting the system, keeping it adaptable as new models emerge.

What does workflow orchestration handle?
?
The sequence of operations, the flow of information between agents, and the overall execution of multi-agent processes.

What three code concerns does the reading separate?
?
Agent definitions (classes in a module), agent instantiation (creating and configuring objects), and workflow implementation (sequence and data passing between agents).

Why put agent class definitions in their own module?
?
It separates what agents are from how they're configured and wired together, so definitions can be reused and tested independently of any one workflow.

Why organize agent code as an importable package?
?
So the workflow code can import agent definitions cleanly, keeping definitions, instantiation and orchestration in separate files.

Why should a base agent class define an abstract execute method that subclasses must override?
?
It sets one common interface every specialized agent must implement, and it fails loudly if a subclass forgets to.

Where should an agent be customized for its specific role?
?
At instantiation, through constructor configuration such as its data source or the fields it handles, not by writing a new class for each variation.

How should a workflow handle a step that fails partway through?
?
Return a structured error status and stop, so later steps never run on missing data.

What is the main limitation of the reading's fetch-and-process example as an agentic system?
?
It uses no LLM and makes no decisions; the agents are deterministic functions wrapped in classes.

Why give every agent the same interface, taking shared state in and returning updated state?
?
The orchestrator can treat every agent the same way, so a workflow becomes a list of agents and can grow into routing or DAG execution without changing agent code.

How do you make agents independent of a specific LLM provider?
?
Define an LLM client interface, write a small adapter per provider, and inject the client into agents at instantiation.

What are the total latency and success rate of sequential agents?
?
Latency is the sum of the step latencies; success rate is the product of the step success rates (assuming independence).
