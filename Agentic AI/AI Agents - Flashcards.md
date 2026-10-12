---
title: "AI Agents – Flashcards"
course: Agentic AI (Cd14526) – Course 1
type: flashcards
source: "[[AI Agents]]"
created: 2026-09-23
---

#flashcards/agentic-ai/agents

Flashcards for [[AI Agents]].

What is an agent in classical AI (Russell & Norvig)?
?
Anything that perceives its environment through sensors and acts on it through actuators to achieve goals.
<!--SR:!2026-09-24,1,230-->

What is an LLM agent?
?
A system where an LLM, in a loop, decides which tool calls to make based on observations until the goal is complete or a limit is hit.
<!--SR:!2026-09-24,1,230-->

What is the key difference between a workflow and an agent?
?
In a workflow, predefined code controls the flow. In an agent, the LLM decides the flow at runtime.
<!--SR:!2026-09-24,1,230-->

What are the core components of an LLM agent?
?
Model, instructions, tools, memory, knowledge/retrieval, planning, runtime/orchestrator, and guardrails.
<!--SR:!2026-09-24,1,230-->

Why must an agent runtime enforce stop conditions?
?
Without them, agents can loop indefinitely, drift, or blow the budget. Typical stop conditions are task complete, max steps, token budget, repeated failures, and human interrupt.
<!--SR:!2026-09-24,1,230-->

How does per-step reliability compound over an n-step trajectory?
?
Success ≈ p^n. For example, 0.98^50 ≈ 0.36.
<!--SR:!2026-09-26,3,250-->

Why does agent token cost grow super-linearly with the number of steps?
?
Each step re-sends the growing context: total ≈ nT0 + Δ·n(n+1)/2.
<!--SR:!2026-09-24,1,230-->

Why enforce limits on irreversible actions in the runtime instead of the prompt?
?
Prompt instructions are probabilistic and injectable. Runtime checks are deterministic.
<!--SR:!2026-09-24,1,230-->

What is a good hybrid design for many business agents?
?
A fixed workflow for the common path, with the agent used only for exceptions.
<!--SR:!2026-09-24,1,230-->

Name three common LLM agent architectures.
?
ReAct, plan-and-execute, reflection (Reflexion), orchestrator-workers, computer-use, and coding agents (any three).
<!--SR:!2026-09-24,1,230-->

