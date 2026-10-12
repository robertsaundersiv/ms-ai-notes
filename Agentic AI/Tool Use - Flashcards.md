---
title: "Tool Use – Flashcards"
type: flashcards
source: "[[Tool Use]]"
created: 2026-09-24
tags:
  - flashcards
---

#flashcards/agentic-ai/tool-use

What is tool use (function calling)?
?
The model emits a structured request (tool name + JSON args) matching a schema. The host executes it and returns the result as an observation.

Who executes a tool call?
?
The host application, never the model. The model only proposes the call.

What are the three parts of a tool definition?
?
Name, description (when/why to use it), and input schema.

What should a tool description say?
?
When to use the tool and when not to, not just what it does.

Why return descriptive tool errors?
?
The error becomes the next observation, so the model can correct its arguments.

How should read tools and write tools be treated differently?
?
Write/act tools have side effects, so gate them with validation, idempotency and human confirmation for irreversible actions.

What are three risk factors for data exfiltration by an agent?
?
Access to private data, exposure to untrusted content, and an outbound channel. Remove one for sensitive agents.

What happens to selection accuracy as the tool list grows?
?
It drops. Use fewer, non-overlapping tools, or route/retrieve tools.

How do you prevent an agent from looping on tool calls?
?
Step limits and detecting repeated identical calls.

Why must observations come from the environment?
?
Otherwise the model can invent results ("email sent") that never happened.
