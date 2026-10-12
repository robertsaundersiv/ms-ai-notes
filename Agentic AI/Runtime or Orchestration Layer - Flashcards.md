---
title: "Runtime or Orchestration Layer – Flashcards"
type: flashcards
source: "[[Runtime or Orchestration Layer]]"
created: 2026-09-27
tags:
  - flashcards
---

#flashcards/agentic-ai/orchestration-layer

What is the orchestration layer of a chain?
?
The code or framework that executes the chain: it picks the next step, passes state, runs gates, handles errors, enforces budgets and logs everything.

What is the split between prompts and the orchestration layer?
?
Prompts say what each step produces. The orchestrator decides when and how steps run.

What separates a chain from an agent in orchestration terms?
?
Who picks the next step. Code picks in a chain. The LLM picks in an agent, and the orchestrator only enforces limits.

What is durable execution?
?
Persisting state after each step so a crashed or paused run can resume from the last completed step.

Why check budgets before each step rather than after?
?
So the run stops before spending more, instead of discovering the overrun after it has happened.

What happens to failures in a well-built runtime?
?
Every failure ends in a visible destination, such as a human queue or an alert. Nothing is silently dropped.

What should each trace span record?
?
Run ID, step, attempt, executor, input, output, gate verdicts, tokens and latency, plus prompt, model and code versions.

With per-turn finish probability s and a cap of N turns, what fraction of runs hit the cap?
?
(1 − s)^N, assuming independent turns.

When should you move from plain code to an orchestration framework?
?
When you need persistence, parallelism or human-in-the-loop pauses.

Why is the orchestrator the trust boundary against prompt injection?
?
Injected text can change what the model proposes, but only the runtime decides what executes, so permissions and approvals are enforced there.
