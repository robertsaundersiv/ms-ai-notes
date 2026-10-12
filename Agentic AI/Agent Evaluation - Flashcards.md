---
title: "Agent Evaluation – Flashcards"
type: flashcards
source: "[[Agent Evaluation]]"
created: 2026-10-06
tags:
  - flashcards
---

#flashcards/agentic-ai/agent-evaluation

Why isn't "the agent runs" enough to know it works?
?
It may still pick wrong tools, waste tokens, produce bad outputs or take harmful actions. Only evaluation shows whether it works correctly, safely and efficiently.

What does it mean that agent behavior can drift unnoticed?
?
Performance or behavior can degrade over time or after changes, such as wrong tool calls or rising token use, with no alert unless something is measuring it.

What are the four dimensions of agent evaluation?
?
Task completion, quality control, tool interaction and system metrics.

What does task completion measure?
?
Whether the agent achieved its goal, how many steps it took, and whether human intervention was needed.

What does quality control measure?
?
Whether the output has the correct format, follows the prompt instructions and actually uses the provided context.

What does tool interaction measure?
?
Whether the agent chose the right tool, passed valid arguments and got a useful result.

What do system metrics measure?
?
Resource use and reliability: latency, token usage, cost and failure rates, including silent failures such as context overflow.

What is final-response (black-box) evaluation?
?
Judging only the agent's end result against the goal or a reference, often with an LLM judge, without looking at how it got there.

What is the main weakness of final-response evaluation?
?
It shows what happened but not why, so lucky successes, inefficient paths or unsafe actions can go unnoticed.

What is single-step evaluation?
?
Testing one decision in isolation, such as which tool the agent selects or how it formats a query, against the expected step.

What are the strengths and limits of single-step evaluation?
?
It is fast, cheap and good for debugging, but it doesn't show whether the full task succeeds.

What is trajectory evaluation?
?
Reviewing the whole execution path: which tools were called, in what order, with what arguments, and how results were used.

Why is trajectory evaluation called a flight recorder for agents?
?
It captures the full sequence of decisions and actions, so you can see why a run succeeded or failed.

When is trajectory evaluation most valuable?
?
For complex workflows where the process matters as much as the result, and for debugging failures.

What four ingredients does every agent evaluation need?
?
Inputs, outputs, reference data and an evaluator.

What counts as inputs in an agent evaluation?
?
The user query, the tools available, and any memory or instructions given to the agent.

What counts as reference data in an agent evaluation?
?
Ground truth to compare against, such as a correct answer, an expected tool sequence or an expected end state.

What kinds of evaluators can grade agents?
?
Rules, heuristics, or a model acting as an LLM judge.

Why is consistency more important than a perfect evaluation metric?
?
A repeatable process lets you compare runs over time and know whether a change actually improved the agent.

Why is agent evaluation hard?
?
Agents behave variably, many tasks are subjective, there's no universal metric, evaluation costs money, and metrics can be overfit.

What is overfitting to evaluation metrics?
?
Tuning an agent to pass the test suite rather than to perform well for real users.

If an evaluation shows poor tool selection, what should you check first?
?
The clarity of tool descriptions and the prompt instructions.

If an evaluation shows excessive token use, what should you change?
?
Shorten memory and context, and prune or trim tool results.

If an agent takes many more steps than needed, what does that suggest?
?
Inefficient planning, which calls for better instructions, clearer tools or a more structured workflow.

Why can't a perfect score on a single test case be trusted?
?
One run on one case says almost nothing about variability, edge cases or safety, and has no statistical weight.

Why should evaluation check tool arguments as well as tool names?
?
The right tool with the wrong arguments can still produce a wrong or harmful result while passing a name-only check.

What is the difference between pass@k and pass^k?
?
pass@k is succeeding at least once in k runs. pass^k is succeeding in all k runs, which is what users experience.

Why must an LLM judge itself be validated?
?
It can be lenient, biased toward confident or long answers, or swayed by the answer's claims, so its grades must be checked against human labels.

Why do flexible trajectory references often beat one golden path?
?
Many tasks have several valid paths, so constraints such as required order, forbidden tools and step limits generalize better than exact matches.

How can evaluation catch dangerous actions like deleting customer records?
?
Include trajectory test cases where destructive tools are forbidden, run them repeatedly in a sandbox, and fail any run that calls them.

Why evaluate the environment rather than the agent's claim?
?
An agent can say it completed an action that never happened, so check the actual system state.

Why reset agent memory between evaluation cases?
?
So earlier runs can't influence later ones and each case is tested independently.

Why should evaluators penalize unexpected tool calls, not just reward expected ones?
?
A check that only asks whether an expected tool appeared will pass runs that also called wrong or forbidden tools.

Why is it a problem when an evaluator fills some metrics with assumed values?
?
Assumed or copied fields inflate scores and make the dimensions look independently measured when they aren't, hiding real failures.

Why should an evaluator's fallback logic be generic rather than tied to one test case?
?
Fallback rules hard-wired to one case's expected keywords will grade every other case incorrectly whenever the fallback triggers.
