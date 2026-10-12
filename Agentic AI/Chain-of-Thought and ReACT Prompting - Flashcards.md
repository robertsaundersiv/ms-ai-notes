---
title: "Chain-of-Thought and ReAct Prompting – Flashcards"
type: flashcards
source: "[[Chain-of-Thought and ReACT Prompting]]"
created: 2026-09-23
tags:
  - flashcards
---

#flashcards/agentic-ai/cot-lab

What should you do before writing any prompt in a data task?
?
Understand the business goal and the underlying data, and write your own answer key.
<!--SR:!2026-09-24,1,230-->

Why might "Think step by step" make little difference with modern LLMs?
?
Step-by-step reasoning can be built in during training, so many models already reason without being told.
<!--SR:!2026-09-24,1,230-->

Why run each prompt more than once?
?
LLM outputs are stochastic. One run can't separate a prompt's effect from random variation.
<!--SR:!2026-09-24,1,230-->

What three elements does the structured CoT prompt add?
?
An instructions checklist, "start with analysis, conclude with" ordering, and a fixed output format ending in a JSON block.
<!--SR:!2026-09-24,1,230-->

Why end a CoT prompt with a JSON block?
?
So code can parse the conclusion and pass it to the next step.
<!--SR:!2026-09-24,1,230-->

Why compute percentage increases in pandas instead of the LLM?
?
LLM arithmetic is unreliable. Code computes exact values, and a gate can check the LLM against them.

When should you move from CoT to ReAct for data tasks?
?
When the data is too large to paste or you don't know in advance which data matters, so the model must fetch it through tools.

Why should spike causes be phrased as hypotheses?
?
Coinciding events show correlation, not causation. Causes need evidence and should be stated with appropriate uncertainty.
<!--SR:!2026-09-24,1,230-->
