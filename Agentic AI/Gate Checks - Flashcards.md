---
title: "Gate Checks – Flashcards"
type: flashcards
source: "[[Gate Checks]]"
created: 2026-09-23
tags:
  - flashcards
---

#flashcards/agentic-ai/gate-checks

What is a gate check?
?
A programmatic validation placed between steps in a prompt chain. It is a quality control point that ensures an output meets criteria before it is passed on.

What are the three core gate types from the lecture?
?
Format, content, and logic.

What does a format gate check, and what tools help?
?
Structure: JSON/XML validity, required fields, types, lengths. Pydantic and structured-output modes help.

What does a content gate check, and what tools help?
?
Keywords, phrases, topic and relevance. Regex, semantic embeddings, or another LLM.

What does a logic gate check?
?
Numerical and logical sense: plausible values, cross-field consistency, whether code compiles, restricted imports.

What does a grounding gate check?
?
Whether the output is supported by the source, e.g. extracted values appear in verbatim evidence quotes.

What does an action-precondition gate check?
?
Whether it is safe to act on an external system now: current state, permissions, idempotency.

Name four gate types beyond format, content and logic.
?
Any four of: grounding, safety/policy, cross-step consistency, confidence, budget, action preconditions, human approval.

In what order should gates run?
?
Cheapest and deterministic first (format, logic), then expensive and probabilistic (LLM judge), then safety and action gates.

What are the options when a gate fails?
?
Retry with feedback, repair in code, fall back, reroute, escalate to a human, or abort/block.

Why shouldn't safety-gate failures be retried automatically?
?
Retrying invites rephrasing until the output slips past the filter. Block, log and alert instead.

Why are gates needed in chains, in one formula?
?
Reliability compounds as p^n. Five 95% steps give about 77% end to end, and gates stop errors spreading.

What is wrong with a gate that only checks format?
?
Output can be well-formed and still wrong, ungrounded or inconsistent.

What two numbers measure how good a probabilistic gate is?
?
Gate recall (real errors caught) and gate precision (rejections that were real errors).
