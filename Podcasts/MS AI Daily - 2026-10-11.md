---
title: "MS AI Daily – 2026-10-11"
type: podcast
created: 2026-10-11
duration_min: 17
covers:
  - "[[Agent Workflow]]"
  - "[[Reflection Report]]"
  - "[[Starter Code Review]]"
  - "[[Agentic AI/python notebooks/agentic-ai-c4-exercises-demos/project/RUBRIC|RUBRIC]]"
  - "[[Agentic AI/python notebooks/agentic-ai-c4-exercises-demos/project/INSTRUCTIONS|INSTRUCTIONS]]"
  - "[[Agentic Frameworks Compared]]"
  - "[[Multi-Agent Architecture Design]]"
  - "[[Agent Evaluation]]"
  - "[[NOC Director Prompt Library]]"
  - "[[Model Context Protocol]]"
  - "[[Evaluator-Optimizer Workflow]]"
  - "[[Structured Outputs]]"
  - "[[Tool Use]]"
tags:
  - podcast
  - review
---

# MS AI Daily – 2026-10-11

![[MS AI Daily - 2026-10-11.mp3]]

> [!abstract] In this episode
> A debrief of the Beaver's Choice multi-agent capstone, built around one theme: rules that matter belong in code, not in prompts. Marcus and Jess cover the architecture, the starter-code traps, the guardrails added after testing, and an honest look at the evaluation results. They also correct one piece of reasoning in the reflection report. Then they place the project on the framework control spectrum and connect it back to topologies, evaluation, evaluator-optimizer loops and structured outputs.

## Segments
- **Deep dive (the capstone):** [[Agent Workflow]], [[Starter Code Review]], [[Reflection Report]], [[Agentic AI/python notebooks/agentic-ai-c4-exercises-demos/project/RUBRIC|RUBRIC]], [[Agentic AI/python notebooks/agentic-ai-c4-exercises-demos/project/INSTRUCTIONS|INSTRUCTIONS]]
- **Deep dive (framework choice):** [[Agentic Frameworks Compared]]
- **Rapid review:** [[Multi-Agent Architecture Design]], [[Agent Evaluation]], [[NOC Director Prompt Library]], [[Model Context Protocol]]
- **Blast from the past:** [[Evaluator-Optimizer Workflow]], [[Structured Outputs]], [[Tool Use]]

## Corrections flagged on air
- [[Reflection Report]]: total assets rising by exactly the gross profit is an accounting identity, because inventory is valued at cost. It doesn't prove that no sale was made below cost. The evidence for that is the price floor enforced in `record_sale_tool`.
- [[Agentic Frameworks Compared]]: the Python environment table says smolagents has "fortnightly releases", but the smolagents SWOT section says there was no PyPI release between 2026-05-29 and the snapshot date. Trust the release gap.
- [[Agent Workflow]]: the sequence diagram loops on `reply_matches_records` "until it passes", with no cap. Check that the implementation limits retries (see [[Evaluator-Optimizer Workflow]], stopping conditions).

## Think about it
Suppose you rebuild Beaver's Choice with the Orchestrator as plain Python that always calls Inventory, then Quoting, then Sales, and the model only handles item matching and reply wording. Which failures from your guardrail table disappear, which survive, and what flexibility do you lose? Is there any kind of customer request where you'd still want a model deciding the order of steps?

> [!quote]- Transcript
> **Marcus:** Here's a scenario. Your sales agent runs its own delivery check, and the check says the order will arrive late. A few seconds later, the same agent records the sale anyway. Nobody hacked anything. The prompt clearly said not to do that. So what went wrong?
> 
> **Jess:** I'm going to guess the answer isn't "write a sterner prompt."
> 
> **Marcus:** It is not. And that exact bug showed up in your capstone project this week. Welcome to MS AI Daily for Sunday, October eleventh, twenty twenty-six. I'm Marcus.
> 
> **Jess:** And I'm Jess. Today feels like a debrief more than a lecture.
> 
> **Marcus:** It is. The main event is the Beaver's Choice Paper Company project: five agents handling quotes, inventory and sales. We'll walk through the architecture, the starter code traps, the evaluation results, and one claim in the report I want to push back on. Then we'll see how your framework comparison explains the choices you made. In the rapid review: multi-agent topologies, agent evaluation, the NOC Director prompt library, and the Model Context Protocol. And in the blast from the past we'll pull in evaluator-optimizer loops, structured outputs, and tool use.
> 
> **Jess:** Okay, set the scene. What does the system actually do?
> 
> **Marcus:** A test harness feeds in twenty customer requests from a CSV. Things like "I need ten thousand sheets of A4 by the fifteenth." An Orchestrator agent maps the customer's wording to exact catalog items, then delegates in order. The Inventory agent decides if each item can be supplied. The Quoting agent prices it. The Sales agent records the sale or rejects the line. A fifth agent, the Business Advisor, reviews things afterward.
> 
> **Jess:** And there's also this orchestration layer, the call your multi agent system function. So that's basically a sixth agent, and you squeezed under the five-agent limit on a technicality?
> 
> **Marcus:** Reasonable suspicion, but no, and the distinction matters. An agent is a model in a loop that decides what to do next. That function decides nothing. It parses dates, opens a per-request context, runs the Orchestrator, and then hands the result to the Advisor. It's plain Python. Same input, same behavior, every time.
> 
> **Jess:** So it's the stage crew, not a cast member.
> 
> **Marcus:** Good way to put it. And that split is the theme of the whole episode: which decisions belong to a model, and which belong to code.
> 
> **Jess:** Speaking of which, the Advisor runs after the reply, not as a tool the Orchestrator can call. Why bother with that?
> 
> **Marcus:** Think about what the Advisor knows. Cash balances, stock counts, margins. If the Orchestrator could call it, those numbers sit in the Orchestrator's context while it writes to the customer. One sloppy sentence and your margin is in a customer email. Running it afterward means it can't leak, by construction. You didn't tell the model to keep a secret. You just never gave it the secret.
> 
> **Jess:** Which is a lot more reliable than asking nicely.
> 
> **Marcus:** Let's talk about what went wrong in testing, because the guardrail table in your workflow note is the best part of this project. First one: the agents dropped or invented dates. One of them used October third, twenty twenty-three.
> 
> **Jess:** Which is before the database even existed, so stock and cash both read as zero.
> 
> **Marcus:** Right. And the fix wasn't a better prompt. Dates are now parsed in code, and the database tools don't take a date argument at all. Jess, why is removing the parameter stronger than validating it?
> 
> **Jess:** Because if the parameter exists, the model can fill it in wrong, and you need a validator that catches every possible bad value. If it doesn't exist, there's nothing to get wrong.
> 
> **Marcus:** Exactly. You shrank the action space. Second failure: the sale recorded after its own delivery check failed. The fix is that the record sale tool re-checks the deadline itself, along with stock and the price floor.
> 
> **Jess:** So the tool doesn't trust the agent that calls it.
> 
> **Marcus:** That's the principle. The model proposes, the tool disposes. The most important rule lives at the point where the write happens, because that's the one place every path has to go through. Third: the Orchestrator skipped the Sales agent and then told the customer they'd been charged forty dollars and fifty cents.
> 
> **Jess:** Which is honestly a very human mistake. "Yeah, I'm sure someone rang that up."
> 
> **Marcus:** Painfully human. The fix uses smolagents' final answer checks. Before the reply goes out, code confirms that the stated total and delivery dates match what's actually in the transactions table, that a no-sale reply says nothing was charged, and that no internal details leak. If the check fails, the agent rewrites.
> 
> **Jess:** Quick check on one of the smaller ones. Max tool threads set to one on every agent. I assumed that was a speed thing, maybe to stay under rate limits?
> 
> **Marcus:** Plausible guess, but it's about correctness. SQLite and parallel writes don't mix well. If two tool calls check stock at the same moment and both see two hundred sheets, both can sell them. That's a race condition. Serializing the calls costs some speed and removes the race. Same idea as the idempotency rule: delegating twice within a request can't book the same sale twice.
> 
> **Jess:** Okay, the starter code review. What were the traps?
> 
> **Marcus:** A few classics. Every database query matches the item name exactly, so "heavy cardstock" reads as zero stock unless you map it to the catalog name first. Create transaction takes the line total, not the unit price. And get stock level returns zero for an item it's never heard of, instead of raising an error.
> 
> **Jess:** That connects to the Tool Use note. Errors should be helpful so the model can correct itself. A silent zero isn't an error at all. It's a confident wrong answer.
> 
> **Marcus:** Exactly right. Zero means "out of stock" and also means "I don't know what you're talking about," and the agent can't tell those apart. That's why your tools reject non-catalog names and list the closest matches. Now my favorite gotcha. Search quote history's docstring says it matches any of the terms. The SQL joins them with AND.
> 
> **Jess:** So more search terms means fewer results, which is the opposite of what the docs say.
> 
> **Marcus:** And the model reads the docstring, not the SQL. Docstrings are prompts now. When the documentation lies, the agent believes it. You handled it by searching on one or two keywords.
> 
> **Jess:** Okay, results. The headline numbers looked good to me. Thirteen of twenty requests changed the cash balance, and twelve sold at least one line.
> 
> **Marcus:** The rubric wanted at least three of each, so you passed comfortably. But I like that the report doesn't stop there. At the line level, sixty lines were requested and only nineteen sold, about thirty-two percent. Forty-eight percent were lost because the item wasn't stocked or wasn't in the catalog. Twenty percent were lost to delivery deadlines.
> 
> **Jess:** And the starter only stocks eighteen of the forty-six catalog items, so the range problem is partly baked in.
> 
> **Marcus:** Partly. Now the pushback. The report says total assets rose from fifty thousand dollars to fifty thousand three hundred nineteen dollars and twelve cents, and that the increase equals gross profit exactly, quote, "no sale was made below cost." Jess, does the first part prove the second?
> 
> **Jess:** Hmm. I'd have said yes. If you'd sold below cost, wouldn't profit come out lower than expected?
> 
> **Marcus:** Lower, yes, but still equal to the asset change. Inventory is valued at cost. So when you sell something, cash goes up by the price, inventory goes down by the cost, and assets change by exactly the profit on that sale. Positive or negative. That equality is an accounting identity. It would hold even if some sales lost money.
> 
> **Jess:** So the evidence for "no sale below cost" is somewhere else.
> 
> **Marcus:** It's the price floor that the record sale tool enforces, cost plus five percent, plus the fifteen percent overall margin. Your conclusion is probably right. The reasoning just needs to point at the right evidence. Worth fixing before a reviewer catches it.
> 
> **Jess:** Fair. What about the request eighteen gap?
> 
> **Marcus:** Good case study. Inventory bought a thousand A4 sheets as a "routine top-up." Top-ups don't go through the deadline check, so the guard that blocks late customer restocks didn't fire. The line was rejected anyway, and fifty dollars became surplus stock.
> 
> **Jess:** So the guardrail was right, it just didn't cover every path to the same write.
> 
> **Marcus:** That's the general lesson. If there are two doors into the same room, a lock on one of them doesn't help much. Also notice the delivery check uses the supplier lead time even for items already in the warehouse. That's partly the starter's fault, since it's the only timing helper, but it overstates delivery times and probably cost you some of those twelve deadline rejections.
> 
> **Jess:** Your suggestion three was to build the customer reply from structured data and only let the model write the greeting.
> 
> **Marcus:** And I think it's the strongest suggestion in the report. Right now the reply check catches problems after they're written. A template prevents them. The report admits one leak got through, "three hundred ninety-nine units available," because the phrase didn't match the leak filter. A blocklist will always miss some phrasing. A template doesn't have that gap.
> 
> **Jess:** Let's bring in the framework comparison. Why smolagents over Pydantic AI?
> 
> **Marcus:** Your reasoning was practical. Managed agents gives you orchestrator-worker almost for free, the tool decorator builds schemas from docstrings the starter already had, it talked to the course proxy with no adapter, and final answer checks gave you that reply gate. You also picked the tool-calling agent over the code agent.
> 
> **Jess:** Because the code agent writes and runs Python, and that sits right next to a database that create transaction writes to.
> 
> **Marcus:** Right. And the comparison note says plainly that smolagents' local executor is not a security sandbox. The note's big idea is a control spectrum. On one end, LangGraph: you own the flow as an explicit graph. In the middle, Pydantic AI and the OpenAI Agents SDK: typed agents you compose. Then smolagents, where the agent loop owns each step. At the far end, CrewAI crews, where the framework owns team behavior.
> 
> **Jess:** And the further right you go, the faster you prototype and the harder it is to debug.
> 
> **Marcus:** Yes. And notice what you did in practice. You started on smolagents, on the right-hand side, and kept dragging pieces left. Dates went into code, deadline checks into tools, reply validation into a check function. You rebuilt the left side of the spectrum by hand.
> 
> **Jess:** Which is kind of an argument for Pydantic AI or LangGraph next time.
> 
> **Marcus:** Possibly. Though the note has the line I'd tattoo on a whiteboard: frameworks package the agent loop, not your consistency guarantees. Lost updates on a shared record are a database problem whatever framework you use. One correction while we're here. In the Python environment section, the note says smolagents has "fortnightly releases." But the smolagents section says there was no PyPI release between the end of May and the snapshot date. Both can't be the current picture. Go with the more specific one, the release gap, and treat "fortnightly" as stale.
> 
> **Jess:** And all those version numbers are a snapshot as of today anyway.
> 
> **Marcus:** Right, they'll be out of date by Tuesday. Re-check before you rely on any of them.
> 
> **Jess:** Rapid review?
> 
> **Marcus:** Rapid review. Multi-Agent Architecture Design. You explain it: orchestrator versus peer-to-peer.
> 
> **Jess:** Orchestrator is hub-and-spoke. One coordinator breaks down the task, delegates in order, and holds the state, like the returns example where no refund happens before the policy check. Peer-to-peer means agents route to each other directly, which fits when you can't script the steps in advance, like diagnosing a network fault. The catch is that the complexity moves around rather than going away. You get dropped tasks, conflicting findings, and no one holding the overall state.
> 
> **Marcus:** Good. Add the numbers. A hub with n agents has about n channels. A full mesh has n times n minus one, over two. Ten agents means ten channels versus forty-five. Here's the gotcha, though. Your notes ask whether a fixed-sequence orchestrator needs to be an LLM at all. Beaver's Choice always runs inventory, then quoting, then sales.
> 
> **Jess:** And the one time the LLM orchestrator improvised, it skipped Sales and claimed a charge.
> 
> **Marcus:** Exactly. Next: Agent Evaluation. Four dimensions: task completion, quality control, tool interaction, system metrics. Three strategies: final response, single step, trajectory. The gotcha is in the M10 demo's evaluator code. It checks the tool's name, not its arguments, and it doesn't penalize extra tool calls. An agent that called a forbidden delete tool and then answered wrong could still get a perfect trajectory score.
> 
> **Jess:** And three perfect scores on one test case is basically zero evidence.
> 
> **Marcus:** That applies to your project too. Twenty requests, one run. If about sixty-five percent of requests change cash, the ninety-five percent margin with twenty samples is roughly plus or minus twenty points. That's fine for a rubric, but too thin to compare two versions of the system. And remember pass to the k. A case that works ninety percent of the time works all five times in a row only about fifty-nine percent of the time.
> 
> **Jess:** The NOC Director Prompt Library next. That one's very close to my day job.
> 
> **Marcus:** Three ideas worth keeping. First, compute, don't ask. Paste the alert logs, do the counting in a spreadsheet or the monitoring tool, and let the model reason about the results. Second, rank problems by subscriber-minutes, because that's what customers actually feel. Third, the model advises and engineers act. Nothing pushes config without a human. The gotcha: the maintenance-procedure reviewer prompt is only the critic half of an evaluator-optimizer loop. The loop only closes if you send the required edits back and review again.
> 
> **Jess:** And the Model Context Protocol. My notes say the twenty twenty-six spec went stateless.
> 
> **Marcus:** Right. As of the July twenty-eighth, twenty twenty-six spec, there's no initialize handshake and no protocol session. Every request carries its own version and capabilities, so any server instance can answer it. State that has to span calls, like a shopping cart, travels as an explicit handle that one tool returns and later calls pass back in. Sampling and roots are deprecated, and elicitation is the main client feature. The gotcha: MCP standardizes the plumbing, not the trust. A tool description is text the model reads as instructions, so a poisoned description is a supply-chain attack.
> 
> **Jess:** Okay, blast from the past.
> 
> **Marcus:** Evaluator-Optimizer Workflow, from about two weeks back. Jess, look at the reply check in your project. Which pattern is that?
> 
> **Jess:** Oh. It's an evaluator-optimizer loop. The Orchestrator generates a reply, the check evaluates it against the records, and if it fails, the agent rewrites with feedback.
> 
> **Marcus:** With a deterministic evaluator, which is the strongest kind, because text can't talk its way past code. Now apply the third element from that note: stopping conditions. Your sequence diagram draws it as "loop until the check passes."
> 
> **Jess:** With no cap. So I should confirm the implementation has a maximum number of retries, and decide what happens when it gives up.
> 
> **Marcus:** That's the homework. Also from that note: when you stop on a limit, return the best attempt and report which criteria still fail. Next, Structured Outputs. One line: schemas guarantee shape, not truth. That's the case for your suggestion three. If Sales returns structured line outcomes, the reply's totals come straight from the data instead of the model's memory. And the wildcard is Tool Use, from the first course. The model proposes a call, and the host validates and executes it. Observations come from the environment, never from the model.
> 
> **Jess:** Which is exactly the forty-fifty bug. The model reported a charge that no tool ever produced.
> 
> **Marcus:** Same failure, three weeks later, in a bigger system. That's why we do review.
> 
> **Jess:** Takeaways?
> 
> **Marcus:** Three. One: put the rules that matter where the write happens. Re-checking the deadline inside the record sale tool beat every prompt instruction you tried, and the request eighteen gap shows that every path to a write needs the same guard. Two: reduce what the model can get wrong. Remove the date parameter, render replies from templates, keep secrets out of context. Prevention by construction beats detection after the fact. Three: make sure your evidence actually supports the claim. An accounting identity isn't proof of a price floor, and one run of twenty requests isn't proof of reliability.
> 
> **Jess:** And the think-about-it question?
> 
> **Marcus:** Suppose you rebuild Beaver's Choice with the Orchestrator as plain Python that always calls Inventory, then Quoting, then Sales, and the model only handles item matching and the reply wording. Which failures from your guardrail table disappear, which ones survive, and what flexibility do you lose? Is there any kind of customer request where you'd still want a model deciding the order of steps?
> 
> **Jess:** Good one to sit with. Thanks, Marcus.
> 
> **Marcus:** Thanks, Jess. That's MS AI Daily. See you tomorrow.

