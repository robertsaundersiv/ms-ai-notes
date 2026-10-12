---
title: "Few-Shot Prompting – Flashcards"
course: Agentic AI (Cd14526) – Course 1
type: flashcards
source: "[[Few-Shot Prompting]]"
created: 2026-09-23
---

#flashcards/agentic-ai/few-shot

Flashcards for [[Few-Shot Prompting]].

What is in-context learning?
?
Performing a new task from instructions and demonstrations in the prompt, without updating the model's weights. The effect lasts for one call.

What is the difference between zero-shot, one-shot and few-shot prompting?
?
Zero-shot has an instruction only. One-shot adds one demonstration. Few-shot (k-shot) adds k demonstrations.

According to Min et al. (2022), what do demonstrations mainly teach a model?
?
The label space, the input distribution and the output format. Label correctness mattered less than expected on many classification tasks.

Why did the A05b all-caps examples fail to produce all-caps output?
?
Examples are soft evidence, not commands. Without an explicit instruction the model only partly followed the pattern. Examples reinforce instructions but don't replace them.

What is majority-label bias in few-shot prompting?
?
The model over-predicts whichever label appears most often in the demonstrations. Fix it by balancing labels.

What is recency bias in few-shot prompting?
?
The model over-weights the label of the last example(s). Fix it by shuffling or testing several orderings.

What is dynamic few-shot prompting?
?
Retrieving the most relevant demonstrations per query (e.g. by embedding similarity) from an example store, instead of using a fixed set.

How does few-shot prompt cost scale with the number of examples k?
?
Linearly, on every call: prompt tokens = instructions + k × average example length + query.

Few-shot vs. RAG vs. fine-tuning: which problem does each fix?
?
Few-shot fixes how the model answers (format, style, labels). RAG fixes what it knows. Fine-tuning permanently changes behavior through the weights.

Why is a dynamic example store a security concern?
?
The model imitates retrieved examples, so anyone who can write to the store can steer behavior. It's an indirect prompt-injection path.

What is few-shot chain-of-thought?
?
Demonstrations that include worked reasoning steps before the answer, showing the model the reasoning structure to follow.
