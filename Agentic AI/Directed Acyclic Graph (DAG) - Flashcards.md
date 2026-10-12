---
title: "Directed Acyclic Graph (DAG) – Flashcards"
type: flashcards
source: "[[Directed Acyclic Graph (DAG)]]"
created: 2026-09-27
tags:
  - flashcards
---

#flashcards/agentic-ai/dag

What is a directed acyclic graph (DAG)?
?
A graph with one-way edges and no directed cycles. You can never follow edges back to your starting node.

What does an edge u → v mean in an agent task graph?
?
v depends on u. It needs u's output, or must run after u.

What property does every DAG have that makes scheduling possible?
?
A topological order: a linear ordering in which every edge points forward.

How does Kahn's algorithm detect a cycle?
?
It repeatedly removes nodes with in-degree 0. If any nodes remain at the end, the graph has a cycle.

What sets the minimum latency of a DAG run with unlimited parallel workers?
?
The critical path: the longest weighted path from a source to a sink.

Does running DAG branches in parallel improve end-to-end reliability?
?
No. Every node must still succeed, so P is the product of all node success rates. Parallelism only reduces latency.

Five nodes each at p = 0.96. What is the end-to-end success rate?
?
0.96^5 ≈ 0.815, whether they are arranged as a chain or a DAG.

Where should retries and re-planning loops live if the plan is a DAG?
?
In the runtime or orchestration layer, outside the acyclic plan.

Name three checks to run on an LLM-generated DAG plan before execution.
?
Acyclicity (Kahn's algorithm), every dependency refers to a real node, and every tool is on the allow-list.

Why is a ReAct agent's control structure not a DAG?
?
It is a loop that chooses the next action at runtime. Only the trace of a single run is a chain.
