---
title: "Orchestrating Agent Activities - Flashcards"
type: flashcards
source: "[[Orchestrating Agent Activities]]"
created: 2026-10-10
tags:
  - flashcards
---

#flashcards/agentic-ai/orchestration

What is orchestration in a multi-agent system?
?
Applying techniques that direct and manage agent interactions so the agents achieve a complex goal together.

What metaphor does the lecture use for the orchestrator, and what do the workflow and the shared state correspond to?
?
A conductor of an orchestra. The workflow definition is the script the conductor follows, and the shared state is the sheet music or project status board.

What must an orchestrator do for every delegated task?
?
Send the right task to the right agent at the right time, provide all the context the agent needs to succeed, and listen for the results or errors that come back.

Which orchestrator responsibility does the lecture call "huge", and why?
?
State management. The orchestrator must track overall progress and hold the information agents share, or it can't know what's done or what the next agent needs.

What should an orchestrator have for the case where an agent fails?
?
A plan: for example retry, a fallback agent, an alternative path, graceful degradation, or escalation to a human.

Why should the orchestration layer be designed for flexibility?
?
So new agents and capabilities can be added without redesigning the whole system.

What are the three core orchestration patterns?
?
Sequential processing, parallel execution, and conditional branching.

When is sequential processing the right pattern?
?
When each step builds on the previous step's result, meaning there is a real data dependency.

Give the lecture's example of sequential orchestration.
?
Wi-Fi troubleshooting: a diagnostic agent checks the connection, then a solution agent writes step-by-step instructions, then a verification agent confirms the fix worked.

How should a sequential workflow react when a verification step finds the solution didn't work?
?
The orchestrator uses its tracked state to explore alternative solutions, looping back rather than ending in failure.

When can tasks be run in parallel?
?
When they don't depend on each other's outputs. They run simultaneously and their results are combined afterwards.

Give the lecture's example of parallel orchestration.
?
A market analysis report where news analysis, stock data, and competitor analysis agents run at the same time and their results are merged.

What is conditional branching in orchestration?
?
The orchestrator chooses the next agent(s) based on an agent's output: if X, do Y, otherwise do Z.

Give the lecture's example of conditional branching.
?
E-commerce returns: if the policy agent says "Eligible", call the inventory and refund agents; otherwise call the denial notification agent.

Do real workflows usually use a single orchestration pattern?
?
No. They combine them: some steps sequential, some in parallel with a wait for all to finish, then branching on a result.

Why can't editing and publishing a blog post run in parallel?
?
Publishing depends on the edited text, so it must happen after editing. Only independent tasks like image generation or SEO analysis can run alongside.

What is the first thing to work out before deciding which steps to parallelise?
?
The dependency graph: which steps need which other steps' outputs.

How does parallel execution affect latency compared with sequential execution?
?
Sequential latency is the sum of step times. Parallel latency is set by the slowest branch.

Does running agents in parallel improve reliability or cost?
?
No. If all branches must succeed, success is still the product of their success rates, and every agent still runs and costs the same.

Why should a branching decision be based on a constrained output rather than free text?
?
Free-text variations (e.g. "Eligible" vs "yes") can send the workflow down the wrong path. A fixed set of allowed values makes the branch reliable.

When is a plain-code orchestrator preferable to an LLM orchestrator?
?
When the workflow's steps and order are known in advance. Code is deterministic, cheap and testable. An LLM orchestrator pays off only when the decomposition changes per request.

What are the main scaling risks of a central orchestrator?
?
It is a single point of failure and a throughput bottleneck, and long runs need durable state so a crash can resume rather than restart.

How should an orchestrator be tested separately from its agents?
?
Replace agents with stubs and check that each branch is taken correctly, parallel results merge correctly, and each failure triggers the intended recovery path.

Why does orchestration create a prompt-injection risk?
?
The orchestrator passes one agent's output into the next agent's context, so injected instructions in untrusted data can propagate down the workflow and influence branch decisions.

Why should a gate sit before irreversible actions at the end of a workflow?
?
Errors compound across agents, so a check before side effects like publishing or refunding stops bad output from causing real damage.
