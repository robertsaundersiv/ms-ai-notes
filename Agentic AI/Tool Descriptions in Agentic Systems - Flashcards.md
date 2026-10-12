---
title: "Tool Descriptions in Agentic Systems – Flashcards"
course: Agentic AI (Cd14526) – Course 1
type: flashcards
source: "[[Tool Descriptions in Agentic Systems]]"
created: 2026-09-23
---

#flashcards/agentic-ai/tool-descriptions

Flashcards for [[Tool Descriptions in Agentic Systems]].

What are the three parts of a tool definition the model sees?
?
Name, description and input schema (usually JSON Schema).

In tool calling, who actually executes the tool?
?
The application runtime. The model only emits a structured call request (name plus arguments) and receives the result as context.

What is an agent-computer interface (ACI)?
?
The tool set, descriptions and result formats, seen as an interface designed for an LLM user, analogous to HCI for humans.

What five things should a good tool description state?
?
Purpose, when to use it, when not to use it (and the alternative), what it returns, and its side effects or reversibility.

Why constrain parameters with enums and formats instead of prose?
?
Schemas are validated deterministically. Prose is only a suggestion the model may ignore.

Why are error messages part of prompt design for tools?
?
Tool results, including errors, return to the model's context and shape its next action. Actionable errors guide recovery; opaque ones cause retry loops.

How do tool-definition tokens scale in an agent run?
?
Roughly number of tools × average definition length, re-sent on every model call in the run.

Name three strategies for handling a very large tool set.
?
Consolidating into task-level tools, namespacing, routing to domain toolsets, tool retrieval, or specialist sub-agents (any three).

What is the most common cause of wrong tool selection?
?
Overlapping or ambiguous tools with no guidance on when to use one versus another.

What is a tool "rug pull"?
?
A third-party tool's description or behavior changing after the user or developer approved it.

Why can't a tool description alone make a destructive tool safe?
?
The description only informs the model. Enforcement, such as confirmation gates and permissions, has to happen in the runtime.
