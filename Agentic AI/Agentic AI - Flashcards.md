---
title: "Agentic AI – Flashcards"
course: Agentic AI (Cd14526) – Course 1
type: flashcards
source: "[[Agentic AI]]"
created: 2026-09-23
---

#flashcards/agentic-ai/foundations

Flashcards for [[Agentic AI]].

What is agentic AI?
?
AI systems that autonomously pursue goals over multi-step tasks: planning, acting through tools, observing outcomes, and adapting, with limited direct supervision.

What is agenticness?
?
The degree to which a system can adaptably achieve complex goals in complex environments with limited direct supervision. It is a spectrum, not a binary.

How does agentic AI differ from an AI agent?
?
An AI agent is the system (model, tools, memory, loop). Agentic AI is the paradigm and property: how much autonomy is exercised, and how it is designed and governed.

What are the four agentic design patterns?
?
Reflection, tool use, planning, and multi-agent collaboration.

What is the core autonomy design principle?
?
Grant the minimum autonomy that solves the task, because each level adds cost, variance, attack surface, and evaluation difficulty.

Which task properties favor less agency?
?
Known, stable steps; high volume; hard-to-verify success; costly or irreversible errors; tight latency or cost budgets.

Name the governance practices for agentic systems (after Shavit et al., 2023).
?
Evaluate suitability, constrain the action space and require approval, set default behaviors, legibility, automatic monitoring, attributability, and interruptibility.

Why does prompt-injection risk grow with autonomy?
?
More untrusted content, more tools, and fewer human checkpoints mean an injected instruction has more ways to cause impact.

What trend did METR (2025) report about agent time horizons?
?
The length of tasks frontier agents complete at 50% reliability has been doubling roughly every 7 months. It is a reported trend, not a law.

What question exposes agent-washing?
?
Who decides the next step: the code or the model?
