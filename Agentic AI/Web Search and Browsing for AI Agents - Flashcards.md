---
title: "Web Search and Browsing for AI Agents – Flashcards"
type: flashcards
source: "[[Web Search and Browsing for AI Agents]]"
created: 2026-10-05
tags:
  - flashcards
---

#flashcards/agentic-ai/web-research

Why do AI agents need web search or browsing?
?
For information newer than the training cutoff, long-tail facts the model never memorized, verifiable sources, broader coverage than private data, and tasks that happen on websites.

What is the difference between web search and web fetching?
?
Search returns ranked links and short snippets. Fetching retrieves a page's full content so claims can be read and quoted in context.

Why is answering from search snippets risky?
?
Snippets are fragments that can drop qualifiers, negations or context that the full page contains.

What does interactive browsing add over simple fetching, and at what cost?
?
It can click, scroll, fill forms and read JavaScript-rendered pages, but it is slower, costlier and more exposed to injection and unintended actions.

What is web grounding?
?
Basing an answer on retrieved web content, with each claim traceable to a cited source rather than to the model's memory.

What is the core data-quality pitfall of web-enabled AI?
?
The agent can pull stale, low-quality, wrong or adversarial content and repeat it fluently and confidently, often with a citation attached.

Name four categories of bad web data.
?
Any four of: stale pages, content farms, AI-generated filler, misinformation or satire, opinion as fact, wrong-entity pages, out-of-context snippets, circular sourcing, extraction failures, adversarial content.

Why is a citation not the same as verification?
?
A citation is generated text. Unless code checks that the page was fetched and contains the supporting quote, the citation may be fabricated or misattributed.

How can code verify a citation?
?
Require a supporting quote with each citation, then check that the URL was fetched in this run and the quote appears in its text.

What is circular sourcing?
?
Many sources that look independent but all repeat a single original claim, giving false corroboration.

Why must corroboration count origins rather than URLs?
?
Copies of one source aren't independent evidence. Ten pages repeating one wrong claim are as weak as the original.

If each independent source is wrong with probability q, what bounds the chance that k agreeing sources are all wrong?
?
At most q^k, but only if the sources are truly independent.

What is a primary source, and when should it win?
?
The first-hand origin of a fact, such as official docs, original data or the original paper. It wins for facts about the issuer's own products, rules or data.

Why does source authority depend on the claim type?
?
A source can be authoritative for some claims and biased or uninformed for others, such as a vendor on its own dates versus on which product is best.

What signals go into scoring a web source?
?
Authority (tier), recency, independent corroboration and relevance to the exact entity and version.

What should an agent do when credible sources conflict?
?
Report the conflict with each source's claim, prefer the primary or more authoritative source if one exists, and escalate if stakes are high. Never blend them into an unsupported middle answer.

When should a web research agent abstain?
?
When no sufficiently reliable or corroborated evidence supports an answer, especially for high-stakes questions.

Why scale verification effort with the stakes of the question?
?
Each extra fetch and check adds cost and latency, so casual questions can rely on one good source while consequential decisions need primary sources, corroboration or a human.

Why should web content never directly trigger actions?
?
Pages can contain injected instructions, so letting web text drive side effects hands control to whoever wrote the page.

How can a browsing agent exfiltrate private data?
?
Injected instructions can make it fetch an attacker URL carrying private data, or submit that data through a form.

Why shouldn't unverified web claims be written to long-term memory?
?
They resurface later without their source context and look like established knowledge, so errors and attacks persist.

What provenance should agent state keep for web-derived claims?
?
The source URL, origin, tier, date, the supporting quote, and the verification verdict.

Why is web search harder to trust than RAG over a curated corpus?
?
The web index is ranked by someone else's objectives, such as engagement and SEO, not by accuracy for your task.

How does AI-generated content on the web weaken verification over time?
?
Agents increasingly cite text written by other models, so agreement among sources means less and tracing to primary sources matters more.
