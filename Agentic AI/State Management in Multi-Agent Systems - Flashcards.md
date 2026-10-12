---
title: "State Management in Multi-Agent Systems - Flashcards"
type: flashcards
source: "[[State Management in Multi-Agent Systems]]"
created: 2026-10-10
tags:
  - flashcards
---

#flashcards/agentic-ai/multi-agent-state

What problem does the "amnesiac customer service agent" analogy illustrate?
?
An agent without state forgets everything between turns, so users must start from scratch each time. Multi-step tasks need memory, and that memory is state.

What mental model does the lesson use for state in a multi-agent system?
?
A shared project dashboard or centralized logbook that records what has happened, the current status, and what has been gathered, so any agent can get up to speed.

What is state?
?
The information a system stores and maintains about the status of a process or interaction at a given time.

What is state management?
?
The techniques and processes for tracking, updating and persisting state within a system.

What is ephemeral state?
?
Temporary state that exists only for one session or conversation, such as chat history.

What is persistent state?
?
State saved to a database or file that lasts across multiple sessions.

What is the difference between conversation-level and system-level state?
?
Conversation-level state is what's happening right now (usually ephemeral). System-level state is what should be remembered for the future (persistent).

What key design decision must you make about every piece of state?
?
Whether it is temporary information that can be discarded or critical data that must be preserved.

Why does the lecture call stateful orchestration "context is king"?
?
Agents almost never work in isolation. They need information gathered earlier in the process, and the orchestrator must manage that shared state and pass along the relevant pieces.

What are the orchestrator's two jobs regarding shared state?
?
Manage the shared state, and pass each agent the relevant pieces it needs.

Why shouldn't an orchestrator pass its entire state to every worker agent?
?
Each worker needs only the context for its task. Minimal context saves tokens, keeps the model focused, limits data exposure, and makes each worker's inputs explicit.

What happens to agents when state isn't managed properly?
?
They "fly blind". For example, a quoting agent can't apply customer discounts without the customer ID, and a fulfillment agent can't ship without the address.

What four mechanisms can carry context from an orchestrator to a worker agent?
?
Direct function or method arguments, a bundled message object, a shared state object managed by the framework (as in graph-based systems), and tool-call arguments.

How does orchestration-level error handling relate to tool-level error handling?
?
It is the next layer up. Tools catch and report their own errors, and the orchestrator decides what the whole workflow does next.

What is retry logic, and what kind of errors is it for?
?
Trying a failed step again, usually after a delay. It is for temporary (transient) issues such as network blips or rate limits.

What is exponential backoff?
?
Increasing the delay between retries, typically doubling it (e.g. 1 s, 2 s, 4 s), so a struggling service gets time to recover.

Why add random jitter to retry delays?
?
So many clients that failed at the same moment don't all retry in lockstep and overload the service again.

Why shouldn't permanent errors be retried?
?
Retrying can't fix them (e.g. a bad request or an auth failure). It only wastes time and money and delays the real failure handling.

What makes it safe to retry a step that has side effects?
?
Idempotency: the operation has the same effect whether it runs once or several times, often enforced with idempotency keys.

What is a fallback or alternative path in failure handling?
?
Plan B when retries fail or the error is permanent: route to a different agent, use a simpler backup tool, or branch the workflow.

What is graceful failure reporting?
?
When a workflow truly can't proceed, it terminates cleanly and reports the failure, with clear context, to the user or system that made the request, instead of crashing silently.

What is a compensating action?
?
An action that undoes an earlier step's persistent change when a later step fails. For example, refunding a charge when service provisioning fails.

Why do multi-agent workflows that modify external state need compensating actions?
?
They aren't atomic. Without undoing completed steps, a failure leaves the system inconsistent, e.g. a customer charged for a service they never received.

What distributed-systems pattern pairs each workflow step with a compensating action?
?
The saga pattern. On failure, the compensations for completed steps run in reverse order.

When should an orchestrator escalate to a human?
?
When an error is too complex, ambiguous or critical to handle automatically.

What should a human-escalation ticket contain?
?
Everything needed to act without reconstructing the run: the input data, intermediate results, and error logs.

How does the tutoring example demonstrate persistent state?
?
The student's mastered concepts, weak areas and preferences are loaded from a database at session start, so the tutor resumes where it left off. Progress is saved continuously, so an interrupted session can resume.

What four questions does the lecture say to keep asking when designing state?
?
What information needs to be remembered? Where does the real truth live? How will we ensure consistency if something fails? How will we handle historical queries?

Why is it risky to treat the orchestrator's state as the source of truth?
?
It is a copy of facts held in systems of record, and copies go stale. Volatile facts should be re-read from the real source before acting on them.

Why should state record what actually happened rather than what an agent intended?
?
If they differ (e.g. a decision was capped by limited resources), state that records intent diverges from reality and misleads later decisions.

How does an append-only event log help with historical queries?
?
It keeps every change rather than overwriting, so you can audit, explain past agent decisions, and rebuild state after a crash.

How should orchestration failure handling be tested?
?
By deliberately injecting faults (timeouts, permanent errors, failures after a side effect) and checking that retries are bounded, compensation runs, and escalation fires with full context.
