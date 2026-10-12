---
title: "CoT prompt Samples"
aliases:
  - Chain-of-Thought Prompt Samples
  - CoT Samples
course: Agentic AI (Cd14526) – Course 1
level: 300 / Graduate
type: study-guide
status: review
created: 2026-09-25
prerequisites:
  - "[[Chain-of-Thought and ReAct]]"
  - "[[Few-Shot Prompting]]"
related:
  - "[[ReAct prompt Samples]]"
  - "[[Prompt Engineering]]"
  - "[[Output Validation]]"
  - "[[Tree-of-Thought]]"
tags:
  - prompt-engineering/cot
  - prompt-samples
  - agentic-ai
  - study-guide
---

# CoT prompt Samples

> [!abstract] TL;DR
> This is a set of reusable **Chain-of-Thought** prompt templates, the companion to [[ReAct prompt Samples]]. CoT asks the model to reason step by step *before* answering. It can be zero-shot ("think step by step"), few-shot (worked examples), or structured (named reasoning fields). ==In production, put the reasoning and the final answer in separate fields, so that code parses the answer and the reasoning is only kept for debugging.==

**Prerequisites:** [[Chain-of-Thought and ReAct]] · [[Few-Shot Prompting]]
**Related:** [[ReAct prompt Samples]] · [[Prompt Engineering]] · [[Output Validation]] · [[Tree-of-Thought]]

> [!note] Source scope
> The theory is in [[Chain-of-Thought and ReAct#Chain-of-Thought]]. These samples were written for this vault (*beyond the lecture*). Device names, numbers and policies are **fictional**. IP addresses use documentation ranges.

> [!todo]- Contents
> - [[#1. CoT Variants at a Glance]]
> - [[#2. Sample 1 – Zero-Shot CoT]]
> - [[#3. Sample 2 – Few-Shot CoT – Billing Proration]]
> - [[#4. Sample 3 – Structured CoT – Outage Triage]]
> - [[#5. Sample 4 – Self-Consistency]]
> - [[#6. Sample 5 – Plan-then-Solve]]
> - [[#7. Pitfalls and Failure Modes]]
> - [[#8. Key Takeaways]]
> - [[#9. Critical Analysis]]
> - [[#10. Self-Test]]
> - [[#Further Reading]]

---

## 1. CoT Variants at a Glance

> [!info]+ Definition – Chain-of-Thought prompting
> Prompting a model to produce intermediate reasoning steps before its final answer. This improves performance on multi-step arithmetic, logic and planning tasks.

^def-cot

| Variant | Trigger | Best for |
|---|---|---|
| Zero-shot CoT | "Let's think step by step." | Quick gains, no examples to hand |
| Few-shot CoT | 2–4 worked examples with reasoning | Domain-specific reasoning patterns |
| Structured CoT | Named fields: `facts`, `reasoning`, `answer` | Production and parsing |
| Self-consistency | Sample $k$ reasoning paths, majority vote | Tasks with a single correct answer |
| Plan-then-solve | Write a plan first, then carry it out | Multi-part problems ([[Task Decomposition]]) |

---

## 2. Sample 1 – Zero-Shot CoT

```text
A customer's plan is 500 Mbps. Speed tests at 3 locations show 480, 210, and 470 Mbps.
The 210 result was on Wi-Fi 2.4 GHz; the others were wired.
Is there evidence of a network-side problem?

Let's think step by step, then give a one-line answer starting with "ANSWER:".
```

*Why it works:* the trigger phrase makes the model reason about the confounding factor (Wi-Fi band) before it concludes. The `ANSWER:` prefix makes the answer easy to parse.

---

## 3. Sample 2 – Few-Shot CoT – Billing Proration

```text
You calculate prorated charges. Show your reasoning, then the final amount.

Q: Plan $60/month (30-day cycle). Customer upgraded to $90 on day 11. Charge for the cycle?
Reasoning: Days 1–10 at $60 → 10/30 × 60 = $20.00. Days 11–30 = 20 days at $90 → 20/30 × 90 = $60.00. Total = $80.00.
Answer: $80.00

Q: Plan $75/month (30-day cycle). Customer downgraded to $45 on day 21. Charge for the cycle?
Reasoning: Days 1–20 at $75 → 20/30 × 75 = $50.00. Days 21–30 = 10 days at $45 → 10/30 × 45 = $15.00. Total = $65.00.
Answer: $65.00

Q: Plan $50/month (30-day cycle). Customer upgraded to $80 on day 16. Charge for the cycle?
Reasoning:
```

> [!warning] Compute, don't ask
> This is a teaching example. In production, **do the arithmetic in code** and use the LLM only to pull out the dates and plans ([[Output Validation]], [[Task Chaining]]). Expected answer: $15/30×50 + 15/30×80 = \$65.00$.

---

## 4. Sample 3 – Structured CoT – Outage Triage

```text
You are a NOC triage assistant. Given alarms and tickets, decide whether this is a
single-customer issue or a wider outage.

Respond ONLY with JSON:
{
  "facts": [ "<fact taken verbatim from the input>", ... ],
  "reasoning": "<step-by-step reasoning using only the facts>",
  "scope": "single_customer" | "node" | "olt" | "regional",
  "confidence": 0.0-1.0
}

Rules:
- Every fact must be quoted from the input.
- If fewer than 3 tickets share a node, scope cannot be "node" or wider.

INPUT:
Alarms: OLT-7 PON 3 LOS at 02:14. OLT-7 PON 4 normal.
Tickets: #881 (Node-12, no sync 02:15), #882 (Node-12, offline 02:16),
#883 (Node-12, offline 02:20), #890 (Node-40, slow Wi-Fi 09:00).
```

*Why it works:* `facts` is the grounding step, checked by a [[Output Validation|grounding gate]]. `reasoning` gets kept for audit. `scope` is an enum that a Pydantic model checks, and the rule is written so it can also be checked in code.

---

## 5. Sample 4 – Self-Consistency

```python
answers = [parse_answer(llm(cot_prompt, temperature=0.8)) for _ in range(5)]
final, votes = Counter(answers).most_common(1)[0]
if votes < 3:            # low agreement → escalate
    route_to_human()
```

Cost grows linearly with $k$. Agreement is a rough confidence signal: if 5 independent samples split 2/2/1, the question is ambiguous or badly specified.

---

## 6. Sample 5 – Plan-then-Solve

```text
First, write a numbered PLAN of the steps needed to answer the question.
Then carry out each step under "EXECUTION", referencing the step number.
Finally, give "ANSWER:" on its own line.

Question: Which of our three uplink options gives the lowest cost per Mbps over a
3-year term, including one-time install fees?
Option A: 1 Gbps, $900/mo, $2,000 install. Option B: 2 Gbps, $1,500/mo, $5,000 install.
Option C: 10 Gbps, $5,200/mo, $0 install.
```

(Answer: 36-month cost per Mbps is A ≈ \$34.4, B ≈ \$29.5, C ≈ \$18.7. **C** is lowest.)

---

## 7. Pitfalls and Failure Modes

| Failure | Symptom | Mitigation |
|---|---|---|
| Unfaithful reasoning | Plausible steps that don't cause the answer | Don't treat CoT as an explanation. Validate the answer on its own |
| Arithmetic slips | Wrong totals despite correct method | Do the maths in code or a calculator tool |
| Answer buried in prose | Parse failures | Structured fields or an `ANSWER:` prefix |
| Few-shot pattern copying | Model copies the example numbers | Vary the examples, check against the input |
| Cost and latency | Long outputs | Use CoT only where accuracy gains justify it. Reasoning models may not need explicit CoT |

---

## 8. Key Takeaways

- [ ] Zero-shot, few-shot, structured, self-consistency and plan-then-solve are the core CoT patterns.
- [ ] Always separate reasoning from a parseable final answer.
- [ ] Ground the reasoning in quoted facts, and validate them.
- [ ] Hand arithmetic to code.
- [ ] Use agreement across samples as a rough confidence signal.

---

## 9. Critical Analysis

- **Faithfulness.** Research shows that CoT text does not always reflect the model's actual computation. It is useful for accuracy, but it is not a reliable explanation.
- **Model generation.** Reasoning-tuned models reason internally. Explicit CoT prompts can add little or even hurt. Re-benchmark when you change models ([[Model Evaluation]]).
- **Security.** Reasoning traces can leak system-prompt or sensitive context. Don't show raw reasoning to end users by default.

> [!question] Discussion
> When would you log the CoT but hide it from the user, and when would you drop it entirely?

---

## 10. Self-Test

> [!question]- Q1. What makes structured CoT better for production than free-form CoT?
> The answer sits in a parseable field that can be validated. The facts can be grounding-checked, and the reasoning is kept apart for audit.

> [!question]- Q2. Quantitative – self-consistency with k = 5 at 400 output tokens each. How many tokens compared with one call?
> 2,000 output tokens, 5× the cost of a single call.

> [!question]- Q3. Design – write a CoT prompt to decide whether a credit request meets policy
> Structured fields: `policy_clauses_cited` (quoted), `facts` (from the ticket), `reasoning`, `eligible: bool`, `amount`. The amount is checked in code against the policy cap.

> [!tip] Flashcards
> Review with [[CoT prompt Samples - Flashcards]].

---

## Further Reading

- [Chain-of-Thought Prompting (Wei et al., 2022)](https://arxiv.org/abs/2201.11903)
- [Large Language Models are Zero-Shot Reasoners (Kojima et al., 2022)](https://arxiv.org/abs/2205.11916)
- [Self-Consistency (Wang et al., 2022)](https://arxiv.org/abs/2203.11171)
- [Plan-and-Solve Prompting (Wang et al., 2023)](https://arxiv.org/abs/2305.04091)
