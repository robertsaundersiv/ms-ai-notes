---
title: "Task Decomposition – Flashcards"
type: flashcards
source: "[[Task Decomposition]]"
created: 2026-09-25
tags:
  - flashcards
---

#flashcards/agentic-ai/task-decomposition

What is task decomposition?
?
Splitting a goal into subtasks and saying how they depend on each other (a sequence, tree, or DAG), so that finishing all of them achieves the goal.

What three things should a good subtask have?
?
One verb, one output, one success test.

How do you calculate the end-to-end success rate of n steps in series?
?
Multiply the step success rates: P = p1 × p2 × … × pn.

What is the difference between static and dynamic decomposition?
?
In static decomposition a developer writes the plan at design time. In dynamic decomposition the LLM writes the plan at runtime (planning agents).

A monolithic prompt succeeds 70% of the time. Is 3 steps at 0.95 each better?
?
Yes. 0.95³ ≈ 0.86.

What is over-decomposition?
?
Splitting so finely that the extra steps and lost context lower end-to-end reliability.

Which subtasks should be done in code rather than by an LLM?
?
Deterministic ones: lookups, arithmetic, and fixed routing rules.

What is least-to-most prompting?
?
Solving easier sub-questions first and using their answers to solve harder ones.
