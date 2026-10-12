---
title: "Output Validation – Flashcards"
type: flashcards
source: "[[Output Validation]]"
created: 2026-09-25
tags:
  - flashcards
---

#flashcards/agentic-ai/output-validation

What is output validation?
?
Runtime checks on each LLM output that accept, repair, or reject it before it reaches a user, the next chain step, or a tool.

What is the untrusted output principle?
?
Treat LLM output like untrusted user input. Never pass it to eval, SQL, a shell, or an API without checking it first.

What are the validation layers, from cheapest to most expensive?
?
Syntax/schema, then content/grounding, then logic/rules, then policy/safety, then judgment (LLM-as-judge or a human).

How does output validation differ from LLM evaluation?
?
Validation runs at runtime on a single output and returns accept, retry, or block. Evaluation runs offline over a dataset and returns metrics.

Why doesn't schema validation stop hallucinations?
?
It checks structure and types only. A made-up value of the right type still passes.

What is a grounding check? Give one example.
?
A check that a claim is supported by the source, e.g. requiring an evidence quote that appears verbatim in the input.

What property of a validator matters most for reducing escaped errors?
?
Its recall: the fraction of bad outputs it catches.

With p = 0.8 and validator recall 0.5 and no retries, what fraction of bad outputs escape?
?
(1 − 0.8) × (1 − 0.5) = 0.10, so 10%.

What should happen after the maximum number of retries?
?
Escalate to a fallback or a human, and log the failure. Never fail silently.
