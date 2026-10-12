---
title: "Multi-Agent RAG - Flashcards"
type: flashcards
source: "[[Multi-Agent RAG]]"
created: 2026-10-10
tags:
  - flashcards
---

#flashcards/agentic-ai/multi-agent-rag

What is Retrieval-Augmented Generation (RAG)?
?
Providing an LLM with external knowledge from a data source before it generates a response.

What limitation of single-source RAG motivates Multi-Agent RAG?
?
Complex questions often need several diverse sources (papers, news, databases, APIs), and a single agent or pipeline struggles to query all of them well.

What mental model does the lesson use for Multi-Agent RAG?
?
A specialist research team: expert researchers for each source, a team lead who assigns tasks, and a writer who combines the findings into one report.

What are the four roles in a Multi-Agent RAG system?
?
Specialized retrieval agents, a retrieval coordinator, a synthesis agent, and (optionally) re-querying or gap-analysis logic.

What is a specialized retrieval agent?
?
An agent designed and equipped with tools to retrieve information from one specific data source, such as a SQL database, a vector store, or a web search API.

Besides retrieving, what else should a specialized retrieval agent contribute?
?
Interpretation and context for its domain, such as noting a study's methodology limitations or a trial's patient outcomes.

What does the retrieval coordinator do?
?
It analyzes the user query (possibly with an LLM call), decides which specialists are needed, delegates retrieval tasks (often in parallel), and collects the results.

What does the synthesis agent do?
?
It combines varied retrieved results (database rows, text snippets, article summaries) into a single coherent answer.

What is a knowledge gap in Multi-Agent RAG?
?
Information missing from the initial retrieval that is needed to fully answer the query.

What does gap analysis (re-querying) logic do?
?
It analyzes the initial results, identifies missing pieces, and triggers targeted follow-up queries to the specialist that owns the missing data.

Which components can perform gap analysis?
?
The retrieval coordinator or the synthesis agent.

How does team-level gap analysis extend the agentic RAG retrieve-reflect-retry loop?
?
Instead of one agent reformulating its own query, the team inspects the combined evidence and sends a targeted follow-up to the right specialist.

What workflow pattern does Multi-Agent RAG apply to retrieval?
?
Orchestrator-workers: the coordinator is the orchestrator, the specialists are workers (often run in parallel), and the synthesis agent is the synthesizer.

Why does Multi-Agent RAG improve "expert querying"?
?
Each agent's prompt and tools can be tuned for one source (efficient SQL, advanced vector search, web-search API quirks), which is hard to achieve in one generalist agent.

Why is Multi-Agent RAG especially strong for mixing data types?
?
Separate specialists handle structured data (records, figures, inventory) and unstructured text (documents, web pages, news), which a single RAG pipeline often struggles to combine.

What is "orchestration flexibility" in Multi-Agent RAG?
?
The coordinator calls only the specialists a query needs: one for a simple lookup, several in parallel for a complex comparison.

Which specialist would a coordinator call for a simple stock-level question?
?
Only the database agent.

When does a RAG system likely need a multi-agent architecture?
?
When it must go beyond document retrieval into databases, APIs, or several specialized sources. This is common in enterprises that combine internal and external data.

How does Multi-Agent RAG differ from a single agent that routes between RAG tools?
?
Each source gets its own agent with its own multi-step reasoning, a coordinator delegates (often in parallel), a separate agent synthesizes, and gap analysis can run follow-up rounds.

How does querying more independent sources affect the chance of finding a needed fact?
?
Coverage rises as one minus the product of each source's miss probability, so several moderately good sources together cover far more than one.

Why doesn't more retrieval coverage guarantee a better answer?
?
More sources also bring more wrong or contradictory evidence. Final quality depends on faithful synthesis.

What should a synthesis agent do when sources contradict each other?
?
Surface the conflict and weigh sources by trust (e.g. peer-reviewed over press release), rather than blending them into a bland average.

Why is specialist interpretation a reliability risk?
?
Each hop is another LLM transformation that can drop caveats or add unsupported claims, and errors compound across hops.

Why should source identifiers be carried through every hop?
?
To preserve provenance, so each claim in the final answer can be traced and cited back to its original source.

What controls the cost of a Multi-Agent RAG system?
?
The number of specialists called, each specialist's internal loop, and the number of gap-analysis rounds. Accurate routing and a round cap are the main levers.

How does parallel fan-out affect latency in Multi-Agent RAG?
?
Latency is set by the slowest specialist rather than the sum of all of them, but cost still scales with every agent called.

Why is Multi-Agent RAG a prime target for indirect prompt injection?
?
Web and news specialists bring untrusted text into the system, and the synthesis agent reads all of it, so injected instructions can steer the final answer.

What guardrail should a SQL retrieval agent have?
?
Read-only credentials and restricted queries, so retrieval can't modify data or expose more than it needs.

At what layers should a Multi-Agent RAG system be evaluated?
?
Routing (right specialists chosen), per-specialist retrieval quality, gap detection on deliberately incomplete results, and synthesis faithfulness with surfaced conflicts.
