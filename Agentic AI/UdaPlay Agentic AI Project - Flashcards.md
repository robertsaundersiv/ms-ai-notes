---
title: "UdaPlay Agentic AI Project – Flashcards"
type: flashcards
source: "[[UdaPlay Agentic AI Project]]"
created: 2026-10-06
tags:
  - flashcards
---

#flashcards/agentic-ai/udaplay

What is two-tier retrieval in a research agent?
?
Answering from a local knowledge base first, and searching the web only when the local results are judged insufficient.

What decides when a two-tier agent falls back to web search?
?
A retrieval evaluation step, often an LLM judge, that rules whether the retrieved documents can answer the question.

Why should an LLM judge return a structured verdict such as a boolean?
?
A typed verdict can drive a workflow branch directly and reliably, without parsing free-text opinions.

Why store each record's full fields as metadata in the vector store?
?
Retrieval then returns exact structured facts, such as year, platform and publisher, rather than only a text blob, which grounds answers better.

Why does a web-search cache need a persistent vector store?
?
Cached results must survive restarts to be reused in later sessions. An in-memory store would lose them.

How can a deterministic cache key prevent duplicate cache entries?
?
Hashing a normalized form of the question gives the same ID for repeats, so an upsert overwrites the old entry instead of adding another.

Why include the original question in a cached web result's embedded text?
?
A repeat of the same question then matches that entry very closely in similarity search.

Why keep source URLs and a cached-on date with cached web results?
?
The URLs preserve provenance for citation, and the date makes freshness checks and expiry possible.

Why tag cached web results with a type field?
?
So cache entries can be found, labelled or deleted separately without touching curated data.

What does caching web results save?
?
Repeated web API calls, with their cost, rate limits and latency, and it makes answers to repeat questions consistent.

What does caching web results not save?
?
LLM tokens, since the cached content still goes into the model's context, and it doesn't keep information fresh.

What is the main risk of writing web results into an agent's knowledge base?
?
Unverified or injected web content becomes persistent internal knowledge that later answers cite as trusted.

Why does a web cache need a TTL?
?
Some facts change, such as news or what a studio is working on, so cached answers must expire or be refreshed.

Why might a demo clear its cache at startup?
?
So the full fallback path is visible every run, rather than being skipped because an earlier run cached the answer.

How can long-term user preferences be applied to an agent's answers?
?
Recall the relevant preferences before each query and inject them into the system prompt as rules.

How can user preferences change an answer without changing retrieval?
?
Retrieval and evaluation stay the same, while the answer step uses the preferences to choose among the retrieved options.

How can an injected preference conflict with grounding rules?
?
A preference such as "add interesting details" can push the model to add facts not found in the retrieved context.

Why is "long-term" memory that is rebuilt on every run not really long-term?
?
If the store is in-memory or reset on startup, nothing persists across restarts. It only works within one process.

What does it mean to build an agent with tools as nodes?
?
Each tool is a fixed step in a state machine, and code routes between steps instead of the LLM choosing which tool to call next.

What are the benefits of tools-as-nodes over an LLM-driven tool loop?
?
A guaranteed process, fewer LLM calls, no runaway loops, unit-testable steps and a truthful record of the path taken.

What flexibility does a tools-as-nodes workflow give up?
?
It can only follow designed paths, so it loses LLM improvisation such as query reformulation or ad-hoc retries unless those are added as nodes.

Why is a process description written by code more trustworthy than one written by the model?
?
Code reports the path actually taken. A model's self-description is a claim that may not match what happened.

When should control flow move from the LLM to code?
?
When inputs follow a predictable pattern, so autonomy adds risk and cost without adding value.

What two roles can structured output play in an agent?
?
A routing signal, such as a judge's boolean verdict, and a validated final deliverable, such as JSON answer records.

Why preserve date precision in structured output?
?
Padding a known year into a full date fabricates precision the source never gave.

What can a too-narrow output schema lose?
?
Citations, nuance and answers to question types it doesn't model, such as yes/no verdicts.

Why extract structured output from the workflow's final text answer rather than from raw documents?
?
The text answer already applied decisions such as preferences and counts, so extraction only structures it instead of re-deciding it.

Why share one rule, such as an answer-count rule, across every stage of an agent?
?
A single definition keeps all stages consistent and prevents the rule from drifting between prompts.

Why does the web-search path typically cost more tokens than the local path?
?
Search results add substantial context, and the extra tool call adds another model turn.
