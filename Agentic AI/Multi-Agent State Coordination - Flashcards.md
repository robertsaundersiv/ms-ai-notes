---
title: "Multi-Agent State Coordination - Flashcards"
type: flashcards
source: "[[Multi-Agent State Coordination]]"
created: 2026-10-10
tags:
  - flashcards
---

#flashcards/agentic-ai/state-coordination

What is state coordination in a multi-agent system?
?
The mechanisms that ensure multiple agents have a consistent, synchronized view of shared state, especially during concurrent operations.

Using the air-traffic analogy, how does state coordination differ from state management?
?
Management is knowing where every plane is. Coordination is actively stopping two planes from using the same runway at once, i.e. detecting and resolving conflicts over shared resources.

What does the surgical-team analogy illustrate?
?
Synchronization: every team member needs the same real-time view of shared state, so a change seen by one (like a drop in blood pressure) is known and acted on by all.

What is synchronization?
?
The process of keeping data consistent across multiple agents or systems.

What is concurrency in a multi-agent system?
?
Multiple agents or processes trying to access or modify the same shared resource at the same time.

What is conflict detection?
?
Identifying when agents' actions have produced an inconsistent or invalid state, or when one agent's knowledge contradicts another's.

What is conflict resolution?
?
The strategy or logic used to resolve a detected conflict and return the system to a consistent state.

What five questions should you ask about shared state in an agent team?
?
Where is the shared state? How do agents access it? What happens if two agents change it at once? What if external systems change it? How do we ensure consistency?

What are the three synchronization strategies from the lesson?
?
Lean on your database (locks and transactions), state broadcasting or eventing, and optimistic concurrency control.

Why should the database, not agent memory, be the source of truth for application state?
?
The database already provides consistency guarantees like transactions and locking. Agent memory holds copies that can go stale.

What do transactions provide to agent tools?
?
Atomicity: a group of changes either commits together or not at all.

What does a lock provide, and what is its cost?
?
Exclusive access to data while one agent changes it. Others must wait, and badly managed locks can cause deadlocks.

Why should a lock never be held across an LLM call?
?
LLM calls take seconds, so every other agent needing that data blocks for that long, which increases contention and deadlock risk.

What is state broadcasting (eventing)?
?
When a tool updates critical state, it publishes an event. Agents subscribed to that event are notified and react, instead of repeatedly polling.

Give an example of state broadcasting from the lesson.
?
When inventory drops below the reorder point, an inventory-low event is published, and interested agents (e.g. reordering) react.

What are the main trade-offs of event broadcasting?
?
It decouples publishers from subscribers and avoids polling, but delivery is usually asynchronous. Subscribers may briefly see stale state or get duplicate or out-of-order events, so they should be idempotent.

What is a lost update?
?
Two agents read the same data and both write changes, and the second write silently overwrites the first.

What is the core assumption of optimistic concurrency control?
?
Conflicts are rare, so don't lock up front. Instead, check for a conflict just before committing.

How does optimistic concurrency control detect a conflict?
?
The agent remembers the version (or timestamp) it read, and the write succeeds only if the record still has that version. If another write bumped the version, the update fails.

What should happen after an optimistic concurrency update fails?
?
Roll back, re-read the latest state, re-evaluate, and retry the whole operation.

When does optimistic concurrency control work well?
?
When reads are frequent and writes to the same data are relatively infrequent.

When is pessimistic locking preferable to optimistic concurrency control?
?
When conflicting writes are frequent, because optimistic retries would pile up and waste work.

What are the four conflict-resolution strategies from the lesson?
?
Predefined rules or policies, negotiation or consensus, rollback and retry, and human escalation.

What is predefined-rule conflict resolution, and why is it a good default?
?
Resolution logic embedded in the system, such as priority orders or "latest timestamp wins". It is deterministic, fast, auditable and testable.

Give the lesson's traffic example of a predefined conflict rule.
?
At a contested intersection: emergency vehicles first, then vehicles on the main road, then first-come-first-served.

What is a risk of rules like "support always wins" or "latest timestamp wins"?
?
The losing update is silently discarded, and timestamp rules depend on synchronized clocks. Resolutions should be logged.

What is negotiation or consensus conflict resolution?
?
Agents actively communicate to reach a resolution, e.g. by voting or proposing alternatives. It is more common in academic or highly complex coordination.

Why is negotiation between LLM agents risky?
?
It is slow and costly, and agents can persuade each other of something false. Persuasion isn't correctness.

Why must rollback and retry redo the whole operation rather than just the final write?
?
The new state may change the right decision, so the agent must re-evaluate from the fresh data rather than reapply its old change.

What failure mode does unbounded rollback and retry risk under contention?
?
Livelock: agents keep colliding and retrying without progress. Cap retries, add backoff and jitter, then escalate.

When should a conflict be escalated to a human?
?
When it is critical, ambiguous, or can't be resolved automatically.

Why do even sequential agent workflows need re-verification?
?
External systems can change data between when an agent reads it and when it acts, so acting without re-checking risks using stale data.

What is the time-of-check to time-of-use gap, and why is it wider for agents?
?
The window between checking a condition and acting on it, during which the data can change. An LLM step in between stretches it from milliseconds to seconds.

Why does adding an LLM step to a read-modify-write cycle raise the conflict rate?
?
The chance of another write arriving grows with the length of the window, so a seconds-long LLM step makes conflicts far more likely than a millisecond database update.

What does eventual consistency mean for agents?
?
Different agents may briefly hold different views of the state, which converge over time. That is acceptable for some decisions but not for ones like "is this seat still free".

How does shared state or an event bus create a security risk between agents?
?
A compromised or prompt-injected agent can publish misleading events or write bad state that other agents trust. Publishing and write rights should be authorized by role.

How should concurrency handling in a multi-agent system be tested?
?
Run agents truly in parallel on the same records, inject delays between read and write to force interleavings, and check for lost updates and correct resolution.
