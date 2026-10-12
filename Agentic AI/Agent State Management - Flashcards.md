---
title: "Agent State Management – Flashcards"
type: flashcards
source: "[[Agent State Management]]"
created: 2026-10-03
tags:
  - flashcards
---

#flashcards/agentic-ai/agent-state

What does it mean that an LLM is stateless?
?
Each call is independent. The model keeps no record of earlier prompts and knows only what is in the current input.

If LLMs are stateless, how does a chat appear to remember earlier turns?
?
The application resends the message history with every call. The state lives in the surrounding code, not the model.

What is the difference between a stateless and a stateful system?
?
A stateless system treats every request on its own. A stateful system tracks what has happened, at least for the duration of a task, and uses it to decide what comes next.

How does an online checkout illustrate a stateful system?
?
It remembers the items in the cart, where you are in the purchase process, and your payment details, then uses them at checkout to compute the total.

What is agent state?
?
Everything an LLM-based agent tracks while working on a task: the user query, system instructions, message history, tool calls and intermediate results.

What does it mean that agent state is ephemeral?
?
It exists only while the task runs and is discarded at the end, unless you deliberately persist it.

Is ephemeral agent state more like working memory or long-term memory, and why?
?
Working memory. It holds only what the agent needs to solve the current task, not what it should remember across sessions.

What is a state machine?
?
A system that moves between well-defined steps, updating internal variables as it goes, where the next step can depend on the current values.

What contract does every step in a state-machine agent follow?
?
It receives the current state object and returns an updated state object with the same schema.

What are the steps of the basic agent execution loop?
?
Start with empty state, prepare system and user messages, call the LLM, check for tool calls. If there are tool calls, execute them, add the results to state and call the LLM again. Otherwise return the final message and stop.

What does a conditional transition do in an agent state machine?
?
It inspects the current state and chooses the next step, for example going to tool execution only if the LLM selected tools.

In a state-machine agent, what does the LLM decide and what does code decide?
?
The LLM decides whether tools are needed by writing tool calls into state. Code reads the state and decides which step runs next.

Why define the state with a typed schema?
?
So every step agrees on the same fields and types, making data flow between steps clear and consistent.

Why should the tool-execution step clear pending tool calls after running them?
?
Otherwise the router sees them again and re-runs the same tools, causing duplicate side effects or an infinite loop.

Why does the basic execution loop need a step or token budget?
?
The only exit is the LLM choosing not to call tools. A model that keeps requesting tools would loop forever without a second exit condition.

Why does resending the full message history make long agent runs expensive?
?
Each call resends everything so far, so total input tokens grow roughly quadratically with the number of loop iterations.

In what sense is a state-machine agent deterministic, and in what sense is it not?
?
Control flow is deterministic given a state, so it is predictable and testable. The LLM's outputs are stochastic, so different runs can reach different states and take different paths.

What does checkpointing state after every step make possible?
?
Resuming a crashed or paused run from its last completed step, including pausing for human approval.

Why is tool output stored in agent state a security concern?
?
It is fed back into the next prompt, so instructions hidden in tool results can act as prompt injection.

What are the main benefits of structuring an agent as a state machine?
?
It is modular, predictable, testable and debuggable, because each step can be tested alone and every intermediate state can be inspected.
