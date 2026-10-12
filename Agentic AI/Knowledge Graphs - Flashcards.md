---
title: "Knowledge Graphs – Flashcards"
type: flashcards
source: "[[Knowledge Graphs]]"
created: 2026-09-25
tags:
  - flashcards
---

#flashcards/agentic-ai/knowledge-graphs

What is a knowledge graph?
?
Facts stored as entities (nodes) connected by typed relations (edges), governed by an ontology.

What is a triple?
?
A (subject, predicate, object) fact, e.g. (OLT-7, FEEDS, Splitter-3).

What is an ontology in a KG?
?
The schema of allowed entity types and relation types, with their constraints.

What is the difference between RDF and property graphs?
?
RDF stores triples and is queried with SPARQL. Property graphs have key-value properties on nodes and edges and are queried with Cypher or Gremlin.

Where do KGs beat vector search?
?
Multi-hop questions, aggregation, and explainability through explicit paths.

What is GraphRAG?
?
RAG that uses graph structure: an entity graph, community summaries, or traversal from entry nodes found by vector search.

Why must text-to-Cypher output be validated?
?
It is generated code. Use read-only credentials and block write clauses such as DELETE.

What is entity resolution?
?
Merging different mentions of the same real-world entity into one canonical node.
