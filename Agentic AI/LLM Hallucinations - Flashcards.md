---
title: "LLM Hallucinations – Flashcards"
type: flashcards
source: "[[LLM Hallucinations]]"
created: 2026-09-24
tags:
  - flashcards
---

#flashcards/agentic-ai/hallucinations

What is an LLM hallucination?
?
Fluent, confident output that is not supported by the source, the context, or verifiable world knowledge.

What is the difference between intrinsic and extrinsic hallucination?
?
Intrinsic contradicts the provided context or source. Extrinsic can't be verified from the context and conflicts with, or is unsupported by, world knowledge.

What is the difference between faithfulness and factuality?
?
Faithfulness: the output is supported by the given source. Factuality: the output matches real-world facts.

Why does the next-token training objective encourage hallucination?
?
It rewards plausible text, not true text, and gives no built-in reward for saying "I don't know".

How do accuracy-only benchmarks encourage guessing?
?
A guess sometimes scores and an abstention never does, so guessing maximizes expected score.

What are the layers of a hallucination mitigation stack?
?
Ground (RAG/tools) → prompt for cite-or-abstain → constrain decoding/structure → validate with gates and citation checks → detect and measure → human review for high stakes.

Why is hallucination worse in an agent than in a chatbot?
?
It can trigger a wrong action: invented tools, arguments, or observations change the environment.

What does SelfCheckGPT-style detection rely on, and what does it miss?
?
Made-up facts vary across samples while known facts agree. It misses errors the model makes consistently, and it costs k extra generations.

What is slopsquatting?
?
An attacker registers package names that models tend to hallucinate, so code that installs them pulls in malware.

With 97% per-step correctness over 5 steps, what is the end-to-end correctness?
?
0.97^5 ≈ 0.86.
