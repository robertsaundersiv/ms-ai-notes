---
title: "Parallelization Workflow – Flashcards"
course: Agentic AI (Cd14526) – Course 1
type: flashcards
source: "[[Parallelization Workflow]]"
created: 2026-09-27
---

#flashcards/agentic-ai/workflow-patterns/parallelization

Flashcards for [[Parallelization Workflow]].

What is the parallelization pattern?
?
Multiple agents work on different parts of a task, or the same task, at the same time, and their outputs are combined into one result.

Which distributed-computing pattern does parallelization mirror?
?
Scatter-gather: the problem is scattered to multiple workers and their findings are gathered back together.

What are the three parts of the parallelization pattern?
?
Split the main task, have agents perform the subtasks in parallel, and aggregate their outputs into a final coherent result.

Besides speed, what does parallelization offer?
?
Diverse perspectives or solutions, which can make outcomes richer or more dependable.

What is the golden rule of parallelization?
?
Subtasks must be largely independent: no agent should have to wait for another agent's output to do its own work.

What should you do when one subtask's output is another subtask's input?
?
Use a sequential pattern such as prompt chaining for those dependent parts.

What is sectioning or sharding?
?
Splitting a large, divisible input (like a long document or dataset) into chunks that are processed in parallel.

What is aspect-based decomposition?
?
Having different agents analyze distinct, independent aspects of the same subject at the same time, e.g. specs, sentiment, and pricing for one product.

Why run identical tasks in parallel?
?
To generate a range of creative outputs, or to get a more reliable result by having several agents vote on an answer.

What are the four aggregation strategies?
?
Concatenation, comparison and selection, voting or majority rule, and a synthesizer or aggregator LLM.

When is concatenation the right aggregation strategy?
?
When outputs are independent pieces of a whole, such as chapter summaries appended into one document.

What does a synthesizer or aggregator LLM do?
?
It takes multiple, possibly diverse outputs and weaves them into a single, coherent, often more nuanced response.

How is majority voting used as aggregation?
?
Several agents independently perform the same classification or answer, and the most frequent output is chosen.

What is the latency of a parallel stage?
?
Roughly the split time, plus the slowest worker's time, plus the aggregation time, instead of the sum of all workers' times.

Three independent voters are each 80% correct. What is majority-vote accuracy?
?
0.8³ + 3 × 0.8² × 0.2 = 0.512 + 0.384 = 0.896.

Why is real voting accuracy usually lower than the independent-voter formula predicts?
?
Copies of the same model and prompt tend to make correlated errors, so votes are not truly independent.
