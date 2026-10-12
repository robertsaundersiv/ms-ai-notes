---
title: "CoT prompt Samples – Flashcards"
type: flashcards
source: "[[CoT prompt Samples]]"
created: 2026-09-25
tags:
  - flashcards
---

#flashcards/agentic-ai/cot-samples

What is Chain-of-Thought prompting?
?
Prompting a model to produce intermediate reasoning steps before its final answer.

What is the classic zero-shot CoT trigger phrase?
?
"Let's think step by step."

What is structured CoT?
?
CoT with named output fields (e.g. facts, reasoning, answer), so the answer can be parsed and validated.

How does self-consistency work?
?
Sample several reasoning paths at non-zero temperature and take a majority vote on the final answer.

Why should arithmetic in CoT prompts be moved to code?
?
LLMs make arithmetic slips even when the method is right. Code is exact.

Is CoT text a faithful explanation of the model's computation?
?
Not reliably. It helps accuracy, but the stated steps may not be what caused the answer.

What does low agreement in self-consistency suggest?
?
The question is ambiguous or badly specified, so escalate or clarify.

What is plan-then-solve?
?
The model writes a numbered plan first, then carries out each step before giving the answer.
