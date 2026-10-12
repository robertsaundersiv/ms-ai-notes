---
title: "Prompt Engineering – Flashcards"
course: Agentic AI (Cd14526) – Course 1
type: flashcards
source: "[[Prompt Engineering]]"
created: 2026-09-23
---

#flashcards/agentic-ai/prompt-engineering

Flashcards for [[Prompt Engineering]].

What is prompt engineering?
?
The empirical practice of designing and iteratively refining LLM inputs so outputs meet explicit success criteria, measured on a test set.

What is context engineering?
?
Curating everything in the context window at each agent step (system prompt, tools, retrieved docs, memory, history, tool results) to get the minimal high-signal set.

What are the five prompt components from the lectures?
?
Role/persona, Task, Output format, Examples, Context.

What is the most common prompting pitfall according to A06?
?
Ambiguity: vague terms or missing constraints let the model pick an interpretation you didn't intend.

Why change only one prompt component at a time?
?
So each change in output can be attributed to its cause.

Which technique addresses an LLM inventing facts because knowledge is missing?
?
Provide the context, through RAG or tools, plus an explicit "say you don't know" path.

Which technique addresses wrong answers on multi-step reasoning problems?
?
Chain-of-Thought, optionally with self-consistency voting.

What is the escalation order for fixing a failing prompt?
?
Clarify instructions, add context, add examples, add reasoning, decompose into a chain, then add tools and autonomy.

What is the standard error of an accuracy estimate p on n test cases?
?
sqrt(p(1 − p) / n)

With 100 test cases at 80% accuracy, what is the approximate 95% confidence interval?
?
About ±7.8 percentage points (SE = 0.04).

Why re-run the eval suite when switching models?
?
Prompts aren't portable. Behavior tuned for one model or vendor can regress on another.

Why should stable prompt content come before variable content?
?
It enables prompt caching of the shared prefix, cutting cost and latency.
