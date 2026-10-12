---
title: "Model Evaluation – Flashcards"
type: flashcards
source: "[[Model Evaluation]]"
created: 2026-09-25
tags:
  - flashcards
---

#flashcards/agentic-ai/model-evaluation

What is generalization error?
?
Expected loss on new data from the deployment distribution, estimated using a held-out test set.

What are the formulas for precision and recall?
?
Precision = TP / (TP + FP). Recall = TP / (TP + FN).

When should you optimize recall?
?
When misses are costly, e.g. outage detection or safety issues.

Why is accuracy misleading on imbalanced data?
?
A trivial majority-class model scores high. With 10% positives, always predicting negative gives 90%.

What is leakage? Give an LLM example.
?
Test information influencing the model or design. Benchmark contamination is an LLM example.

What is the approximate 95% confidence interval for a proportion?
?
p ± 1.96 · sqrt(p(1 − p) / n).

What is calibration?
?
Whether a model's confidence scores match its observed accuracy.

Which test compares two classifiers on the same items?
?
A paired test such as McNemar's or a paired bootstrap.
