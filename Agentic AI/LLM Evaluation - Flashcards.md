---
title: "LLM Evaluation – Flashcards"
type: flashcards
source: "[[LLM Evaluation]]"
created: 2026-09-24
tags:
  - flashcards
---

#flashcards/agentic-ai/llm-evaluation

What is an eval?
?
A repeatable test that runs a system on fixed inputs and scores outputs against defined criteria, so changes can be compared.

What is the difference between a benchmark and an application eval?
?
A benchmark compares general model capability. An application eval tests your system on your task and data.

What are the main grader types?
?
Exact/programmatic, reference-based (BLEU/ROUGE/embeddings), LLM-as-judge, human, and pairwise preference.

How do you validate an LLM judge?
?
Measure its agreement with human labels on a sample (e.g. Cohen's kappa) before trusting it.

Name three LLM-judge biases.
?
Position bias, verbosity (length) bias, and self-preference.

What is the standard error of accuracy on n items?
?
sqrt(p(1-p)/n). The 95% CI is about p ± 1.96·SE.

About how wide is the 95% CI for 85% accuracy on 50 items?
?
About ±10 percentage points, so small differences are noise.

Which statistical test compares two prompts on the same items?
?
A paired test such as McNemar's test.

What is the difference between pass@k and pass^k?
?
pass@k: at least one of k attempts succeeds. pass^k: all k succeed (≈ p^k). Production agents need pass^k.

What four things should you evaluate for an agent?
?
Outcome/final state, trajectory (tools and order), efficiency (cost, steps), and safety (e.g. injection resistance).

What is benchmark contamination?
?
Test items leaked into training data, which inflates scores.

How are gate checks related to evals?
?
A gate is a per-request eval with a pass/fail threshold, and it can reuse the same grader.
