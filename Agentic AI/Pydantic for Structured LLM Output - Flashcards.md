---
title: "Pydantic for Structured LLM Output – Flashcards"
type: flashcards
source: "[[Pydantic for Structured LLM Output - Study Guide]]"
created: 2026-09-23
tags:
  - flashcards
---

#flashcards/agentic-ai/pydantic-structured-output

What three roles can one Pydantic model play in an LLM chain?
?
A prompt spec (it generates the schema the model sees), a gate (it validates the response), and a typed handoff to the next step.

Why is schema-valid LLM output not automatically safe?
?
Schema validation checks shape only. Values can still be ungrounded, inconsistent across fields, or implausible.

What is an information-bound gate?
?
A validation rule derived from a downstream step's dependency on a specific fact, not from the data's shape.

What rule decides which gate checks to write?
?
Start from the facts downstream steps consume. Each consumed fact needs a check, and each check should protect a consumed fact.

What four properties should you check for each consumed fact?
?
Well-formed, grounded, consistent, plausible.

Which gate types from the course map to the four properties?
?
Well-formed maps to format. Grounded maps to content. Consistent and plausible map to logic.

How can a validator check output against the source document or world state?
?
Pass that information into validation as context, so validators can compare the output to the source rather than only checking its shape.

What kind of validator implements cross-field (logic) checks?
?
A model-level validator that runs after the individual fields are parsed, so it can compare fields with each other.

How do you stop a model fabricating values to fill required fields?
?
Make the field nullable so "not found" can be represented, and require evidence whenever it is non-null.

What does forbidding extra fields in a schema protect against?
?
The model adding invented fields (e.g. "approved": true) that a later step might read.

What is the pass probability after k independent attempts with per-attempt pass rate p?
?
1 - (1 - p)^k. It is an upper bound, because real failures are correlated.

What must a validate-retry loop end with when retries are exhausted?
?
Escalation to a human or a fallback. The output is never passed forward.

Why keep validators pure rather than querying a database inside them?
?
Determinism, speed, testability and replayability in evaluations. Pre-load world state into context instead.

Why doesn't a schema defend against prompt injection?
?
An attacker can write the malicious claim into the source, so the output is both schema-valid and grounded. Consequential actions need checks against trusted world state.

What is the key metric to evaluate a gate, beyond pass rate?
?
Gate recall on wrong outputs, plus the error rate among outputs accepted after a retry.
