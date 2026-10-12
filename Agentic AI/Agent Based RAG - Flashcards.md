---
title: "Agent Based RAG – Flashcards"
type: flashcards
source: "[[Agent Based RAG]]"
created: 2026-10-06
tags:
  - flashcards
---

#flashcards/agentic-ai/agent-based-rag

How can agentic RAG be built from passive RAG pipelines?
?
Wrap each passive retrieve, augment, generate pipeline as a tool, then let a tool-calling agent decide which tool to call, if any, and with what query.

What is the simplest form of agentic RAG?
?
A router: the agent chooses which knowledge source to query, or none, based on the question and the tool descriptions.

Why give each document source its own collection and tool?
?
Separate sources give the agent something to route between and keep unrelated content from mixing in retrieval results.

What makes an agent route correctly between two retrieval tools?
?
Distinct tool descriptions. Details such as source title, publisher, scope and date are the signal the model uses to choose.

Why is putting a source's publisher and date in a tool description useful?
?
It lets the model judge scope and freshness, for example recognizing that an older report can't answer a question about a later year.

What happens inside a passive RAG pipeline?
?
Retrieve the top passages for the question, build a prompt that combines them with the question, and have the LLM generate an answer.

What is a nested state machine in agentic RAG?
?
A retrieval workflow that runs entirely inside one step of the agent's workflow, such as the tool-execution step.

Why keep clients like the LLM and vector store outside the workflow state?
?
State is copied for snapshots, and clients are hard or impossible to copy, so they are injected as shared resources instead.

What is the risk of computing similarity distances but never using them?
?
The pipeline always answers from whatever came back, even when no passage is actually relevant, instead of saying nothing was found.

What does it show when an agent answers without calling any retrieval tool for an out-of-scope question?
?
Correct abstention: it recognized that none of its sources covers the question rather than forcing an irrelevant retrieval.

Why is abstention without a fallback only half a solution?
?
The user still gets no answer. A fallback such as a guarded web search lets the agent actually find the information.

What is query rewriting in a routing agent?
?
Turning the user's natural-language question into a more retrieval-friendly query, often keyword-focused, before calling the retrieval tool.

Why can't an agent reflect on evidence when its retrieval tool returns only a finished answer?
?
It never sees the passages or relevance scores, so it can't judge relevance, find gaps or cite sources.

What risk comes from stacking two LLM generation layers in RAG?
?
Each layer can drop qualifiers or numbers or add details, so the final answer can drift from the source passages.

What should a retrieval tool return to support reflection and citation?
?
The top passages with source and page identifiers and relevance scores, optionally alongside a short answer.

Why add source and page metadata when indexing documents?
?
It enables citations, filtering and provenance checks, which aren't possible with content-only chunks.

What is a downside of using whole PDF pages as chunks?
?
Pages are arbitrary boundaries: they can split tables or arguments and mix several topics into one embedding.

Why does an agent loop need a step cap even when the prompt says when to stop?
?
Prompt instructions are requests the model may not follow, and only a code-level cap guarantees the loop ends.

Why must an unknown tool name still produce a tool message?
?
Each tool call expects a matching result, and silently skipping it typically breaks the next model request.

What does session memory add to a routing agent?
?
It carries earlier messages in the same session into the next invocation, so follow-up questions keep their context.

How should a routing RAG agent be evaluated?
?
With in-scope, cross-source and out-of-scope questions, measuring routing accuracy, abstention, answer correctness, faithfulness to passages, and tool calls per question, compared against querying every source every time.

What capabilities separate a routing RAG agent from a fully reflective one?
?
Inspecting retrieved evidence, retrying with new queries based on gaps, pivoting to other tool types, decomposing questions and citing sources.
