---
title: "Multi-Agent Systems – Flashcards"
type: flashcards
source: "[[Multi-Agent Systems]]"
created: 2026-09-24
tags:
  - flashcards
---

#flashcards/agentic-ai/multi-agent

What is a multi-agent system?
?
Two or more LLM agents, each with its own instructions, tools and state, cooperating through defined communication to complete a task.

Name five multi-agent coordination patterns.
?
Orchestrator–worker, pipeline/sequential, router/handoff, debate/critic, peer/swarm.

When does multi-agent help?
?
When subtasks are separable and benefit from context isolation, parallelism, specialization or separation of duties.

When does multi-agent hurt?
?
For tightly coupled tasks that need shared full context. Agents duplicate context and make conflicting decisions.

What should a delegation from an orchestrator include?
?
Objective, output format, scope/boundaries, and a stop condition or budget.

Why can a critic agent miss errors?
?
If it's the same model with similar context, it shares the generator's blind spots.

How does multi-agent affect cost?
?
It multiplies tokens (roughly agents × tokens each, plus overhead), often several times a single agent.

What is the main security risk in multi-agent systems?
?
Each agent is an injection entry point, and a compromised agent can instruct others. Treat inter-agent messages as untrusted and use per-agent least privilege.

What is the fair baseline for comparing a multi-agent system?
?
A strong single-agent system at an equal token budget.
