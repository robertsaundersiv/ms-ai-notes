---
title: "Agents and Databases – Flashcards"
type: flashcards
source: "[[Agents and Databases]]"
created: 2026-10-05
tags:
  - flashcards
---

#flashcards/agentic-ai/databases

Why is private structured data especially valuable to agents?
?
It holds the organization's real records, such as tickets, customers, orders and inventory, which public sources can't reach and which agents need in order to do real work.

Why can't web search answer "What is the status of ticket #3042"?
?
The status lives in a private internal database or CRM behind authentication, not on the public web.

What does it mean for an agent to write to a system of record rather than just reply?
?
It actually inserts or updates the relevant database row to record the work, instead of only saying "done" in chat.

What are relational databases best suited for in agent use?
?
Exact, structured queries over tables with defined schemas, such as customer records, transactions and inventory.

How do NoSQL document databases differ from relational ones?
?
They store flexible, document-oriented records without a fixed table schema. They are useful, but less common for direct agent integration.

What do vector databases store, and what kind of query do they answer?
?
Embeddings of content. They return the nearest neighbours by similarity, meaning items close in meaning even without matching words.

What is text2SQL?
?
Translating a natural-language question into a SQL query. It is a set of practices and techniques, not a single library.

What three things must an agent handle to do text2SQL well?
?
Understand the schema, handle filters and date ranges correctly, and avoid dangerous or ambiguous queries.

Why is hard-coding a date a poor way to answer "how many signed up this week"?
?
It is only correct for one week. Relative date logic is needed, and the ambiguity between calendar week and last seven days should be resolved or stated.

Why feed database error messages back to the model?
?
They tell it what was wrong, such as a missing column, so it can correct the query on the next attempt.

What schema context helps an LLM write correct SQL?
?
Relevant table and column definitions, column descriptions, sample or allowed values, and verified example question-and-query pairs.

Why must database guardrails be enforced in the database rather than only in the prompt?
?
A prompt rule is a request the model can misread or be manipulated past. Database permissions are enforced regardless of what the model generates.

What is the principle of least privilege for agent database access?
?
Give the agent's database role only the minimum permissions it needs, such as read-only for querying and narrow grants for specific writes.

Why prefer fixed tools for writes and text2SQL for reads?
?
Writes are where mistakes become incidents and usually form a small known set, while reads benefit from flexibility and are lower risk.

What lesson does the "delete John Doe" example teach?
?
An agent should flag or suggest action, not take destructive steps on its own. Destructive operations need constraints, validation and human approval.

Name four layers of guardrails for agent database access.
?
Any four of: least-privilege roles, table and column allow-lists or row-level security, SQL parsing and statement allow-lists, limits and timeouts, fixed write tools with transactions, human approval, audit logging.

Why can a text2SQL answer be wrong even when the query runs successfully?
?
Running proves only syntax and permissions. Wrong tables, filters or joins still return plausible numbers, so results must be checked against expectations or reference answers.

How does compounding error affect text2SQL reliability?
?
Each stage, such as table choice, filters, aggregation and interpretation, must be right, so overall correctness is the product of per-stage reliabilities.

Why are database rows still untrusted input for an LLM?
?
Text fields such as ticket bodies were written by people and can contain injected instructions, so they must be treated as data, not commands.

What does "RAG is a pattern, not a tool" mean?
?
RAG is retrieving context to improve generation. The retrieval can use SQL, keyword search, vector search or a combination, so a vector database is optional.

What is hybrid retrieval?
?
Using structured filtering (SQL or metadata) to narrow candidates, then ranking them semantically with vector search.

Why does hybrid retrieval often beat either method alone?
?
SQL handles exact constraints such as dates, categories and permissions, while vectors handle meaning, and filtering first also shrinks the search space.

When should an agent route a question to SQL instead of vector search?
?
When it asks for exact facts such as IDs, statuses, counts or date ranges, where there is one correct answer rather than a similarity ranking.
