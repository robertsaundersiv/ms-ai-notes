---
title: "Implementing Routing Workflow – Flashcards"
course: Agentic AI (Cd14526) – Course 1
type: flashcards
source: "[[Implementing Routing Workflow]]"
created: 2026-09-28
---

#flashcards/agentic-ai/workflow-patterns/routing-implementation

Flashcards for [[Implementing Routing Workflow]].

What does a routing workflow's set of specialists typically look like?
?
A few agents with narrow, distinct responsibilities, such as product research, customer analysis and pricing strategy, each reached by its own route.

What are the two parts of a router?
?
Classification (an LLM call that picks a label) and dispatch (code that calls the specialist matching that label).

What is routing with context gathering?
?
A route that first runs other specialists to collect inputs, then passes their outputs to the final specialist.

Why let callers supply context that a route would otherwise gather?
?
Supplied data is used directly and the matching LLM calls are skipped, which saves cost and latency and avoids generated data where real data exists.

Why does substring matching on classifier output misroute?
?
A free-text reply can mention several route names, and whichever check runs first wins, regardless of what the model meant.

Why does case-sensitive matching cause unrouted queries?
?
A reply that differs only in capitalization matches no route, so the query falls through.

What happens if dispatch code doesn't handle an empty model response?
?
It crashes on the missing value instead of falling back.

What three failure types does fragile dispatch produce?
?
Misrouting, failure to route, and crashing.

What is the general fix for fragile classifier output?
?
A closed set of short labels (including "other"), normalized and matched exactly, with a retry with feedback and then a fallback.

Why prefer a dispatch table (label → handler) over a chain of conditionals?
?
Adding a route becomes one entry, check order can't cause misrouting, and classification can be tested separately from dispatch.

Why should a router return a structured result with a status?
?
So callers can tell a real answer from an unrouted or failed query, instead of showing an error string as if it were an answer.

How do you count the LLM calls on a context-gathering route?
?
One for classification, one per context-gathering specialist, and one for the final specialist.

How does parallel context gathering change a route's latency?
?
Sequential gathering adds every gathering call. Parallel gathering adds only the slowest one, so latency is classify + max(gather) + final.

Why can a route's output be unreliable even when routing is correct?
?
If its inputs come from agents with no real data, they're LLM-generated, and errors propagate into the final recommendation.

Where is model tiering most obviously useful in a router?
?
The classifier, because it only outputs one short label, so a smaller, cheaper model can do it.

Why does a closed label set help against prompt injection?
?
Injected text can't create a new route, because only exact matches to predefined labels are dispatched. It can still steer the choice among existing routes.
