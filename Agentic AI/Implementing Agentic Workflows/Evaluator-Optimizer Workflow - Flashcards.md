---
title: "Evaluator-Optimizer Workflow – Flashcards"
course: Agentic AI (Cd14526) – Course 1
type: flashcards
source: "[[Evaluator-Optimizer Workflow]]"
created: 2026-09-27
---

#flashcards/agentic-ai/workflow-patterns/evaluator-optimizer

Flashcards for [[Evaluator-Optimizer Workflow]].

What is the evaluator-optimizer workflow?
?
A workflow pattern that improves output quality through an iterative cycle of generation, critique, and refinement.

What problem does the evaluator-optimizer workflow address?
?
A first output is often only a good start; the pattern checks whether it is accurate, complete, within all constraints, and up to the required standard, and improves it if not.

What does the optimizer (generator) agent do?
?
It takes the task and generates an output, then refines that output based on the evaluator's feedback.

What does the evaluator (critic or reflector) agent do?
?
It acts as an expert reviewer, assessing the optimizer's output against predefined evaluation criteria and providing specific, actionable feedback.

Describe one cycle of the evaluator-optimizer loop.
?
The optimizer generates, the evaluator critiques the output against the criteria, and the optimizer refines it based on the feedback; the cycle repeats until a stopping condition is met.

What three elements make the evaluator-optimizer loop effective?
?
Clear evaluation criteria, actionable feedback, and stopping conditions.

What three questions test whether an evaluation criterion is clear?
?
Is it specific? Can it be measured or objectively checked? Is it unambiguous?

What makes feedback actionable?
?
It is specific and constructive, with enough detail for the optimizer to understand what needs to change and ideally how to change it.

What three inputs does the optimizer use to produce an improved version?
?
The original task instructions, its previous attempt, and the evaluator's feedback.

What are the three common stopping conditions?
?
The output meets all evaluation criteria, a maximum number of iterations is reached, or the improvement between cycles becomes negligible.

Why does an evaluator-optimizer loop need stopping conditions?
?
So the process is both effective and finite, preventing endless loops and wasted cost.

What kinds of tasks is the evaluator-optimizer workflow best suited to?
?
Tasks demanding high precision, adherence to complex requirements, and top quality, such as research reports, critical code, or detailed plans.

When a loop stops at its iteration cap, which attempt should it return?
?
The highest-scoring attempt, with a note of which criteria still fail, because later attempts can be worse.

Each cycle passes with probability 0.5. What is the probability of passing within 3 attempts?
?
1 − 0.5³ = 0.875.

Why can't the loop be more reliable than its evaluator?
?
If the evaluator falsely accepts a bad output, the loop stops early with that bad output; quality is capped by how well the evaluator detects problems.
