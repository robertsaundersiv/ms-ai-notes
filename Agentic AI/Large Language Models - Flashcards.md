---
title: "Large Language Models – Flashcards"
course: Agentic AI (Cd14526) – Course 1
type: flashcards
source: "[[Large Language Models]]"
created: 2026-09-23
---

#flashcards/agentic-ai/llm-foundations

Flashcards for [[Large Language Models]].

What is the pre-training objective of an LLM?
?
Next-token prediction: model the probability of the next token given all previous tokens, trained self-supervised on large text corpora.

What is a token, and roughly how long is one in English?
?
A sub-word unit produced by the tokenizer. About 4 characters or three-quarters of a word.

What is the context window?
?
The maximum number of tokens (prompt plus output) the model can attend to in one call. It is the model's only working memory.

What does post-training add on top of pre-training?
?
Instruction following (SFT), preference alignment (RLHF or DPO), and, for reasoning models, RL on verifiable tasks.

What is the self-attention formula?
?
softmax(QK^T / sqrt(d_k)) V

How does naive attention cost scale with sequence length n?
?
Quadratically, O(n^2).

What does temperature do in sampling?
?
It divides the logits before softmax. Low temperature sharpens the distribution toward the top token; high temperature flattens it for more diversity.

What is the Chinchilla compute-optimal rule of thumb?
?
About 20 training tokens per parameter.

What is the approximate training compute formula?
?
C ≈ 6ND FLOPs, where N is parameters and D is training tokens.

How much memory do a 7B model's weights need at FP16?
?
About 14 GB (7 billion × 2 bytes).

What is the KV cache, and why does it matter?
?
Stored attention keys and values for past tokens. It speeds up generation but grows linearly with context length, consuming GPU memory.

Why do LLM outputs vary across runs of the same prompt?
?
Each answer is sampled from a probability distribution. Even at temperature 0, hardware non-determinism can change outputs.

What is "lost in the middle"?
?
LLMs use information at the start and end of a long context more reliably than information in the middle.
