---
title: "Task Chaining – Flashcards"
type: flashcards
source: "[[Task Chaining]]"
created: 2026-09-25
tags:
  - flashcards
---

#flashcards/agentic-ai/task-chaining

What is task chaining?
?
Chaining at the level of subtasks, where each link may be an LLM call, a tool or API call, code, or a human step.

How does task chaining differ from prompt chaining?
?
Prompt chains link only LLM calls. Task chains link subtasks with any executor.

What is an executor in a task chain?
?
The component that performs a link: an LLM, a code function, an API/tool, or a human.

In what order should you prefer executors?
?
Code, then API/tool, then LLM, then human: the cheapest one that can do the link reliably.

Why does moving a link from an LLM to code raise end-to-end reliability?
?
Code links have p ≈ 1, so they no longer reduce the product of step success rates.

What is a state object in a task chain?
?
A typed record (e.g. a Pydantic model) passed along and updated by each link.

Why must side-effecting links be idempotent?
?
Retries or resumes may run them again, which would duplicate records or charges.

What is the saga (compensation) pattern?
?
Defining undo actions so a chain that fails partway can reverse the side effects already done.
