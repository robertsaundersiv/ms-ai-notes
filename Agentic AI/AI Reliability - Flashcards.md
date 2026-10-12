---
title: "AI Reliability – Flashcards"
type: flashcards
source: "[[AI Reliability]]"
created: 2026-09-24
tags:
  - flashcards
---

#flashcards/agentic-ai/reliability

What is reliability for an LLM system?
?
The probability that it produces an acceptable result for the real input distribution over time, covering correctness, consistency, robustness, format, availability and calibration.

Why is reliability a property of the system, not the model?
?
The model is stochastic and fails silently. Validation, retries, fallbacks and monitoring around it decide how reliable the system is.

What is silent failure?
?
A wrong output that looks like a correct one, with no error raised.

What is the formula for chain success with n independent steps?
?
p^n

What is the end-to-end success of 5 steps at 0.95 each?
?
About 0.77.

How does a gate plus one retry change per-step success?
?
p_eff ≈ p + (1 − p) · d · p, where d is the gate's detection rate.

Why can retries fail to help?
?
Errors are often correlated with the input or prompt, so a plain retry repeats the mistake. Add feedback or vary the prompt or model.

Why do retried actions need idempotency?
?
So that retrying a tool call (e.g. a refund or email) doesn't cause duplicate side effects.

Why pin model versions?
?
Provider updates can silently change behavior. Pinning plus regression evals catches the change.

Name five reliability patterns.
?
Decomposition, structured output, gates, retry with feedback, fallbacks/circuit breakers, grounding, human in the loop, monitoring.
