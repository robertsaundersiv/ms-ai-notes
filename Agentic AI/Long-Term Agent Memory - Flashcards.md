---
title: "Long-Term Agent Memory – Flashcards"
type: flashcards
source: "[[Long-Term Agent Memory]]"
created: 2026-10-06
tags:
  - flashcards
---

#flashcards/agentic-ai/long-term-memory

What is the difference between short-term and long-term agent memory?
?
Short-term memory holds context within one session or thread. Long-term memory stores facts, experiences and preferences externally and recalls them across sessions.

Why do agents such as tutors, assistants and support bots need long-term memory?
?
To personalize responses, avoid repeating questions or instructions, and improve by learning from past interactions.

What is semantic memory in an agent?
?
Facts learned from the user through interaction, such as names, preferences or the tools their team uses.

What is episodic memory in an agent?
?
Records or summaries of past interactions and their outcomes, such as a fix that worked last time.

How is episodic memory commonly used?
?
As few-shot examples: recalling how a similar past situation was handled successfully.

What is procedural memory in an agent?
?
Learned behavioral adaptations, such as adopting a formal tone, often implemented by updating internal prompts or rules.

What is the one-line distinction between semantic, episodic and procedural memory?
?
Semantic is what is true about you, episodic is what happened between us, and procedural is how I should behave with you.

What kinds of stores can hold long-term memory?
?
Vector databases for semantic recall, relational databases for structured facts, and document stores for flexible profiles and episodes.

What are the three memory scopes?
?
User-scoped (one identity), team-scoped (shared across a group), and global-scoped (patterns across all users).

How does an agent decide which memories to query?
?
It identifies the current context, such as user ID, team or application route, and queries the collections in that scope.

What can trigger memory retrieval?
?
Semantic similarity, tags, time and session or task context.

Where can retrieved memories be injected?
?
Into the system prompt, as background context, or as parameters to tools.

How does long-term memory differ from RAG?
?
RAG retrieves from static documents written by others. Long-term memory is built from interaction and evolves over time, even when it uses the same retrieval mechanics.

Why does long-term memory need policies that a RAG index doesn't?
?
The agent writes its own corpus, so it needs rules for what to store, when it expires and who can access it.

What are the four memory best practices from the lesson?
?
Selectivity, expiry with TTLs, separation with namespaces, and balancing privacy against performance.

Why shouldn't an agent store every line of dialogue?
?
It adds noise to retrieval, raises cost and increases privacy exposure. Only useful, durable information should be kept.

What is a TTL in agent memory?
?
A time-to-live after which a memory expires, so outdated information is retired automatically.

What problem do memory namespaces solve?
?
They prevent collisions and leaks between users, teams or use cases by partitioning the store.

What three questions guide memory design?
?
What should be remembered, how long it should persist, and who can access it.

How does metadata filtering make a shared vector store user-scoped?
?
Each memory is stored with owner metadata, and every search filters on that owner, so only that user's memories can match.

Why fix the owner and namespace in code rather than letting the model pass them to memory tools?
?
The model then can't read or write another user's memories, by mistake or through injected instructions.

What is memory consolidation?
?
Merging, updating or replacing stored memories to remove duplicates and resolve contradictions, such as an old preference replaced by a new one.

What is memory poisoning?
?
Wrong or malicious content written into long-term memory that then influences every future session that recalls it.

Why is procedural memory the riskiest memory type?
?
It changes the agent's own behavior, so a single manipulated or mistaken interaction could alter how it acts permanently unless updates are reviewed and reversible.

Why must long-term memory use persistent storage?
?
An in-memory or reset-on-start store loses everything on restart, so it is effectively short-term memory with a long-term interface.

Why should memories be weighted by recency?
?
Facts become stale at different rates, so decaying older memories favors current information without discarding stable facts outright.

How should global-scope memory protect privacy?
?
Promote only aggregated, anonymized patterns to global scope, never individual users' personal details.
