---
title: "Prompt Chaining for Agentic Reasoning – Flashcards"
course: Agentic AI (Cd14526) – Course 1
type: flashcards
source: "[[Prompt Chaining for Agentic Reasoning - Study Guide]]"
created: 2026-09-22
---

#flashcards/agentic-ai/prompt-chaining

Flashcards for [[Prompt Chaining for Agentic Reasoning - Study Guide]].

What is prompt chaining?
?
Splitting a task into sequential LLM calls, where each call's output feeds the next.

What is a gate in a prompt chain?
?
A programmatic or LLM check between chain steps that validates the output before the chain continues.

What does the routing pattern do?
?
A classifier step selects which specialized downstream chain handles the input.

What is the map-reduce pattern?
?
Apply one prompt to many chunks (map), then synthesize the results with a second prompt (reduce).

What is the orchestrator-workers pattern?
?
An LLM dynamically creates subtasks, delegates them to worker calls, and synthesizes the results. Unlike parallelization, the subtasks are not known in advance.

What is the evaluator-optimizer pattern?
?
A generator/evaluator feedback loop that repeats until the criteria are met or an iteration cap is reached.

What is goal drift?
?
A chain gradually optimizing away from the original intent, because each step optimizes for the previous step's output.

How does chain reliability scale with length?
?
$P = p^n$. Reliability drops exponentially, so five 95% steps give about 77%.

Parallelization vs. orchestrator-workers: what's the key difference?
?
In parallelization, code predefines the subtasks. In orchestrator-workers, the LLM decides the subtasks at runtime.

Why re-inject the original user request into later chain steps?
?
It prevents context loss (dropped constraints) and goal drift.
