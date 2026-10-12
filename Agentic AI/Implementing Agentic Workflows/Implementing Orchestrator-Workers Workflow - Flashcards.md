---
title: "Implementing Orchestrator-Workers Workflow – Flashcards"
course: Agentic AI (Cd14526) – Course 1
type: flashcards
source: "[[Implementing Orchestrator-Workers Workflow]]"
created: 2026-09-28
---

#flashcards/agentic-ai/workflow-patterns/orchestrator-workers-implementation

Flashcards for [[Implementing Orchestrator-Workers Workflow]].

What kinds of problems suit an orchestrator-workers implementation?
?
Tasks that break into distinct specialist subtasks you can't fully list in advance, such as multi-part research or a report interpreted section by section.

In the general-contractor analogy, what do the orchestrator and the worker lookup correspond to?
?
The orchestrator is the general contractor who makes the plan and delegates. The worker lookup is the contact list used to find the right specialist.

What is the role of a generic fallback worker?
?
The reliable handyman: it handles any task type that has no specialist, so tasks aren't dropped.

What are the four steps of an orchestrator-workers run?
?
Make the plan, delegate each task to a matching worker, have each worker do its job, and gather the reports into a final result.

What makes a plan format easy or hard to parse reliably?
?
Loose text conventions such as ad-hoc tags or one item per line break easily. A structured format such as JSON, validated against a schema, parses reliably.

Why is fixed-position string slicing a fragile way to parse model output?
?
It assumes exact lengths and layout. Off-by-one errors silently corrupt every value, and formatting variations break it.

Why is a parser that silently returns nothing dangerous?
?
An empty plan means no workers run and nothing reports the failure. Parsers should fail loudly so the problem can be retried or surfaced.

What are the trade-offs between a fallback worker and raising an error for an unknown task type?
?
A fallback keeps the task but may handle it poorly. Raising an error makes the gap visible, but if the error is only printed, the task silently disappears from the result.

Why should a missing tag or field in a worker's reply be treated as a failure?
?
Otherwise the worker's findings are silently blank, and the final result looks complete when it isn't.

Which part of the orchestrator-workers theory do the course scripts leave out?
?
Synthesis. They list the worker outputs one after another instead of combining them into one coherent answer.

Why should the planning prompt list the available worker types?
?
So the orchestrator plans only with types that have a worker, instead of inventing task types that get dropped or misrouted.

What is a plan gate?
?
Pure code that accepts or rejects the plan before execution: valid structure, a bounded number of subtasks, unique IDs, known types, non-empty descriptions, valid dependencies, and no cycles.

What should happen when the plan gate rejects a plan?
?
Re-prompt with the specific error. After a small retry budget, stop with an explicit planning-failed status.

What common plan failure does a retry with error feedback fix?
?
Chatty prose wrapped around the structured plan, such as "Sure! Here is the plan:".

Why should an orchestrator report a run status rather than just text?
?
So callers can tell a full success from a partial result, a planning failure, or total worker failure, and react appropriately.

How do you stop one failing worker from sinking the whole run?
?
Isolate each worker's errors, mark only that subtask as failed, and finish with a partial status.

What are dependency waves?
?
Groups of subtasks whose dependencies are all complete. Waves run in order, and the subtasks within a wave run in parallel.

How does wave grouping detect a dependency cycle?
?
It reaches a point where subtasks remain but none has all its dependencies done.

What should happen to a subtask whose dependency failed?
?
Skip it, record the problem, and tell the synthesizer it wasn't completed.

How does latency grow with dependency waves?
?
Each wave adds only its slowest subtask: planning time, plus the sum of each wave's maximum, plus synthesis time.

Why compute deterministic checks, like out-of-range values, in code rather than with the LLM?
?
Comparisons and arithmetic are exact in code. The LLM should only interpret the results.

What can a fake-LLM test not verify about an orchestrator?
?
Plan quality: whether the chosen subtasks are sensible, complete, and non-overlapping. That needs labeled requests and a live model.
