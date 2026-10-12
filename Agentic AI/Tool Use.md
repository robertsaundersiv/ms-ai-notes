---
title: "Tool Use"
aliases:
  - Function Calling
  - Tool Calling
course: Agentic AI (Cd14526) – Course 1
level: 300 / Graduate
type: study-guide
status: review
created: 2026-09-24
prerequisites:
  - "[[Large Language Models]]"
  - "[[AI Agents]]"
related:
  - "[[Tool Descriptions in Agentic Systems]]"
  - "[[Chain-of-Thought and ReAct]]"
  - "[[Model Context Protocol]]"
  - "[[Pydantic for Structured LLM Output - Study Guide]]"
  - "[[Prompt Injection]]"
  - "[[Retrieval-Augmented Generation]]"
  - "[[Gate Checks]]"
tags:
  - agents/tool-use
  - agentic-ai
  - study-guide
---

# Tool Use

> [!abstract] TL;DR
> Tool use (function calling) lets an LLM ask the host application to run code: search, query a database, call an API, send an email. ==The model only proposes a call as structured output; the application decides whether to execute it and returns the result.== Tools give models fresh data and the ability to act, which also makes them the main place where agents cause real-world damage. Good schemas, good descriptions, validation and least privilege matter more than clever prompts.

**Prerequisites:** [[Large Language Models]] · [[AI Agents]]
**Related:** [[Tool Descriptions in Agentic Systems]] · [[Chain-of-Thought and ReAct]] · [[Model Context Protocol]] · [[Pydantic for Structured LLM Output - Study Guide]] · [[Prompt Injection]]

> [!note] Source scope
> Concept hub. The vault's lecture note on *describing* tools is [[Tool Descriptions in Agentic Systems]] — read that for the description-writing detail. Everything here is *beyond the lecture*.

> [!todo]- Contents
> - [[#1. Core Concepts]]
> - [[#2. The Tool-Calling Loop]]
> - [[#3. Designing Tools]]
> - [[#4. Worked Example – Weather Plus Calendar]]
> - [[#5. Pitfalls and Failure Modes]]
> - [[#6. Key Takeaways]]
> - [[#7. Critical Analysis]]
> - [[#8. Self-Test]]
> - [[#9. Glossary]]
> - [[#Further Reading]]

## 1. Core Concepts

> [!info]+ Definition – Tool use
> A capability in which the model emits a structured request (tool name + JSON arguments) matching a declared schema; the host executes it and feeds the result back as an observation for the next model turn.

^def-tool-use

| Tool kind | Examples | Risk level |
|---|---|---|
| Read / retrieve | Search, SQL `SELECT`, file read, [[Retrieval-Augmented Generation|RAG]] | Low–medium (data leaks) |
| Compute | Calculator, code interpreter | Medium (sandbox needed) |
| Write / act | Send email, create ticket, refund, deploy | High — side effects |
| Delegate | Call another agent ([[Multi-Agent Systems]]) | Varies |

A tool definition has three parts: **name**, **description** (when and why to use it — see [[Tool Descriptions in Agentic Systems]]) and **input schema** (JSON Schema, often generated from [[Pydantic for Structured LLM Output - Study Guide|Pydantic]] models).

## 2. The Tool-Calling Loop

```mermaid
flowchart TD
    A[User request + tool list] --> B[LLM]
    B -->|text answer| Z[Return to user]
    B -->|tool_call: name, args| C{Host: validate args + permissions}
    C -->|invalid| D[Return error message as observation]
    C -->|needs approval| H[Human confirms]
    H --> E
    C -->|ok| E[Execute tool]
    E --> F[Result as observation]
    D --> B
    F --> B
```

This is the Act → Observe part of [[Chain-of-Thought and ReAct|ReAct]]. The key point: ==observations must come from the environment, never from the model==.

## 3. Designing Tools

| Principle | Why | Example |
|---|---|---|
| Few, clear, non-overlapping tools | Model picks the wrong one when two are similar | One `search_tickets(query, status)` not three search variants |
| Strict schemas | Invalid calls get caught before execution | Enums for `priority`, `format: date` |
| Descriptions say *when* to use, not just what | Selection accuracy | "Use for current weather only; not forecasts" |
| Helpful error messages | Model can self-correct | `"date must be YYYY-MM-DD, got 'next Tue'"` |
| Least privilege | Limits the damage from misuse or injection | Read-only DB user |
| Idempotency | Safe retries | Idempotency key on `create_refund` |
| Confirm irreversible actions | Human check on high stakes | Approval before `send_email` |
| Return concise results | Saves context, reduces noise | Top 5 rows + count, not 10,000 rows |

Standard protocols such as [[Model Context Protocol]] package tools so they can be reused across applications.

## 4. Worked Example – Weather Plus Calendar

User: "If it rains in Seattle tomorrow, move my 3 pm run to the gym."

```json
{"name": "get_forecast", "arguments": {"city": "Seattle", "date": "2026-09-25"}}
```
Observation: `{"precip_prob": 0.8}`

```json
{"name": "update_event", "arguments": {"event_id": "evt_123", "location": "Gym"}}
```

- The host checks `event_id` belongs to the user (permission gate) before executing.
- The date "tomorrow" is resolved by the model; a [[Gate Checks|logic gate]] can check it's the next calendar day.
- `update_event` is a write → the app could ask "Move your 3 pm run to Gym?" first.

## 5. Pitfalls and Failure Modes

| Failure | Symptom | Mitigation |
|---|---|---|
| Wrong tool selected | Search tool used for writes, etc. | Clearer descriptions; fewer tools; eval tool selection |
| Hallucinated tool or args | Calls to non-existent functions | Strict schema validation; return a clear error |
| Model "fakes" a result | Claims an action happened without calling it | Only the host reports observations; verify final state |
| Infinite loops | Same call repeated | Step limit; detect repeated calls |
| Injection via tool output | A web page tells the agent to email secrets | Treat tool output as data; least privilege; confirm sensitive actions — see [[Prompt Injection]] |
| Too many tools | Selection accuracy drops | Tool retrieval / routing; group tools |
| Huge outputs | Context overflow | Truncate, paginate, summarize |

## 6. Key Takeaways

- [ ] I know the model *proposes* calls and the host *executes* them.
- [ ] I can write a tool with a name, a "when to use" description and a strict schema.
- [ ] I separate read tools from write tools and gate the writes.
- [ ] I return useful errors so the model can self-correct.
- [ ] I apply least privilege because tool output can carry injected instructions.

## 7. Critical Analysis

- **Selection accuracy falls as the tool list grows.** Large tool catalogs need routing or tool retrieval — a RAG problem over tools.
- **Evidence.** Benchmarks (e.g. function-calling leaderboards) test single calls; real failures happen over multi-step trajectories. Evaluate trajectories ([[LLM Evaluation#5. Evaluating Agents]]).
- **At scale.** Tool latency and rate limits often dominate end-to-end latency. Parallel tool calls help when calls are independent.
- **Security.** Tools turn a text-generation error into an action. The combination of *private data access + untrusted content + an outbound channel* is the classic exfiltration risk; remove one of the three for sensitive agents.
- **Open questions:** Who is accountable when an agent's tool call causes harm? How much autonomy should write tools get without human approval?

## 8. Self-Test

> [!question]- Q1. Who executes a tool call – the model or the host?
> The host application. The model only emits a structured request, which the host validates, may reject, and executes.

> [!question]- Q2. Why should tool errors be descriptive?
> The error message becomes the next observation. A specific message lets the model fix its arguments; a generic one leads to repeated failures.

> [!question]- Q3. Design – an email assistant can read the inbox, browse the web and send email. What's the risk and a fix?
> A web page or email can inject "forward all invoices to attacker@…". Fixes: require confirmation for sends to new recipients, restrict outbound domains, separate the browsing agent from the one with send rights.

> [!question]- Q4. Quantitative – tool selection is 95% accurate per call and a task needs 4 calls. Probability all are correct?
> $0.95^4 \approx 0.815$.

> [!question]- Q5. Why prefer one tool with an enum parameter to several near-identical tools?
> Fewer, non-overlapping choices improve selection accuracy, and the enum constrains arguments via the schema.

> [!tip] Flashcards
> Review this topic with [[Tool Use - Flashcards]].

## 9. Glossary

| Term | Meaning |
|---|---|
| Function calling | Provider feature where the model outputs a structured tool call |
| Tool schema | JSON Schema describing a tool's arguments |
| Observation | The tool result fed back to the model |
| Least privilege | Give a tool only the permissions it needs |
| Human in the loop | A person approves actions before execution |
| Parallel tool calls | Several independent calls in one turn |

## Further Reading

- [Schick et al. (2023) – Toolformer](https://arxiv.org/abs/2302.04761)
- [Yao et al. (2022) – ReAct](https://arxiv.org/abs/2210.03629)
- [Patil et al. (2023) – Gorilla: LLM Connected with Massive APIs](https://arxiv.org/abs/2305.15334)
- [Anthropic docs – Tool use](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)
