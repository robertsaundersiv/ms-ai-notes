---
title: "Retrieval-Augmented Generation – Flashcards"
type: flashcards
source: "[[Retrieval-Augmented Generation]]"
created: 2026-09-24
tags:
  - flashcards
---

#flashcards/agentic-ai/rag

What is RAG?
?
A pattern where a retriever selects passages from an external corpus for each query, and the LLM answers conditioned on them.

When do you use RAG, and when fine-tuning?
?
RAG for knowledge (facts, freshness, private data). Fine-tuning for behavior (style, format).

What are the steps of the RAG indexing pipeline?
?
Parse → clean → chunk → embed → store in a vector index with metadata.

What are the steps of the RAG query pipeline?
?
Rewrite query → retrieve top-k (hybrid) → rerank → build a prompt with cited chunks → generate → validate citations.

Why use hybrid retrieval?
?
Dense retrieval handles paraphrase. Sparse (BM25) handles exact IDs, codes and rare terms.

What is the chunk-size trade-off?
?
Small chunks are precise but lose context. Large chunks keep context but add noise.

What is the most common cause of RAG failure?
?
Retrieval failure: the right chunk never reaches the context.

Which metrics separate retrieval and generation quality?
?
Retrieval: recall@k, context precision. Generation: faithfulness and answer correctness.

Where must access control be enforced in RAG?
?
At retrieval time via metadata/ACL filters, before text reaches the LLM.

What is indirect prompt injection in RAG?
?
Instructions hidden in retrieved documents that the model may follow. Treat retrieved text as untrusted data.

What is the formula for cosine similarity?
?
(q · d) / (|q| |d|)
