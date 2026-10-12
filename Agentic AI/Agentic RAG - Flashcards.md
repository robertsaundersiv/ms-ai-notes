---
title: "Agentic RAG – Flashcards"
type: flashcards
source: "[[Agentic RAG]]"
created: 2026-10-05
tags:
  - flashcards
---

#flashcards/agentic-ai/agentic-rag

What is passive (basic) RAG?
?
A fixed pipeline that takes a query, retrieves a few chunks once and generates an answer, with no check on relevance and no retry.

What is agentic RAG?
?
RAG in which the agent controls retrieval as part of its reasoning: it decides when and what to retrieve, evaluates results, finds gaps, reformulates queries and retries or switches tools before answering.

What is the core loop of agentic RAG?
?
Retrieve, reflect, retry: gather evidence, assess whether it is enough, and search again differently if it isn't.

What four steps make up the agentic RAG feedback loop?
?
Assess whether documents are relevant, identify missing information, reformulate the query if needed, and repeat retrieval or adjust strategy before answering.

Why is the main shift in agentic RAG about behavior rather than tools?
?
The key change is that the agent self-monitors, checking and improving its retrieval instead of treating it as a black box.

In the Zillow case, why was the passive answer shallow?
?
It faithfully summarized documents about market volatility but missed what the algorithm did, the feedback loop from Zillow's own purchases, and the business pressures.

What did the agentic agent do differently in the Zillow case?
?
It noticed the documents didn't explain the algorithm's behavior, reformulated toward technical and strategic flaws, retrieved analyst and investigative sources, and built a multi-factor explanation.

What feedback loop contributed to Zillow Offers' failure, according to the lesson?
?
Zillow's own aggressive pricing and purchases distorted the market data its model relied on.

What three planning decisions does an agentic RAG agent make?
?
When to retrieve (including skipping it), what to retrieve first, and how to integrate retrieved context across steps.

When can an agentic RAG agent skip retrieval?
?
When the input already contains enough context to answer.

What reflection heuristics can an agent use to judge retrieved passages?
?
Whether they contain the question's entities or keywords, whether they directly answer the what or why, whether every claim can be backed by a source, and whether anything is contradictory or outdated.

What are two ways to implement reflection in agentic RAG?
?
Have an LLM score each passage, for example on whether it supports the answer, or have the generator first list what it knows and what is still unclear before answering.

Are agentic RAG reflection checks trained classifiers?
?
No. They are heuristics, imperfect but useful, often guided by prompts or scoring models.

What is query reformulation?
?
Rewriting a search query after weak results by making it more specific, extracting keywords, simplifying it, or splitting it into sub-questions.

What is a tool pivot in agentic RAG?
?
Switching to a different source or tool, such as web search, another database or a summarizer, when the current retrieval isn't helping.

Why does retrying the same query rarely help?
?
The same query on the same index returns the same results, so each retry must change the query, the retriever or the source.

If each retrieval round independently succeeds with probability r, what is the chance of success within n rounds?
?
1 − (1 − r)^n, though real rounds are correlated, so actual gains are usually smaller.

Why does agentic RAG need stop conditions?
?
Without them it can loop indefinitely, raising cost and latency. Common stops are all gaps filled, a round cap, no new evidence, or all tools tried.

What do faithfulness and relevancy measure in RAG evaluation?
?
Faithfulness is whether the answer is supported by the retrieved context. Relevancy is whether the context and answer address the question.

Why can a faithful answer still be a bad answer?
?
It may be fully supported by the retrieved context while missing key information, so coverage of the question must also be checked.

What is the router-to-planner spectrum in RAG agents?
?
A range from simple routers that pick a retriever to full planners that decompose questions and use multiple tools, trading off cost, latency and intelligence.

Why put a router in front of an agentic RAG system?
?
Simple questions can go to cheap passive retrieval while only complex ones get the costly reflective loop, keeping average cost low.

Why is the reflection step the weak link of agentic RAG?
?
The loop works only if the agent can judge relevance and sufficiency correctly, and LLM self-assessment can be overconfident or never satisfied.

How can retrieved documents attack an agentic RAG loop?
?
Injected text can redirect queries, trigger pivots to attacker sources or claim no further search is needed, so tool choice and budgets must be enforced in code.

What should an agentic RAG agent do when its budget runs out before all gaps are filled?
?
Answer with what it has and explicitly state the remaining gaps rather than inventing content.
