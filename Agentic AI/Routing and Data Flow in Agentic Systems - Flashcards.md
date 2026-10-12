---
title: "Routing and Data Flow in Agentic Systems - Flashcards"
type: flashcards
source: "[[Routing and Data Flow in Agentic Systems]]"
created: 2026-10-10
tags:
  - flashcards
---

#flashcards/agentic-ai/routing-data-flow

What is routing in a multi-agent system?
?
Directing messages or tasks to the appropriate agent, or group of agents, within the system. It decides the path.

What is data flow management?
?
Managing the data payload as it moves between agents: enhancing, filtering or transforming it so it's in the right format for the receiver.

How do routing and data flow differ?
?
Routing decides where a message goes. Data flow decides what shape the message is in when it arrives.

In the mailroom analogy, what do routing and data flow correspond to?
?
Routing is the clerk deciding which department gets each memo. Data flow is translating the memo (e.g. legal jargon into plain English) so the recipient can use it.

What is direct delegation?
?
The orchestrator acts as the router, following a predetermined script (run A, then B, then branch on the result).

When is direct delegation enough?
?
When the workflow is known and scripted, as in many business processes. It is simple, effective and often exactly what you need.

What three situations call for dynamic routing instead of direct delegation?
?
Unscripted incoming messages that must be sorted, a pool of identical agents that needs load balancing, and traffic with mixed urgency.

What is content-based routing?
?
Routing a message based on its content or metadata, to send diverse requests to the right specialist.

What signals can content-based routing use?
?
Keywords, sentiment, data type, metadata tags, and the message's source.

Where is content-based routing typically placed in a system?
?
At the front, sorting incoming requests (e.g. a central customer-service intake) before any specific workflow begins.

Why check cheap signals before using an LLM classifier for routing?
?
Metadata, data type and keywords are fast, cheap and deterministic. The LLM is only needed when they're inconclusive.

What is round-robin routing?
?
Distributing tasks evenly across a pool of similar agents in rotation: 1, 2, 3, 1, 2, 3…

What is the main purpose of round-robin routing?
?
Scaling: when one agent isn't enough, run several identical ones and spread the work among them.

What requirement must agents meet to be pooled with round-robin routing?
?
They must be interchangeable, with the same prompt, tools and capabilities.

How does smarter load balancing improve on basic round-robin?
?
It picks the agent with the smallest current workload or the one idle longest, instead of cycling blindly.

Why does plain round-robin perform poorly for LLM tasks?
?
Task sizes vary a lot, so long tasks can pile up on one agent while others sit idle. The slowest agent then sets the batch time.

What is priority-based routing?
?
Tagging messages with a priority level and processing higher-priority messages before lower-priority ones.

When is priority-based routing most useful?
?
When responsiveness matters for certain tasks, as in financial trading, real-time system monitoring, or emergency response.

Give the lecture's example of priority-based routing.
?
Hospital monitoring: a critical vital-sign alert goes to the alert-notification agent immediately, even while routine hourly status logs are queued.

What is starvation in priority routing, and how is it prevented?
?
Low-priority work never runs because higher-priority work keeps arriving. Aging (raising priority as a message waits) or reserved capacity prevents it.

Why shouldn't message senders set their own priority?
?
Everyone would mark their messages urgent, and attackers could jump the queue. Priority should come from trusted signals like source and type.

Does priority routing increase a system's capacity?
?
No. It shares out waiting time: urgent work gets faster at the cost of longer waits for routine work, especially under high load.

How can the three routing patterns be combined?
?
Content-based routing picks the specialist type, priority orders that type's queue, and round-robin or load balancing picks the specific agent instance.

What are the three data flow operations?
?
Enhancement (adding related information), filtering (removing unnecessary data), and reformatting or transformation (changing structure or data types).

What is enhancement in data flow management?
?
Adding related information to the payload so the receiving agent has the context it needs.

What is filtering in data flow management, and what are its benefits?
?
Removing data the receiver doesn't need. It saves tokens, reduces confusion, and limits data exposure.

What is transformation in data flow management?
?
Changing the payload's structure or data types to match what the receiving agent expects.

What is an impedance mismatch between agents?
?
One agent's output format is incompatible with the next agent's expected input, causing parse failures, crashes or misreads.

Why is it worth cleaning and structuring data between agent steps instead of passing everything along?
?
It prevents impedance mismatches, makes handoffs reliable, and keeps the system maintainable.

What makes agent-to-agent handoffs robust in practice?
?
Schema contracts: the sender emits validated structured data and the receiver declares exactly what it accepts.

What is the risk of using an LLM to transform data between agents?
?
LLM transformations can be lossy, dropping facts or inventing them. Deterministic transforms are preferable, and LLM-made ones should be validated.

How can content-based routing be exploited?
?
A user can write content designed to trigger a privileged or urgent route. Route on trusted metadata where possible and treat content as untrusted.

Why doesn't adding more identical agents always speed up processing?
?
If they share a bottleneck, such as a rate-limited LLM endpoint or a database, the queue just moves to that shared dependency.
