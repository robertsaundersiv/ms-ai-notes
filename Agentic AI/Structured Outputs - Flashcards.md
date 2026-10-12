---
title: "Structured Outputs – Flashcards"
type: flashcards
source: "[[Structured Outputs]]"
created: 2026-09-30
tags:
  - flashcards
---

#flashcards/agentic-ai/structured-outputs

What is a structured output?
?
A model response that follows a machine-readable contract, usually JSON matching a schema, so code can parse it instead of scraping text.

Why do structured outputs make agents more useful than plain text?
?
Downstream systems such as ticketing, dashboards, alerts and other agents can act on typed fields directly. That enables integration and automation.

Why isn't asking for JSON in the prompt enough?
?
The prompt is a request, not enforcement. Models are trained on natural language, not strict type rules, so they sometimes produce invalid or vague output.

What are common ways prompt-only JSON breaks code?
?
Values outside the allowed set, placeholders instead of null, wrong types, JSON wrapped in extra text, missing or renamed keys, and truncated output.

What does an output parser do?
?
It parses the model's raw text and validates it against a schema. If it's valid you get a typed object; if not, a fallback runs (retry, repair, default or escalate).

What are the five steps of the structured-output reliability ladder?
?
Prompt for JSON, then parser plus validation, then function calling with a schema, then strict constrained decoding, then semantic validators with retries and escalation.

How does function calling help produce structured output?
?
The model receives a schema and returns its answer as a structured call object, which is usually well-formed and easy to parse.

Does plain function calling guarantee the output matches the schema?
?
No. Without strict mode the schema is a strong hint. The model can still produce invalid values or miss fields.

What is constrained decoding?
?
At each token the provider blocks tokens that would break the schema, so the output is schema-conformant by construction.

What does strict schema enforcement guarantee, and what doesn't it?
?
It guarantees shape: valid JSON, the right keys, types and allowed values. It doesn't guarantee truth, grounding, cross-field consistency, or completion if the output is refused or truncated.

What's the difference between a JSON-only mode and strict schema mode?
?
A JSON-only mode guarantees valid JSON syntax, but not your fields or types. Strict mode guarantees conformance to your specific schema.

Why can a schema-valid output still be wrong?
?
A schema checks form, not facts. A hallucinated or ungrounded value of the right type passes the schema.

Why define output schemas as typed classes, such as Pydantic models?
?
One definition does three jobs: it generates the schema the model sees, validates the response, and gives your code a typed object.

How should a typed date field relate to the input context?
?
A date type can force a valid format, but relative dates like "next Friday" only resolve correctly if the prompt supplies the current date.

What should happen when a structured output fails validation?
?
Send the specific validation errors back to the model for a bounded number of retries, then escalate to a fallback or a human.

Why must retries be capped?
?
Failures are often correlated, so repeating rarely fixes the same mistake and only adds cost. The loop needs to end in escalation.

How does strict mode usually represent an optional field?
?
As a required field that may be null. The key is always present, and null means absent.

Why should a schema let the model express "not found"?
?
If a field can't be null, the model is forced to invent a value or a placeholder, which passes validation but is false.

Why prefer closed vocabularies (enums) over free-text fields?
?
They block vague or invalid values, make routing deterministic, and can't carry injected instructions.

Why give a classification field an "other" option?
?
Without an escape value the model forces out-of-scope cases into a wrong category. "Other" keeps classification honest and shows where categories are missing.

Why do field descriptions in a schema matter?
?
The schema is part of the prompt. Descriptions tell the model what each field means and when to leave it empty.

Why might you place a reasoning field before the answer fields?
?
Output is generated in key order, so the model reasons before it commits to the answer.

How should you evaluate a structured-extraction system?
?
Measure field-level accuracy against labeled data, not just the percentage of outputs that are valid JSON.

Why keep your own schema validation even when the provider enforces the schema?
?
Provider guarantees vary and support only part of the schema language. Local validation keeps one source of truth and makes the system portable.

Which structured output fields are a prompt-injection risk?
?
Free-text string fields, because they can carry instructions into the next agent or prompt. Enums and booleans can't.

Besides validation errors, what else must structured-output code handle?
?
Refusals and truncated output, which can return no usable object even when the schema is enforced.
