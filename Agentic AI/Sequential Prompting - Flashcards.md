---
title: "Sequential Prompting – Flashcards"
type: flashcards
source: "[[Sequential Prompting]]"
created: 2026-09-23
tags:
  - flashcards
---

#flashcards/agentic-ai/sequential-prompting

What is sequential prompting?
?
Running a task as separate prompts, where each takes the previous output and does one new thing with it.

When is sequential prompting useful?
?
When a single large prompt would overcomplicate the output, or when intermediate results need to be seen or checked.

What was the reading's sequential prompting example?
?
Research key concepts of AI agents, then summarize the research, then draft a LinkedIn post from the summary.

What are the main benefits of sequential prompting?
?
It mirrors human reasoning, focuses on one goal at a time, improves accuracy, and lets each prompt be improved on its own.

How does sequential prompting differ from Chain-of-Thought?
?
CoT puts reasoning steps inside one response. Sequential prompting uses separate prompts that can each be checked.

What turns sequential prompting into prompt chaining?
?
Code, instead of a human, passes each output into the next prompt.

What is the manual equivalent of a gate check in sequential prompting?
?
You reviewing each output before running the next step.

Why is the research step the riskiest in the LinkedIn example?
?
Without real sources the model recalls from memory and can hallucinate facts and sources, which then flow into every later step.

How do you prevent goal drift across steps?
?
Re-state the original goal in every step's prompt.

When should you use a new chat per step instead of one chat?
?
When a step must use only the previous output, to avoid context bloat and old content leaking in.

Three steps are each 90% reliable. What is the end-to-end reliability?
?
About 73% (0.9 cubed).

If step 2 of a sequence is weak, what do you change?
?
Only step 2's prompt. Refine it and rerun from there.
