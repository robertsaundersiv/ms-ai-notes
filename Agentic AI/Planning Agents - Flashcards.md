---
title: "Planning Agents – Flashcards"
type: flashcards
source: "[[Planning Agents]]"
created: 2026-09-24
tags:
  - flashcards
---

#flashcards/agentic-ai/planning-agents

What is a planning agent?
?
An agent that writes an explicit plan (steps or a DAG), executes it with tools, monitors outcomes, and revises the plan when needed.

How does a planning agent differ from ReAct?
?
ReAct picks one action at a time from the latest observation. A planning agent commits to a plan first and re-plans on mismatch.

What are the steps of the plan-execute-replan loop?
?
Plan → verify → (approve) → execute step → observe → compare with expectation → continue, re-plan, or finish.

What are the benefits of explicit plans?
?
Coherence on long tasks, lower cost (strong planner, cheap executors), parallelism, and human review/audit.

How is re-planning like Model Predictive Control?
?
Both use a receding horizon: plan ahead, execute the next step, observe, and re-plan from the new state.

What is LLM-Modulo?
?
The LLM proposes plans and external sound verifiers or solvers check them.

What did PlanBench-style studies find?
?
LLMs often produce invalid plans on formal planning tasks, so plans need verification.

What should plan verification check?
?
Tools exist, args are valid, dependencies are acyclic, no forbidden actions, write steps are flagged for approval, and the plan is within budget.

How do you prevent re-plan loops?
?
Cap re-plans and budget, then escalate to a human.
