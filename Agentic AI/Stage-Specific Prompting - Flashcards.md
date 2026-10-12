---
title: "Stage-Specific Prompting – Flashcards"
type: flashcards
source: "[[Stage-Specific Prompting]]"
created: 2026-09-25
tags:
  - flashcards
---

#flashcards/agentic-ai/stage-specific-prompting

What is stage-specific prompting?
?
Giving each stage of a chain its own tuned prompt and settings, matched to that stage's single job.

What is minimal sufficient context?
?
Giving a stage only the inputs it needs from earlier stages, not the full history.

What should an extraction stage's temperature and format be?
?
Temperature 0 with a strict JSON schema, and every value quoted from the input or null.

Why use a different model or rubric for the review stage?
?
A reviewer that is the same model with the same prompt tends to rubber-stamp the generator's mistakes.

Why shouldn't the generation stage see raw source documents?
?
It should use facts that have passed validation. This cuts hallucination, cost, and prompt-injection exposure.

Which stage parameters can be tuned?
?
Role, instructions, examples, output format, temperature, model, and gate.

How does stage-specific prompting relate to task decomposition?
?
Decomposition decides what the stages are. Stage-specific prompting decides how each stage is instructed.

What is the risk of tuning one stage's prompt on its own?
?
Downstream regressions, so run end-to-end evals after every change.
