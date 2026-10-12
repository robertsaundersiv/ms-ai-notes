---
title: "AI Memory – Flashcards"
type: flashcards
source: "[[AI Memory]]"
created: 2026-09-24
tags:
  - flashcards
---

#flashcards/agentic-ai/memory

Why are LLMs described as stateless?
?
They retain nothing between calls. Only tokens in the current context affect the output.

What are the five memory types for agents?
?
Short-term/working (context), episodic (events), semantic (facts/preferences), procedural (skills/instructions), parametric (weights).

Where does short-term memory live?
?
In the context window.

What are the main memory operations?
?
Write, retrieve, consolidate, forget, compress.

What three signals does the Generative Agents retrieval score combine?
?
Recency, importance, and relevance.

What does memory consolidation do?
?
Merges duplicates and replaces outdated or contradicting facts.

What is memory poisoning?
?
Malicious or injected content stored as memory, which then affects every future session.

How do you prevent cross-user memory leaks?
?
Partition memory stores by user/tenant and support deletion.

Why is the context window a budget?
?
System prompt, memories, recent turns, tool results and output reserve all compete for a fixed token limit.

How is agent memory related to RAG?
?
Long-term memory is retrieval over the agent's own stored history, so it inherits RAG's failure modes.
