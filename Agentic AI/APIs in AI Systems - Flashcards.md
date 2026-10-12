---
title: "APIs in AI Systems – Flashcards"
type: flashcards
source: "[[APIs in AI Systems]]"
created: 2026-10-05
tags:
  - flashcards
---

#flashcards/agentic-ai/apis

What are the three roles APIs play in an AI agent?
?
The model API (reasoning), tool APIs (fresh data and actions), and memory APIs (persisting and retrieving knowledge across runs).

Does the model call tool APIs itself?
?
No. It proposes a structured tool call. The orchestrator validates it, makes the real API call with its own credentials, and returns the result.

What does it mean that a model API is stateless?
?
It keeps no memory between requests, so every request must include all the context the model needs.

How does a stateless model API connect to agent state management?
?
The agent's state, especially the message history, becomes the payload of each request. Managing state largely means deciding what goes into that payload.

Why does resending the full history make long conversations expensive?
?
Each request includes every earlier turn, so total input tokens grow roughly quadratically with the number of calls.

Why put stable content such as the system prompt and tool schemas at the start of a request?
?
Prompt caching discounts a repeated prefix, so keeping the unchanging parts first maximizes cache hits.

What does server-side conversation state change, and what does it not change?
?
It changes where the state is stored (with the provider instead of the client). State still exists, and you trade control and data retention for smaller payloads.

What does the model actually see of a tool API?
?
Only the tool's name, description and argument schema. Credentials and the real endpoint stay in the orchestrator's code.

Why expose narrow, task-shaped tools instead of a generic HTTP tool?
?
Narrow tools are easier for the model to use correctly and limit what a mistaken or manipulated model can reach.

Why trim API responses before adding them to agent state?
?
Everything in state is resent to the model, so raw responses inflate cost, consume context and distract the model.

Why should tool errors be returned as data rather than raised?
?
The model can read the error and correct its call, and the agent loop keeps running instead of crashing.

Why must API keys never be stored in agent state?
?
State is sent to the model provider and written to logs and traces, so keys would leak and could be echoed out through injection.

How do memory APIs bridge ephemeral state and long-term memory?
?
Retrieval calls seed the state with relevant memories at the start of a run, and write calls store durable facts from the final state before it is discarded.

What API calls typically implement memory retrieval?
?
Embedding the query, then a similarity search in a vector database, or a key lookup for stored facts and preferences.

What is the tradeoff between orchestrator-driven and model-driven memory?
?
Orchestrator-driven memory is predictable and testable but may retrieve irrelevant items. Memory exposed as a tool lets the model choose, but is less predictable and makes memory writes an injection target.

Why is it useful to model each API call as its own state-machine step?
?
You get a snapshot of state before and after every external interaction, which makes failures in external services traceable.

What is idempotency, and why does it matter for retrying API calls?
?
An idempotent operation has the same effect if repeated. Retrying a non-idempotent write, such as sending an email, can duplicate it unless you use idempotency keys or a confirmation gate.

With per-call success p and r retries on independent failures, what is per-call success?
?
1 − (1 − p)^(r+1).

Why don't retries fix an agent that keeps calling a tool with the wrong arguments?
?
Retries only help independent, transient failures. A systematic misunderstanding repeats every time, so the fix is a clearer description or feeding the validation error back.

Why is every tool API response a security risk?
?
It is pasted into the next prompt, so instructions hidden in it can act as prompt injection. Treat it as untrusted data and keep authorization decisions in code.

How can memory APIs persist an attack across sessions?
?
If injected content gets written to memory as a "fact", it is retrieved and trusted in later runs. Gate memory writes and record where each memory came from.

What problem does the Model Context Protocol solve for tool APIs?
?
It standardizes how tools and resources are exposed, so any compatible client can use any compatible server without custom integration code.

Why is the model often called the least reliable API in an agent?
?
It is stochastic and its behaviour shifts across versions, unlike documented deterministic services, so deterministic validation and routing code should surround it.
