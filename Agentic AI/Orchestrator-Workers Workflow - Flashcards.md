---
title: "Orchestrator-Workers Workflow – Flashcards"
course: Agentic AI (Cd14526) – Course 1
type: flashcards
source: "[[Orchestrator-Workers Workflow]]"
created: 2026-09-28
---

#flashcards/agentic-ai/workflow-patterns/orchestrator-workers

Flashcards for [[Orchestrator-Workers Workflow]].

What is the orchestrator-workers workflow?
?
A pattern in which a central LLM dynamically breaks a task into subtasks, delegates them to worker LLMs or agents, and combines their outputs into a final result.

What are the three roles in orchestrator-workers?
?
The orchestrator (plans and delegates), the workers (each executes one subtask), and the synthesizer (combines the results).

What is the defining difference between orchestrator-workers and parallelization?
?
In parallelization, code fixes the subtasks in advance. In orchestrator-workers, an LLM decides the subtasks at runtime for each input.

When should you not use orchestrator-workers?
?
When you can list the subtasks in code before seeing the input. Use chaining or parallelization instead.

Which building-block agent acts as the orchestrator?
?
The Action Planning Agent.

What checks should a plan gate run?
?
Valid JSON with a subtask list, workers from a closed allowed set, a subtask count within the cap, an instruction for every subtask, and valid dependencies with no cycles.

Why should the worker set be closed?
?
So the planner can't invent workers, and injected text can't create a new actor with new permissions.

How many LLM calls does a single round with k subtasks take?
?
k + 2: one plan call, k worker calls, and one synthesis call.

What sets latency when subtasks have dependencies?
?
The critical path: the longest chain of dependent calls in the plan's DAG.

What is the end-to-end success probability if all k subtasks must succeed?
?
About p_plan × p_w^k × p_synth.

Plan 0.9, each worker 0.95, synthesizer 0.95, k = 5. What is the success probability?
?
About 0.9 × 0.774 × 0.95 ≈ 0.66.

Why is capping the number of subtasks a reliability control as well as a cost control?
?
Success falls as p_w^k, so fewer required subtasks means fewer chances for one to fail.

What should the synthesizer do about failed subtasks?
?
Report which subtasks failed instead of hiding them, cite subtask ids for its claims, and flag contradictions between workers.

What is the single point of failure in orchestrator-workers?
?
The planner. If the plan misses a subtask, perfect workers still produce an incomplete answer.

What is over-decomposition, and how do you limit it?
?
Splitting a task into far more subtasks than needed, which multiplies cost. Limit it with a subtask cap and a prompt that asks for the fewest subtasks that cover the task.

Why is the retail router's pricing route not orchestrator-workers?
?
Its sub-steps are fixed in code. No LLM decides which subtasks to run, so it is routing with context gathering.
