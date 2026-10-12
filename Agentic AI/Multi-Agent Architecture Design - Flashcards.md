---
title: "Multi-Agent Architecture Design - Flashcards"
type: flashcards
source: "[[Multi-Agent Architecture Design]]"
created: 2026-10-07
tags:
  - flashcards
---

#flashcards/agentic-ai/multi-agent-architecture

What three questions does sketching a multi-agent architecture force you to answer?
?
Who talks to whom, what each agent needs to know, and how the overall job gets done.

What is the orchestrator pattern in multi-agent design?
?
A central coordinator receives the task, decomposes it, and delegates subtasks to specialized worker agents, often in a set order. Workers report back to it, and it manages the overall state.

What communication topology does the orchestrator pattern use?
?
Hub-and-spoke: communication flows mainly through the central orchestrator.

What kinds of workflows suit the orchestrator pattern best?
?
Structured, predictable, multi-step workflows where order matters, such as returns, order fulfilment, ticket routing and report generation.

Why is order enforcement a key benefit of an orchestrator?
?
Some steps must not run before others (e.g. no refund before eligibility is confirmed). A central controller guarantees the correct sequence and tracks state.

Why is an orchestrated system easier to debug than freely interacting agents?
?
All coordination and state pass through one place, so you can trace one path instead of reconstructing many peer conversations.

What is the peer-to-peer (direct routing) pattern?
?
Requests go straight to the most qualified agent, and agents communicate directly. After each step, an agent decides which peer to contact next, with no central mediator.

When should you prefer peer-to-peer over an orchestrator?
?
When the sequence of steps isn't known upfront, or when a central orchestrator would become a bottleneck.

What two ways can a peer agent seek help?
?
It can broadcast a request to peers, or route a task directly to a peer it knows has the right expertise.

What becomes harder in peer-to-peer systems as the number of agents grows?
?
Managing the communication flow, making sure tasks aren't dropped, reconciling conflicting information, and tracking the overall state.

Does peer-to-peer reduce system complexity?
?
No. It moves complexity from a central planner into coordination: flow control, dropped tasks, conflicts and distributed state.

What are the main risks of a central orchestrator?
?
It can become a throughput bottleneck and a single point of failure.

What four things must you define regardless of topology?
?
Roles, communication protocols, state management, and data flow.

What is the design principle behind giving each worker one business function?
?
Clear mapping. Each specialist is built for one distinct job, which makes responsibilities, permissions and failures easy to locate.

Why does a fully connected peer mesh scale worse than hub-and-spoke?
?
A mesh has up to n(n-1)/2 pairwise channels, which grows quadratically, while hub-and-spoke has about n. That means more coordination paths and more trust edges.

Why is ticket triage a good fit for the orchestrator pattern?
?
The steps are predictable (classify, gather context, resolve or escalate, notify), order matters, and the ticket's state must be tracked and auditable.

Why is diagnosing an intermittent network fault a good fit for peer-to-peer?
?
The next step depends on findings (e.g. topology decides which device logs to check), so the path can't be scripted, and specialists benefit from exchanging findings directly.

What is a common safeguard against tasks being dropped or looping between peer agents?
?
Give each task an ID, keep a shared task ledger, and add timeouts plus hop or budget limits.

How should inter-agent messages be treated from a security standpoint?
?
As untrusted data. A compromised agent can try to instruct others, so validate messages and give each agent least privilege.
