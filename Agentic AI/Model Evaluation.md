---
title: "Model Evaluation"
aliases:
  - ML Model Evaluation
  - Evaluation Metrics
course: Agentic AI (Cd14526) – Course 1
level: 300 / Graduate
type: study-guide
status: review
created: 2026-09-25
prerequisites:
  - "[[Artificial Intelligence]]"
related:
  - "[[LLM Evaluation]]"
  - "[[Output Validation]]"
  - "[[Large Language Models]]"
  - "[[AI Reliability]]"
  - "[[Chain-of-Thought and ReAct]]"
tags:
  - evaluation/metrics
  - machine-learning
  - study-guide
---

# Model Evaluation

> [!abstract] TL;DR
> Model evaluation is the general machine-learning practice of estimating how well a model will perform on **unseen data**. It uses held-out splits, suitable metrics and uncertainty estimates. ==A metric only counts if it matches the real cost of errors and is measured on data the model has never seen.== [[LLM Evaluation]] applies these foundations to generative models, where outputs are open-ended and labels are costly.

**Prerequisites:** [[Artificial Intelligence]]
**Related:** [[LLM Evaluation]] · [[Output Validation]] · [[Large Language Models]] · [[AI Reliability]]

> [!note] Source scope
> Linked from [[LLM Evaluation]], [[Large Language Models]] and [[Chain-of-Thought and ReAct]] as the general ML foundation. The content is standard ML material (*beyond the lecture*).

> [!todo]- Contents
> - [[#1. Core Concepts]]
> - [[#2. Classification Metrics]]
> - [[#3. Other Task Metrics]]
> - [[#4. Uncertainty and Significance]]
> - [[#5. Worked Example – Ticket Classifier]]
> - [[#6. Pitfalls and Failure Modes]]
> - [[#7. Key Takeaways]]
> - [[#8. Critical Analysis]]
> - [[#9. Self-Test]]
> - [[#10. Glossary]]
> - [[#Further Reading]]

---

## 1. Core Concepts

> [!info]+ Definition – Generalization error
> The expected loss on new data drawn from the deployment distribution. We estimate it from a held-out **test set** that is never used to make training or design decisions.

^def-generalization

| Split | Used for | Rule |
|---|---|---|
| Train | Fitting parameters | — |
| Validation / dev | Tuning hyperparameters, prompts, thresholds | Can be reused, but it overfits slowly |
| Test | The final estimate | Look at it **once** |
| Cross-validation | Small datasets | Rotate the k folds |

> [!warning] Leakage
> If any test information shapes the model (duplicates, future data, prompt tuning on test cases), the estimate is optimistic. In LLMs, **benchmark contamination** is one form of leakage ([[Large Language Models]]).

^leakage

---

## 2. Classification Metrics

|  | Predicted + | Predicted − |
|---|---|---|
| **Actual +** | TP | FN |
| **Actual −** | FP | TN |

$$
\text{Precision}=\frac{TP}{TP+FP}\quad
\text{Recall}=\frac{TP}{TP+FN}\quad
F_1=\frac{2PR}{P+R}\quad
\text{Accuracy}=\frac{TP+TN}{N}
$$

^classification-metrics

| Metric | Use when |
|---|---|
| Accuracy | Classes are balanced and errors cost the same |
| Precision | False positives are costly (e.g. automatic account credits) |
| Recall | Misses are costly (e.g. outage detection, safety) |
| F1 / macro-F1 | Imbalanced classes, one summary number |
| ROC-AUC / PR-AUC | Ranking quality independent of threshold. Prefer PR-AUC when positives are rare |
| Calibration (ECE) | Confidence scores drive decisions ([[Gate Checks]] thresholds) |

---

## 3. Other Task Metrics

| Task | Metrics |
|---|---|
| Regression | MAE, RMSE, $R^2$ |
| Retrieval / ranking | Recall@k, MRR, nDCG ([[Vector Databases]]) |
| Generation (reference-based) | Exact match, BLEU/ROUGE (weak), BERTScore |
| Generation (reference-free) | LLM-as-judge, human rating, faithfulness ([[LLM Evaluation]]) |
| Agents | Task success rate, steps and cost per task, tool-call accuracy |

---

## 4. Uncertainty and Significance

A metric from $n$ test items is an estimate. For a proportion $\hat p$, the 95% confidence interval is roughly:

$$
\hat p \pm 1.96\sqrt{\frac{\hat p(1-\hat p)}{n}}
$$

With $\hat p = 0.85$ and $n=200$ this is $\pm 0.049$. **Two prompts scoring 85% and 88% on 200 items are not clearly different.** Use paired tests (McNemar, bootstrap) when comparing systems on the same items.

---

## 5. Worked Example – Ticket Classifier

Outage vs non-outage on 1,000 tickets (100 real outages). The model flags 120: 90 true outages and 30 false alarms.

- Precision $= 90/120 = 0.75$. Recall $= 90/100 = 0.90$. $F_1 \approx 0.82$.
- Accuracy $= (90 + 870)/1000 = 0.96$. This looks great, but a model that *always* says "no outage" gets 0.90.
- Decision: missing an outage costs far more than a false alarm, so optimize recall and set a precision floor. Tune the threshold on the dev split, then report on the test split.

---

## 6. Pitfalls and Failure Modes

| Failure | Symptom | Mitigation |
|---|---|---|
| Accuracy on imbalanced data | High score, useless model | Precision, recall, PR-AUC, baseline comparison |
| Test-set reuse | Scores go up, production doesn't | Keep the test set locked, refresh it |
| Distribution shift | Offline and online disagree | Evaluate on recent production samples, monitor |
| No confidence intervals | Chasing noise | Report CIs, use paired tests |
| Wrong metric | Optimizing something nobody cares about | Tie the metric to business cost |
| Averages hide failures | Minority group fails | Slice metrics by segment |

---

## 7. Key Takeaways

- [ ] Keep train, dev and test separate. Test is used once.
- [ ] Choose precision or recall according to what errors cost.
- [ ] Accuracy misleads on imbalanced data. Always compare to a baseline.
- [ ] Report confidence intervals. Small differences on small sets are noise.
- [ ] Slice metrics by segment and watch for distribution shift.

---

## 8. Critical Analysis

- **Transfer to LLMs.** Classic evaluation assumes a fixed label space and i.i.d. data. LLM outputs are open-ended, and the input distribution changes with the prompt, so LLM-as-judge and human evaluation carry most of the load. They bring their own biases (position, verbosity, self-preference).
- **Benchmarks vs your task.** Leaderboard gains often don't carry over to domain tasks. Build a small, high-quality eval set from your own data.
- **At scale.** Continuous evaluation (sampled production traffic, drift monitors) replaces one-off test runs.
- **Security.** Adversarial evaluation (red-teaming, injection suites) is a separate axis from average-case accuracy.

> [!question] Discussion
> 1. How many labelled items do you need to detect a 3-point improvement with 95% confidence?
> 2. When is a calibrated 80%-accurate model better than an uncalibrated 85% one?

---

## 9. Self-Test

> [!question]- Q1. Why is the test set used only once?
> Repeated use leaks information into design choices, which biases the estimate upward.

> [!question]- Q2. Quantitative – TP=40, FP=10, FN=20. Give precision, recall and F1.
> P $=0.80$, R $\approx 0.667$, F1 $\approx 0.727$.

> [!question]- Q3. Quantitative – 95% CI for 90% accuracy on n = 100
> $0.9 \pm 1.96\sqrt{0.09/100} = 0.9 \pm 0.059$.

> [!question]- Q4. Design – evaluate an LLM ticket router before launch
> Label ~500 recent tickets (stratified). Measure per-class precision and recall, and a confusion matrix. Compare against the current rules as a baseline. Report CIs, slice by channel and region, and shadow-deploy before switching.

> [!tip] Flashcards
> Review with [[Model Evaluation - Flashcards]].

---

## 10. Glossary

| Term | Meaning |
|---|---|
| Held-out set | Data not used for training or tuning |
| Confusion matrix | Table of TP, FP, FN, TN |
| Calibration | Whether confidence scores match observed accuracy |
| Distribution shift | Deployment data differs from evaluation data |
| McNemar test | Paired significance test for two classifiers |

---

## Further Reading

- [scikit-learn – Model evaluation](https://scikit-learn.org/stable/modules/model_evaluation.html)
- [HELM: Holistic Evaluation of Language Models (Liang et al.)](https://arxiv.org/abs/2211.09110)
- [Judging LLM-as-a-Judge (Zheng et al., 2023)](https://arxiv.org/abs/2306.05685)
