---
title: "MS AI Daily – 2026-10-06"
type: podcast
created: 2026-10-06
duration_min: 20
covers:
  - "[[Retrieval-Augmented Generation]]"
  - "[[Agentic RAG]]"
  - "[[Agents and Databases]]"
  - "[[Web Search and Browsing for AI Agents]]"
  - "[[Model Context Protocol]]"
  - "[[MCP Specification 2026 – Changes Since March 2025]]"
  - "[[Agent State Management]]"
  - "[[Orchestrator-Workers Workflow]]"
  - "[[Implementing LLM Feedback Loops]]"
  - "[[Model Predictive Control (MPC)]]"
  - "[[Marketing Director Prompt Library]]"
  - "[[ReAct prompt Samples]]"
  - "[[Sequential Prompting]]"
  - "[[APIs in AI Systems]]"
tags:
  - podcast
  - review
---

# MS AI Daily – 2026-10-06

![[MS AI Daily - 2026-10-06.mp3]]

> [!abstract] In this episode
> Retrieval as a reasoning loop: why a perfectly faithful RAG answer can still be shallow (the Zillow Offers case), why retries only help when something changes, and how SQL, vector and web sources each need their own guardrails. Then MCP's 2026-07-28 shift to stateless requests, explicit handles and Multi Round-Trip Requests, tied back to agent state and stateless model APIs.

## Segments
- **Cold open:** faithful but shallow, from [[Agentic RAG]]
- **Deep dive, part 1 (retrieval as a loop across sources):** [[Retrieval-Augmented Generation]], [[Agentic RAG]], [[Agents and Databases]], [[Web Search and Browsing for AI Agents]]
- **Deep dive, part 2 (MCP goes stateless):** [[Model Context Protocol]], [[MCP Specification 2026 – Changes Since March 2025]]
- **Rapid review:** [[Agent State Management]], [[Orchestrator-Workers Workflow]], [[Implementing LLM Feedback Loops]], [[Model Predictive Control (MPC)]], [[Marketing Director Prompt Library]]
- **Blast from the past:** [[ReAct prompt Samples]], [[Sequential Prompting]], [[APIs in AI Systems]]

> [!warning] Corrections and caveats raised in the episode
> - [[Agent State Management]]: the token-cost formula sums $T_0 + i\,m$ from $i = 1$, but the note's own self-test and [[APIs in AI Systems#^quadratic-cost]] use $T_0 + (i-1)\,m$. Both are quadratic, but the exact totals differ. Prefer the $(i-1)$ form.
> - [[Agents and Databases#7. Hybrid Retrieval – Structure Plus Meaning]]: the 50× figure applies to brute-force scans. With approximate (especially graph-based) indexes, very selective filters can reduce recall or need a filtered-search mode, so benchmark it on your own data.
> - [[Sequential Prompting]]: the original "like CoT" definition is clearer stated as: CoT puts its steps inside one response, while sequential prompting uses separate prompts you can inspect.
> - [[MCP Specification 2026 – Changes Since March 2025]]: the revision is recent and SDK support is still catching up. Check versions before you build on it.

## Think about it
You're building an agentic RAG assistant that uses MCP tools to query a ticket database, and those tools return handles such as a result-set ID. Your orchestrator summarizes old conversation turns to control quadratic token costs. Where in your architecture should those handles live? What should happen when a reflection loop retries with a different query? And how would you detect that a summary silently dropped something the agent still needed?

> [!quote]- Transcript
> **Marcus:** Here's a puzzle to start the day. Your RAG system answers a question. Every sentence in the answer is backed by a retrieved document. A faithfulness checker gives it a perfect score. And the answer is still not good enough. How?
>
> **Jess:** Okay, I'm hooked. Bad documents?
>
> **Marcus:** Nope. Good documents, accurately summarized. We'll get to why that's still a failure. Welcome to MS AI Daily for Tuesday, October sixth, twenty twenty-six. I'm Marcus.
>
> **Jess:** And I'm Jess. So what's on the board today?
>
> **Marcus:** Big retrieval day. We'll connect plain RAG, agentic RAG, agents talking to databases, and web search into one picture, which is really about retrieval as a reasoning loop with multiple sources. Then we'll look at the Model Context Protocol and how its twenty twenty-six revision went stateless. After that, a rapid review of agent state, orchestrator-workers, your feedback loop lab, model predictive control, and the marketing prompt library. Then a quick blast from the past with ReAct prompts, sequential prompting, and APIs.
>
> **Jess:** That's a lot of plumbing.
>
> **Marcus:** It's agent plumbing week. Bring a wrench.
>
> **Marcus:** Let's start with the foundation. Jess, in one sentence, what is retrieval-augmented generation?
>
> **Jess:** You retrieve relevant passages at query time, put them in the prompt, and the model answers from that evidence instead of only from its training data.
>
> **Marcus:** Perfect. And your notes have a rule of thumb I really like: most RAG failures are retrieval failures. If the right chunk never makes it into the context, no amount of prompt engineering saves you. The model just guesses, fluently.
>
> **Jess:** So when I debug, I check retrieval first. Something like recall at k, meaning did the right chunk show up in the top k results, before I blame the generator.
>
> **Marcus:** Exactly. Measure retrieval and generation separately. Now, the basic pipeline your notes describe is what the lecture calls passive RAG. Query comes in, retrieve the top few chunks once, generate. No check on whether those chunks were any good.
>
> **Jess:** And agentic RAG puts retrieval inside the agent's reasoning loop. Retrieve, reflect, retry.
>
> **Marcus:** Right. Which brings us back to the cold open. The lecture uses Zillow Offers, Zillow's home-buying program that ran from twenty eighteen to twenty twenty-one. The question is, why did Zillow's algorithm fail? Passive RAG pulls three documents: the shutdown announcement, an article blaming market volatility, and a statement from the CEO about unpredictability. The answer comes back as, the algorithm failed because of unpredictable housing markets.
>
> **Jess:** Which isn't wrong.
>
> **Marcus:** Not wrong. Every claim is supported. Faithfulness is high. But it's shallow. None of those documents explain what the algorithm was actually doing. The agentic version notices that gap, reformulates into questions like, how did Zillow's pricing algorithm affect its own purchases, and finds the deeper story. The model missed local market nuance, Zillow overpaid, business pressure overrode caution, and there was a feedback loop where Zillow's own aggressive buying distorted the market data it was learning from.
>
> **Jess:** So the answer to the puzzle is that faithfulness and coverage are different metrics. Faithful means everything I said is supported. Coverage, or context recall, means I actually retrieved everything I needed to answer the question.
>
> **Marcus:** That's it. And there's a nice irony your notes point out. Zillow's failure is a story about a model acting on its own outputs without enough self-correction. Which is exactly the failure an agentic RAG loop has to avoid in its own design.
>
> **Jess:** Okay, here's my instinct, and tell me if it's wrong. If one retrieval round has, say, a fifty percent chance of finding the evidence, then three rounds gets me to eighty-seven and a half percent. So I just retry three times.
>
> **Marcus:** Your arithmetic is fine. One minus one half cubed. The assumption isn't. That formula assumes the rounds are independent. If you rerun the same query against the same index, you get the same chunks back. Retry number two is a photocopy of retry number one.
>
> **Jess:** So the retries only help if something changes between them.
>
> **Marcus:** Right. Change the query, decompose it into sub-questions, switch retrievers, or pivot to another source entirely. Repeating yourself louder isn't a retrieval strategy. It doesn't work on people either.
>
> **Jess:** And that's where the other notes come in. Switching retrievers could mean going from the vector store to SQL.
>
> **Marcus:** Which is today's databases lecture. The lecture's example is, what's the status of ticket three oh four two? Web search is useless there. That status lives in a private table or a CRM behind a login. The agent needs to translate natural language into a query, which is text-to-SQL, or call a database-backed tool.
>
> **Jess:** And your notes made a point I want to make sure I have right. RAG doesn't require a vector database.
>
> **Marcus:** Correct. RAG is a pattern, not a tool. If your ticket assistant runs a SQL query and answers from the rows, that's RAG. Vectors are for meaning, things like, find tickets similar to, internet keeps dropping at night. SQL is for exact answers. And the strongest systems do both. Filter with SQL on city and date range, then rank by vector similarity within those candidates.
>
> **Jess:** The notes had the math on that. If a filter keeps two percent of a million tickets, a brute-force vector scan goes from a million comparisons to twenty thousand. Fifty times fewer.
>
> **Marcus:** For a brute-force scan, yes. Here's the production footnote, and your notes hint at it. Most real vector databases use approximate nearest neighbor indexes, graph-based ones especially, and very selective filters can interact badly with them. You can lose recall, or the engine may need a special filtered-search mode. So filtering first is still the right idea, but don't assume a fifty-times speedup out of the box. Benchmark it on your own data.
>
> **Jess:** Okay. Now the scary part. Writes.
>
> **Marcus:** The lecture's horror story. The agent notices that John Doe hasn't bought anything in a while. Instead of flagging him for re-engagement, it deletes all his records.
>
> **Jess:** Very efficient churn reduction.
>
> **Marcus:** Technically he can't churn anymore. So the guardrails. Jess, if your system prompt says never run delete, is that a guardrail?
>
> **Jess:** I'd say it's a weak one. It's a request. A read-only database role is a guarantee, because the database enforces it no matter what the model writes.
>
> **Marcus:** Exactly. Put hard limits where the model can't talk its way past them. Your notes lay out a spectrum. Fixed tools, where code owns the SQL. Parameterized templates. Read-only text-to-SQL against curated views. And free-form writes, which you basically avoid. The design rule is text-to-SQL for reads, fixed tools for writes. Most write operations an agent needs are a small, known set anyway. Add a ticket note. Request a refund. Each one narrow, validated, and gated with human approval when it matters.
>
> **Jess:** And a query that runs isn't necessarily a query that's right.
>
> **Marcus:** That's the sneaky one. Your notes do the compounding. If table selection, filters, aggregation, and interpretation are each ninety-five percent reliable, you're at about eighty-one percent end to end. And a wrong SQL query usually doesn't throw an error. It returns a plausible number. So you evaluate with execution accuracy, comparing results against reference answers, not just checking that the query ran.
>
> **Jess:** Then the last pivot option is the web.
>
> **Marcus:** And the web is the least trustworthy source of the bunch. Your web search note says it well: treat every result as untrusted evidence, not truth. The model will repeat a content farm's rumor in confident prose, with a citation attached.
>
> **Jess:** Which is the laundering problem. But here's where I might be wrong. If ten websites say the same thing, that's pretty strong corroboration, right?
>
> **Marcus:** That's the trap, and it's a reasonable instinct. If those ten pages all trace back to one blog post, you have one source wearing ten hats. If each independent source is wrong twenty percent of the time, two independent sources agreeing gets you under four percent risk. But ten copies of one original is still twenty percent. Count origins, not URLs.
>
> **Jess:** And the router end-of-life example nailed that. The forum said the router was end-of-life, dump it. The vendor bulletin said end of sale in twenty twenty-six, but support until twenty twenty-nine.
>
> **Marcus:** Three distinctions saved the day there. The entity, the AX three thousand versus the AX three thousand S. The term, end of sale versus end of support. And the authority, vendor versus forum. The most emphatic sources were the least reliable. Which, honestly, is also true of meetings.
>
> **Jess:** So if I zoom out, these four notes are one architecture. A router decides which source fits the question. A reflective loop checks whether the evidence covers the question. And every source has its own guardrails. Databases get least privilege, the web gets source tiers and a citation gate.
>
> **Marcus:** And your agentic RAG note calls that the autonomy spectrum. Passive RAG, then a router, then a reflective loop, then a full planner. Start at the cheapest level that meets your quality bar, and only send the hard questions up the ladder. One more thing all four notes agree on. Retrieved text is data, never instructions. A ticket body, a web page, or a runbook can contain injected text trying to steer the agent.
>
> **Jess:** Okay, segment two. MCP. I learned it as client sends initialize, server responds, now you have a session. And your notes say that's gone?
>
> **Marcus:** Gone, according to the twenty twenty-six July twenty-eighth revision your notes are based on. Quick refresher first. The Model Context Protocol solves the M times N integration problem. Ten AI apps and fifty services would need five hundred custom connectors. With a shared protocol, you need ten clients plus fifty servers. Sixty pieces.
>
> **Jess:** And servers expose three primitives. Tools are controlled by the model. Resources are controlled by the application. Prompts are controlled by the user.
>
> **Marcus:** Right. Now the big shift. In March twenty twenty-five, MCP was stateful. Handshake, session ID, and the server remembered your version and capabilities. In the twenty twenty-six revision, every request carries its own protocol version and client capabilities in a metadata field. A connection is just a pipe, not a conversation.
>
> **Jess:** Why make that change? It sounds like more overhead per request.
>
> **Marcus:** It is more overhead per request. The payoff is operational. With sessions, a remote server needs sticky routing, meaning every request in a session has to hit the instance that remembers it, or you need a shared session store. Stateless requests let any instance answer any request, behind an ordinary load balancer or a serverless platform.
>
> **Jess:** Wait. That's the same argument as the model API. The model is stateless, so the client resends the conversation every time.
>
> **Marcus:** That's precisely the connection, and your notes make it explicit. Whoever needs the state carries it. So where does state go when a tool needs to remember something across calls, like a shopping cart?
>
> **Jess:** My guess would be the server keeps it, keyed by the connection?
>
> **Marcus:** That's how you'd have done it in twenty twenty-five, and it's exactly what's no longer allowed. Servers must not rely on earlier requests on the same connection. Instead, a tool like create basket returns a handle, a basket ID, and later calls pass it as an ordinary argument. The spec's guidance is that a handle is a name, not a capability. You re-check authorization on every call.
>
> **Jess:** So the model is now carrying the basket ID around in its conversation history. That feels fragile.
>
> **Marcus:** It is, and your notes flag it. If your orchestrator summarizes old turns to save tokens and the summary drops the basket ID, the workflow breaks. The fix is to pull handles out into a dedicated field in agent state that never gets summarized. Agent memory design and MCP tool design are now coupled.
>
> **Jess:** What about servers that used to ask the user something mid-call?
>
> **Marcus:** That's Multi Round-Trip Requests. The server can't send a request to the client anymore. Instead it returns an input-required result with the questions plus an opaque string called request state. The client asks the user, then retries the original call with the answers and that same request state. It's like a web form's hidden field. And because that string passes through the client, it's attacker-controlled input. If it affects authorization or business logic, you sign it.
>
> **Jess:** And sampling got deprecated, right? The server borrowing the host's LLM.
>
> **Marcus:** Deprecated, along with roots and logging. Elicitation, asking the user for input, is now the main client feature. Form mode for structured input, never secrets. URL mode for things like third-party sign-in or payment. One honest caveat: this revision is only a couple of months old as of today. SDKs and servers are still catching up, and many deployments will be dual-era for a while. Check the spec and your SDK's version before you build on any of this.
>
> **Jess:** And the security warning didn't change.
>
> **Marcus:** Nope. MCP standardizes the plumbing, not the trust. Tool annotations like read-only are hints from the server, and a malicious server can label a destructive tool read-only. Tool poisoning, rug pulls, over-broad credentials. Same database lesson: least privilege, enforced outside the model.
>
> **Jess:** Rapid review time?
>
> **Marcus:** Rapid review. Agent state management. Jess, give me the step contract.
>
> **Jess:** Every step takes a state object and returns an updated state object. A router function reads the state and picks the next step. And the state is ephemeral, it's working memory for one run.
>
> **Marcus:** Good. The gotcha: the tool step has to clear pending tool calls, or the router sees them again and re-runs the same tools forever. And a correction for your notes. The token-cost formula in that note sums the base prompt plus i times m, starting at i equals one, but the note's own self-test and your APIs note use i minus one, meaning the first call has no added turns. Both are quadratic, so the conclusion holds, but the exact totals differ. I'd stick with the i minus one version, since it matches the worked examples.
>
> **Jess:** Noted. Orchestrator-workers next. The key difference from parallelization is who decides the split. In parallelization, code fixes the subtasks in advance. Here, the LLM chooses them per input.
>
> **Marcus:** And the gotcha is reliability. With plan adequacy at ninety percent, five workers at ninety-five percent each, and a synthesizer at ninety-five, you land around sixty-six percent. So capping the number of subtasks is a reliability control, not only a cost control. Also notice the planner level of agentic RAG is basically orchestrator-workers applied to retrieval.
>
> **Jess:** Then my feedback loop lab. Which, I'll admit, had a ghost in it.
>
> **Marcus:** The most valuable bug in the vault. Your loop printed eight passing, then twelve passing, then success, and never called the model, because the loop body was commented out and old variables were still sitting in the Jupyter kernel. Lesson: restart and run all before you trust a loop's output. And the conceptual takeaway: the tests are the spec. The model learned about median mode and the value error purely from failing tests.
>
> **Jess:** Model predictive control. Plan over a horizon, apply only the first move, measure, and re-plan.
>
> **Marcus:** And the gotcha is that plans aren't commitments. In your worked example, the plan said the next move would be minus two, but after re-planning from the measured state the controller applied minus two point four. I checked that worked example by hand, by the way, and the numbers hold up. For agents, plan-and-execute with re-planning is the MPC version. Without re-planning, it's open-loop, and it'll happily drive into the wall it saw coming two steps ago.
>
> **Jess:** And the Wi-Fiber marketing library. Prompt four was my favorite. Gate each tower sector as open, limited, or closed before you spend money acquiring customers there.
>
> **Marcus:** Which is a gate check doing business work. Selling into a congested sector creates churn you pay for later. Same idea as a source gate on the web. Decide what's allowed in before you process it.
>
> **Jess:** Blast from the past?
>
> **Marcus:** Blast from the past. Your ReAct prompt samples. The NOC triage agent works through think and act steps, one tool per step, read-only, with every claim citing an observation, and an honest, inconclusive exit after eight steps. Look at that next to today's material. Cite every claim is a citation gate. Read-only is the database role. The step limit is the stop condition from agentic RAG.
>
> **Jess:** And sequential prompting. Separate prompts where each takes the previous output and does one new thing. Done by a human, it's sequential prompting. Done by code, it's prompt chaining.
>
> **Marcus:** One small sharpening for your original definition, which said it's like chain-of-thought with different links. The note itself fixes this, but it's worth saying out loud. Chain-of-thought lives inside one response. Sequential prompting puts the steps in separate prompts you can inspect and fix one at a time. And the research step warning connects straight to today. Ungrounded research at the start of a chain is the shallow-answer problem, upstream.
>
> **Jess:** And APIs in AI systems ties the whole episode together.
>
> **Marcus:** It does. The model API is stateless, so the agent's state is literally the request payload. Today we saw that same idea show up in MCP. And one more gotcha from that note: retries fix transient errors, not systematic ones. Which is the agentic RAG lesson again. If nothing changes between attempts, the retry is wasted.
>
> **Jess:** Okay, wrap us up.
>
> **Marcus:** Three takeaways. One, a faithful answer can still be a shallow one. Measure coverage as well as faithfulness, and make every retry change something, whether that's the query, the retriever, or the source. Two, enforce limits where the model can't negotiate. That means database roles, fixed write tools, source allow-lists, and signed request state, not instructions in a prompt. Three, statelessness doesn't remove state, it moves it. The model API, the twenty twenty-six MCP spec, and your agent state machine all follow the same rule. Whoever needs the state carries it, so design deliberately for what gets carried and what gets lost.
>
> **Jess:** And the think about it question?
>
> **Marcus:** Here it is. Imagine you're building an agentic RAG assistant that uses MCP tools to query a ticket database, and those tools return handles like a result set ID. Your orchestrator summarizes old conversation turns to control quadratic token costs. Where in your architecture should those handles live, what should happen when a reflection loop retries with a different query, and how would you detect that a summary silently dropped something the agent still needed?
>
> **Jess:** That's a good one. I'll be chewing on that during my commute.
>
> **Marcus:** That's the idea. Thanks for listening to MS AI Daily. Go retrieve something worth reflecting on.
>
> **Jess:** See you tomorrow.
