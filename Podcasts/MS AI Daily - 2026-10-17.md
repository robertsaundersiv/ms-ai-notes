---
title: "MS AI Daily – 2026-10-17"
type: podcast
created: 2026-10-17
duration_min: 18.6
covers:
  - "[[Skate Park Orchestration]]"
  - "[[Smolagents Framework]]"
  - "[[Agentic Frameworks Compared]]"
  - "[[Multi-Agent RAG]]"
  - "[[IT Director Prompt Library]]"
  - "[[Tool Descriptions in Agentic Systems]]"
  - "[[ReAct prompt Samples]]"
  - "[[Model Context Protocol]]"
tags:
  - podcast
  - review
---

# MS AI Daily – 2026-10-17

![[MS AI Daily - 2026-10-17.mp3]]

> [!abstract] In this episode
> One question ties the episode together: who owns the control flow? Marcus and Jess use the skate park exercise's runaway diagnoser, which used about 62% of the input tokens to pick one category, to explain the smolagents loop, its quadratic token cost and p-to-the-n reliability, the control spectrum across six agent frameworks, and Multi-Agent RAG as orchestrator-workers applied to retrieval. The review segments show that older notes on tool descriptions, ReAct prompts and MCP explain most of what went wrong at the skate park.

## Segments
- **Cold open and agenda:** the "every answer looked fine" skate park run, see [[Skate Park Orchestration]]
- **Deep dive: who owns the control flow?**
  - *Soft routing and the looping diagnoser:* [[Skate Park Orchestration]]
  - *Inside the agent loop: final answer as the stop signal, quadratic token growth, p to the n, code agents vs tool-calling agents:* [[Smolagents Framework]]
  - *The control spectrum, and why frameworks package the loop but not your consistency guarantees:* [[Agentic Frameworks Compared]]
  - *Specialists, coordinator, synthesizer and gap analysis; the independence assumption in the coverage math; evaluating each layer:* [[Multi-Agent RAG]]
- **Rapid review:** [[IT Director Prompt Library]] (hours lost vs. ticket count, compute don't ask, the automation screener's determinism check), plus a quick recall of the lesson-code gotchas in [[Smolagents Framework]]
- **Blast from the past:** [[Tool Descriptions in Agentic Systems]] (three skate park bugs explained), [[ReAct prompt Samples]] (guardrails, plus an inconsistency in the few-shot examples), [[Model Context Protocol]] (M×N → M+N, stateless handles, trust)

> [!warning] Corrections flagged in this episode
> - [[ReAct prompt Samples]]: the prompts require a single THINK/ACT message at every step, but the final steps of the config-drift and vulnerability examples show ACT with no THINK. Few-shot examples teach the model to skip reasoning at the end. The `"$MC"` ticker format is also ambiguous; document the format the tool expects.
> - [[Agentic Frameworks Compared]] §10: "2.55 minor releases" should read version 2.55, meaning about 55 minor releases within 2.x (the note's §5 already says this correctly).
> - [[Multi-Agent RAG]] coverage math: not wrong, but it assumes independent sources. Correlated sources, such as outlets rewriting the same press release, make the 93.6% figure an upper bound.

## Think about it
Suppose you rebuild the skate park system for production and move routing out of the orchestrator's prompt and into code, so each category reaches only its own small toolset. Which kinds of customer requests get *worse*, not better, under that design? How would you give those requests a path without going back to every request seeing all nine tools?

> [!quote]- Transcript
> **Marcus:** Here's a puzzle. You run ten customer requests through a two-agent system. Every single reply looks fine. Bookings land, maintenance gets logged, the double-booking gets refused. And yet about sixty-two percent of everything you paid for in input tokens went to the agent doing the easiest job in the building.
>
> **Jess:** The easiest job being what, exactly?
>
> **Marcus:** Picking one word out of a list of seven. A classifier. It called its own tool four to six times per request, with identical arguments, and nobody noticed, because nobody read the log.
>
> **Jess:** That's painful. And it's the skate park exercise, right? I remember thinking that one went well.
>
> **Marcus:** It did go well, if you only grade the answers. That's the whole lesson. Welcome to MS AI Daily for Saturday, October seventeenth, twenty twenty-six. I'm Marcus.
>
> **Jess:** And I'm Jess. So what's on the board today?
>
> **Marcus:** No notes changed in the last two days, so today's deep dive is last week's agent material, all tied together by one question: who owns the control flow? We'll start with the Skate Park Orchestration exercise, go under the hood of the smolagents loop, zoom out to your Agentic Frameworks Compared note, and then see the same patterns again in Multi-Agent RAG. After that, a rapid review of your IT Director Prompt Library, and a blast from the past with the Model Context Protocol, your ReAct prompt samples, and tool descriptions. Those last three end up explaining a lot of what went wrong at the skate park.
>
> **Jess:** Okay, start with the skate park. Remind me of the shape of it.
>
> **Marcus:** A skate park and shop in Nairobi. Two stages. A diagnoser agent sorts each customer request into one of seven categories, things like session booking, skateboard, maintenance, event. Then an orchestrator agent takes the request plus that category and picks from nine business tools: check a booking, add a booking, check inventory, log maintenance, and so on. Classify, branch on the category, run tools in sequence.
>
> **Jess:** So it's the routing workflow. Classify first, then dispatch.
>
> **Marcus:** Right on the front half. But here's the question. Where does the branching actually happen? In the penguin and scientist exercise the hub was Python code. Where is it here?
>
> **Jess:** I'd assume in code too. The diagnoser returns a category, and the glue function sends it to the right place.
>
> **Marcus:** That's the reasonable assumption, and it's wrong for this exercise. The glue function just runs both stages in order. The branching lives in the orchestrator's prompt. There's a list of rules like "for session booking, check availability, then add the booking," and the model reads the rules and decides. All nine tools are visible on every request.
>
> **Jess:** So the category is more of a hint than a route.
>
> **Marcus:** Exactly. Your note calls it soft routing. Flexible, but the model can ignore it. If it decides a maintenance request needs the event tool, nothing stops it. Hard routing would be code: category maintenance gets a sub-agent that can only see the two maintenance tools.
>
> **Jess:** Okay, now the diagnoser. Why would it keep calling the same tool five times? That seems like a strange failure.
>
> **Marcus:** Think about what the tool returned. The submit diagnosis tool basically echoed the category back. From the model's point of view, it submitted, and the world said "yes, maintenance." Did that tell it the job was finished?
>
> **Jess:** Not really. It's like hitting save on a document and getting no confirmation, so you hit save again.
>
> **Marcus:** That's a good analogy, and it's close to what your note suspects. The model gets no signal that it's done, so it keeps submitting until it finally reaches for final answer. Your note lists three fixes, cheapest first. Cap the diagnoser at one or two steps. Have the tool return something explicit, like "Recorded. Now call final answer." Or, the real fix: classification doesn't need an agent loop at all. Make one model call with a constrained enum output.
>
> **Jess:** Let me push back on the cost, though. If it called the tool five times instead of once, isn't that five times the cost? Your note says roughly eighty percent of the diagnoser's tokens were waste, which is about four out of five. So it's linear?
>
> **Marcus:** Close, but it's worse than linear, and this is where the smolagents note matters. Every step re-sends the full history. Step one sends the prompt. Step two sends the prompt plus step one. Step five sends the prompt plus all four previous steps. Your note writes it as total tokens equals n times P, plus s times n times n plus one over two, where P is the fixed prompt and s is what each step adds.
>
> **Jess:** So there's a linear part from the prompt, and a quadratic part from the history.
>
> **Marcus:** Right. With a big system prompt, the linear part dominates early. Let the loop run long and the quadratic term takes over. That's why your note says step caps are a cost control, not just a safety net. Sounds boring, saves your budget.
>
> **Jess:** Let's go under the hood, then. What is smolagents actually doing for me?
>
> **Marcus:** It's the hand-written tool loop from your Building Agents with Tools note, packaged up. The tool decorator turns a function's name, type hints and docstring into the schema the model sees. Then the framework runs the loop: the model emits a tool call, the framework parses it, runs your function, appends the observation, and asks again. It stops when the model calls the built-in final answer tool, or hits the step cap.
>
> **Jess:** So that's ReAct with the bookkeeping done for you.
>
> **Marcus:** Yes. And the only way the agent says "I'm done" is by calling final answer. That's exactly the signal our diagnoser kept missing.
>
> **Jess:** The note mentions two agent styles. Tool calling agent versus code agent.
>
> **Marcus:** The lesson's tool calling agent emits one JSON tool call per step. The code agent writes a Python snippet that calls tools as functions, so it can do several calls in one step. Fewer steps helps both cost and reliability.
>
> **Jess:** And code is more deterministic than free-form JSON, so I'd guess the code agent is also the safer choice?
>
> **Marcus:** That's the trap. It's more expressive, not safer. The code agent executes code the model wrote, so you need a real sandbox. Your frameworks note points out that smolagents' own README says its local executor is not a security sandbox. You'd want Docker or a managed sandbox like E2B or Modal.
>
> **Jess:** Okay, and reliability. That's the p to the n idea?
>
> **Marcus:** Yes. If each step succeeds with probability p and the task needs n steps, end-to-end success is roughly p to the n. At ninety-five percent per step, three steps gets you about eighty-six percent. Ten steps, about sixty percent. Every step an agent adds through autonomy is another roll of the dice.
>
> **Jess:** So a looping diagnoser isn't just expensive. Every extra step is one more chance for it to go wrong.
>
> **Marcus:** Exactly. Now zoom out. Your frameworks comparison note puts six frameworks on one axis: how much control flow the framework owns versus how much you own. Want to try placing a few?
>
> **Jess:** LangGraph is the explicit graph, so you own the flow. CrewAI is role-based teams, so the framework owns more of the behavior. And smolagents is somewhere in between: you write the tools, but the agent loop decides each step.
>
> **Marcus:** Good. Pydantic AI and the OpenAI Agents SDK sit at "typed agent, you compose." npcsh, the shell-first one with agents defined as files, sits near smolagents. And one wrinkle: CrewAI Flows, as opposed to Crews, sit back on the "you own the flow" end. Same vendor, both ends of the spectrum.
>
> **Jess:** And the course keeps pushing production systems to the left.
>
> **Marcus:** "LLM proposes, code disposes." Moving right gets you faster prototypes. Moving left gets you auditability and determinism, at the cost of more code. Now, here's the line from that note I most want you to remember: frameworks package the agent loop, not your consistency guarantees.
>
> **Jess:** Meaning what, concretely? Because Pydantic AI has durable execution, and LangGraph has checkpointers. Doesn't durable state cover things like lost updates on a shared record?
>
> **Marcus:** That's a really natural assumption, and it's the exact distinction the note makes. Durable execution answers "the process crashed halfway, can I resume?" Lost updates are two writers clobbering the same row. That belongs in the database layer, with versions and transactions. Same with the penguin exercise, where history recorded what the agent intended rather than what actually happened. No framework fixes that. It's a design choice: write state after the action is confirmed.
>
> **Jess:** So a checkpoint saves my place in the workflow. It doesn't make my writes correct.
>
> **Marcus:** That's it. And the note maps the skate park problems onto framework features: typed outputs instead of digging through step logs, a single typed call or a deterministic classify node instead of the looping diagnoser, conditional edges instead of soft routing.
>
> **Jess:** Quick question on the version numbers. The note says Pydantic AI is at two point five five, and then somewhere it says "two point five five minor releases." That tripped me up.
>
> **Marcus:** Good catch. That second phrasing is a slip. Version two point five five means about fifty-five minor releases within major version two, which the earlier part of your note gets right. Either way, it moves fast, so pin your versions. Treat the version table as perishable and the control spectrum as durable.
>
> **Jess:** Okay, Multi-Agent RAG. My instinct is it's the skate park pattern pointed at data sources.
>
> **Marcus:** That's a strong instinct. It's the orchestrator-workers workflow applied to retrieval. You have specialized retrieval agents, each owning one data source and its tools: a SQL agent, a vector store agent, a web or news agent, a domain A P I agent like PubMed. A retrieval coordinator analyzes the query and calls only the specialists it needs, often in parallel. A synthesis agent merges everything. And optionally, gap analysis notices what's missing and sends a targeted follow-up.
>
> **Jess:** Gap analysis sounds like the retrieve, reflect, retry loop from Agentic RAG.
>
> **Marcus:** It is, lifted to the team level. Instead of one agent rephrasing its own query, the team looks at the combined evidence and asks the right specialist for the missing piece. Your note's example: the trials agent finds a Phase 1 trial with no results, and the news agent finds a press release claiming success. That's a gap and a contradiction at once.
>
> **Jess:** But how is this different from one agent with a bunch of retrieval tools? That's what Agent Based RAG was.
>
> **Marcus:** Narrower than people expect. Wrapping each source as a tool already gets you source routing. Specialists pay off when each source needs its own multi-step reasoning: writing and fixing SQL, reformulating searches, judging source quality. Cram all of that into one context and it gets crowded.
>
> **Jess:** And the coverage math. Three sources at sixty percent each gets you over ninety-three percent.
>
> **Marcus:** One minus point four cubed, about point nine three six. But notice the assumption: the sources are independent. In practice they often aren't. If four news outlets all rewrote the same press release, you don't have four sources. You have one source with four headlines. So treat that number as an upper bound.
>
> **Jess:** Huh. So more sources raises coverage, but also raises the chance of pulling in something wrong or contradictory.
>
> **Marcus:** And that makes the synthesis agent the quality bottleneck. The failures I'd write on a whiteboard: blandly averaging a peer-reviewed paper with a press release, lost provenance, and indirect prompt injection from web results. The fixes: carry source I Ds through every hop, normalize into a typed schema before synthesis, cap the gap rounds, and keep the SQL agent read-only.
>
> **Jess:** And evaluate per layer.
>
> **Marcus:** Routing, retrieval per specialist, gap detection, then synthesis faithfulness. Your skate park note says the same thing: score the diagnoser's routing on its own, assert the tool trajectory, check the state objects directly, and alert on step budgets. That last one would have caught the looping diagnoser on day one.
>
> **Jess:** Okay, rapid review. IT Director Prompt Library.
>
> **Marcus:** Let's do it recall style. That library has a governing metric. What is it, and why does it matter?
>
> **Jess:** Rank problems by employee hours lost, not ticket count. Blocked time times occurrences. A password reset happens a lot, but a field tech whose tablet won't open jobs is idle for hours.
>
> **Marcus:** That's it. And the gotcha?
>
> **Jess:** Compute, don't ask. Do the counting in a spreadsheet and give the model the results, rather than asking it to do arithmetic over ninety days of tickets.
>
> **Marcus:** Good. Now connect it to today. Prompt eight, the automation candidate screener. What's its first step?
>
> **Jess:** The determinism check. Which parts can a rule, a script or a built-in system feature handle? Those never go to an LLM. Then check whether the existing tool already does it natively.
>
> **Marcus:** And notice the pattern ladder that follows: none, single prompt, prompt chain, routing, parallelization, orchestrator-workers, evaluator-optimizer, autonomous agent. Run the skate park diagnoser through that screener and what verdict do you get?
>
> **Jess:** Single prompt. Constrained output. Definitely not an autonomous agent.
>
> **Marcus:** The IT Director library and the skate park, teaching the same lesson from opposite ends. Also worth keeping: employee comments are data, not instructions, and prompts nine and ten use plan-then-solve, where the model shows you its plan and stops before writing the full document.
>
> **Jess:** One more from smolagents. The weather agent asks the model to "respond with JSON." That's a request, not a guarantee, right? You validate with something like Pydantic and retry.
>
> **Marcus:** Right. And its docstrings had no Args section, which smolagents uses to describe each argument. Which brings us to the blast from the past.
>
> **Jess:** Tool descriptions.
>
> **Marcus:** Tool descriptions. The model knows a tool only through its name, description and input schema. Tool descriptions are prompt engineering. Now replay the skate park with that lens. The inventory tool returned zero stock for an item the shop doesn't even carry. What principle did that break?
>
> **Jess:** Return high-signal results. "Out of stock" and "we don't sell that" look identical. It should return an explicit "not carried" result.
>
> **Marcus:** And the maintenance log got a reported by value of "customer," which the model invented.
>
> **Jess:** Everything required. If a field is required and the model doesn't know the value, it makes one up. Make it optional, or have the agent ask.
>
> **Marcus:** And the diagnoser that wouldn't stop? An error message or a tool result is the next prompt the model reads. A tool that says "Recorded, now call final answer" is just an instructive result. Three skate park bugs, all explained by a note from September.
>
> **Jess:** That's a satisfying callback. What about the ReAct samples?
>
> **Marcus:** They teach the THINK slash ACT format, one tool per step. The network and IT examples add guardrails: read-only rules, cite every observation, a step limit with an honest "inconclusive" exit, and a calculator tool. Compute, don't ask, again.
>
> **Jess:** Anything off in them?
>
> **Marcus:** One real inconsistency worth fixing. The prompts say every step must be a single THINK and ACT message. But in the config drift and vulnerability examples, the last few steps are ACT with no THINK at all. Few-shot examples are the strongest instruction in the prompt, so the model will learn to skip its reasoning exactly when it's wrapping up. Your tool descriptions note has a principle for that: keep examples consistent with the instructions. And a smaller one in the financial analyst sample: it passes the ticker as dollar sign M C. Whether that works depends on the tool, so it's ambiguous, but the model will copy the dollar sign every time. Document the expected format.
>
> **Jess:** And MCP, last one.
>
> **Marcus:** The core idea: the M times N integration problem becomes M plus N. Wrap a service once as an MCP server, and any MCP client can use it. Ten apps and fifty services goes from five hundred connectors to sixty. Servers expose tools, which the model controls, resources, which the application controls, and prompts, which the user controls. Your note is updated to the July twenty twenty-six spec, where requests are stateless. Any state that spans calls, like a shopping cart, travels as an explicit handle that one tool returns and later calls pass back.
>
> **Jess:** Which is the same idea as the skate park's business state living in Python objects while the agent's memory resets every request.
>
> **Marcus:** Exactly that. State that matters lives outside the model. And since every framework in your comparison speaks MCP, remember that it standardizes the plumbing, not the trust. Third-party tool descriptions go straight into your agent's context.
>
> **Jess:** Okay, wrap it up for me.
>
> **Marcus:** Three takeaways. One: don't put an agent loop where a single constrained call will do. A classification is one call with an enum, and every unnecessary step costs you quadratically in tokens and multiplicatively in reliability. Two: decide deliberately where control lives. Routing in a prompt is soft and lets every request reach every tool. Routing in code is deterministic and limits the blast radius, and frameworks differ mostly in which default they hand you. Three: frameworks package the loop, not your guarantees. Durable execution doesn't prevent lost updates, multiple sources don't guarantee correctness, and a run where every answer looks right can still be wasting most of its budget. Read the trajectory, not just the reply.
>
> **Jess:** And the think about it question?
>
> **Marcus:** Here it is. Suppose you rebuild the skate park system for production and move routing out of the orchestrator's prompt and into code, so each category reaches only its own small toolset. Which kinds of customer requests get worse, not better, under that design? And how would you give those requests a path, without going back to every request seeing all nine tools?
>
> **Jess:** Ooh. The helmet one is already nagging at me. I'll sit with it.
>
> **Marcus:** Sit with it. That's the show. Thanks for listening to MS AI Daily.
>
> **Jess:** See you tomorrow.
