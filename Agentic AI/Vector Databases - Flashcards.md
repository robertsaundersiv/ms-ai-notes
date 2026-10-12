---
title: "Vector Databases – Flashcards"
type: flashcards
source: "[[Vector Databases]]"
created: 2026-09-25
tags:
  - flashcards
---

#flashcards/agentic-ai/vector-databases

What is an embedding?
?
A learned map from text to a dense vector, where texts with similar meanings land close together.

What does a vector database do?
?
Stores vectors with IDs and metadata, and indexes them for fast k-nearest-neighbour search with filtering and updates.

Why use approximate nearest neighbour (ANN) search?
?
Exact search is O(N·d) per query. ANN gives sub-linear search at a small cost in recall.

How does HNSW work?
?
It builds a layered proximity graph and searches it greedily from the top layer down. Recall is high, but it uses a lot of memory.

Why does hybrid search help?
?
Dense vectors capture meaning but blur exact tokens such as error codes. BM25 catches those exact matches.

What does a reranker do?
?
A cross-encoder re-scores the top candidates from the first retrieval pass, which often gives the biggest quality gain.

What is the float32 memory for N vectors of dimension d?
?
N × d × 4 bytes, before index overhead.

Why must metadata filters be applied at query time in multi-tenant RAG?
?
To enforce access control. Otherwise one tenant's documents can be retrieved for another tenant.

What should be versioned together with the index?
?
The embedding model. Query and document vectors must come from the same model.
