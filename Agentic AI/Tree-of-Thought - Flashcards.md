---
title: "Tree-of-Thought – Flashcards"
type: flashcards
source: "[[Tree-of-Thought]]"
created: 2026-09-24
tags:
  - flashcards
---

#flashcards/agentic-ai/tree-of-thought

What is Tree-of-Thought (ToT)?
?
A reasoning framework where the LLM generates several candidate thoughts per step, evaluates partial solutions, and searches the tree with pruning and backtracking.

What are ToT's four components?
?
Thought decomposition, thought generator, state evaluator, search algorithm.

Which search algorithms does ToT use?
?
BFS (with beam), DFS with backtracking, beam search.

What does ToT add to chain-of-thought?
?
Multiple candidates per step, evaluation of partial solutions, and backtracking.

How does ToT differ from self-consistency?
?
Self-consistency votes over complete independent paths. ToT evaluates partial states to steer the search.

How many leaves does a full tree with branching k and depth d have?
?
k^d. Pruning and beam width keep it tractable.

What is ToT's main weak point?
?
The state evaluator. If it misjudges partial solutions, the search prunes good branches.

What result did Yao et al. report for Game of 24?
?
GPT-4 solved 4% with CoT vs 74% with ToT (b=5).

When is ToT a poor choice?
?
Simple tasks, latency-sensitive use, or when partial solutions can't be evaluated reliably.

Which control method is ToT's search similar to?
?
Model Predictive Control: simulate candidate futures and pick the best next step. It is also similar to MCTS in RL.
