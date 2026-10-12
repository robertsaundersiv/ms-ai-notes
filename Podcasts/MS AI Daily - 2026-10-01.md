---
title: "MS AI Daily – 2026-10-01"
type: podcast
created: 2026-10-01
duration_min: 27
covers:
  - "[[Building Agents with Tools in Python]]"
  - "[[Building an AI Agent with Tools - Exercise]]"
  - "[[Structured Outputs]]"
  - "[[Agent Components and Agent Types]]"
  - "[[Gate Checks]]"
  - "[[Implementing Gate Checks]]"
  - "[[LLM Feedback Loops]]"
  - "[[Sonar Ticket and Outage Classification - How-To]]"
  - "[[Retrieval-Augmented Generation]]"
  - "[[Artificial Intelligence]]"
  - "[[Implementing Parallelization Workflow]]"
tags:
  - podcast
  - review
---

# MS AI Daily – 2026-10-01

![[MS AI Daily - 2026-10-01.mp3]]

> [!abstract] In this episode
> Marcus and Jess take apart the tool-calling loop: the model only requests calls, your code runs them, and every tool call ID gets exactly one tool message. They use the game-stats exercise to show that an agent can reason only about what crosses its observation boundary. Then they link tool arguments to structured outputs: strict mode guarantees an answer's shape, never its truth, and schema design decides whether an honest answer is even possible.

## Segments
- **Cold open:** the game-stats agent that averages one game when asked about "all games". [[Building an AI Agent with Tools - Exercise]]
- **Deep dive:**
  - The tool-call loop and invariant, the course snippets' missing appends, and JSON-string arguments. [[Building Agents with Tools in Python]]
  - The `Agent` class, what "parallel" tool calls really mean (emitted together, not necessarily run concurrently), the observation boundary, the hidden dataset size, counting in the model's head (0.99^100 ≈ 0.37), replacing `eval` with an AST allow-list, and answering every ID. [[Building an AI Agent with Tools - Exercise]]
  - A tool's argument object is itself a structured output, plus the reliability ladder, the reading's "guarantees" claim (true only in strict mode), the course `lib` sitting on rung 3, optional fields becoming required-but-nullable, and the schema acting as a prompt. [[Structured Outputs]]
- **Rapid review:**
  - The five components, the four agent types, and the two hidden axes of the type spectrum. [[Agent Components and Agent Types]]
  - Gate verdicts, cheapest-first ordering, and E[calls] = 1.24. Design tension: short-circuiting on the first failure vs. returning every error in one retry. [[Gate Checks]] · [[Implementing Gate Checks]]
  - Tool errors as external feedback, the ranking of feedback sources, returning the best iteration, and evaluator gaming. [[LLM Feedback Loops]]
  - Ticket 1006 and compute-don't-ask. JSON mode vs. strict mode. Self-reported confidence isn't calibrated. [[Sonar Ticket and Outage Classification - How-To]]
  - Retrieval as a tool and the observation boundary. ACLs belong at retrieval time. [[Retrieval-Augmented Generation]]
  - The rational-agent view, plus two corrections (see below). [[Artificial Intelligence]]
- **Blast from the past:** silent thread failures and the stale global dict, and what you inherit if you run parallel tool calls concurrently. Nuance: leaving the `with ThreadPoolExecutor` block waits for hung workers, so only a client-side timeout sets a real deadline. [[Implementing Parallelization Workflow]]

> [!warning] Corrections raised in the episode
> - [[Artificial Intelligence]] says LLMs are "Transformers with RL-based fine-tuning". That's too broad. LLMs come from self-supervised next-token pretraining. RLHF is a common fine-tuning step for chat models, but it isn't part of what makes something an LLM.
> - [[Artificial Intelligence]] §5 says the LLM + rules approach "needs no labels". It needs no *training* labels, but it still needs labelled data for *evaluation* (compare the 500-ticket plan in [[Sonar Ticket and Outage Classification - How-To]]).
> - [[Implementing Parallelization Workflow]] §6 (an extension, not an error): `future.result(timeout=...)` records the failure, but leaving the `with` block calls `shutdown(wait=True)`. A hung call still blocks `analyze_contract`, so put the deadline on the API client.

## Think about it
Picture turning the Sonar ticket classifier into a tool-using agent. In **Design A**, the model gets tools to look up the account, list open outages and set the ticket group, and it runs in a loop deciding what to call. In **Design B**, code fetches the account and outage data, the model returns a strict structured decision, and code validates it and writes the ticket group. Which design keeps ticket 1006 (a delinquent account) from being sent to tier 1? Where does each design's observation boundary sit, and where do the gates have to live? And if the model in Design A issues the lookup and the write as parallel tool calls in the same turn, what could go wrong?

> [!quote]- Transcript
> **Marcus:** Jess, here's a puzzle. You build a little data-analyst agent over a video game dataset. You ask it, what's the average score of the top ten games, and it nails it. Ninety-one point five, checked by hand. Every test passes. Then a colleague asks, what's the average score of all the games, and the agent quietly averages exactly one game. Same model, same code. What broke?
>
> **Jess:** My first instinct is the model. Maybe it misread "all" as "the best one"?
>
> **Marcus:** That's the instinct almost everyone has, and it's the wrong place to look. The model did something perfectly reasonable with what it could see. The bug lives in what it could see. And that idea, that an agent can only reason about what its tools and schemas tell it, is the thread running through today's whole episode.
>
> **Jess:** Okay, I'm hooked. Welcome to MS AI Daily, it's Thursday, October first, twenty twenty-six. I'm Jess.
>
> **Marcus:** And I'm Marcus. Let's get into it.
>
> **Jess:** So, the plan. We're doing the brand-new material first: building tool-using agents in Python, the agent-with-tools exercise where that game dataset comes from, and structured outputs. Then a rapid review of gate checks, feedback loops, agent types, the Sonar ticket how-to, retrieval-augmented generation, and the big-picture A I note. And we'll close with the parallelization exercise as our blast from the past.
>
> **Marcus:** And I promise those connect. By the end you'll see that a tool call, a structured output, and a gate check are really three views of the same contract.
>
> **Jess:** Let's start at the bottom, then. What actually is a tool-using agent in Python, mechanically?
>
> **Marcus:** Strip away the frameworks and it's two things: a list of messages and a loop. You define a normal Python function, say get weather, with type hints and a docstring. A decorator turns that into a schema: a name, a description pulled from the docstring, and parameter types pulled from the hints. You send that schema along with your messages. And if the model decides it needs the tool, it doesn't answer in text. It answers with a tool call.
>
> **Jess:** And this is the part people get wrong in casual conversation. The model doesn't run get weather.
>
> **Marcus:** Never. The model writes a structured request: here's an I D, here's the function name, here are the arguments. Your code runs the function. Your code wraps the result in a tool message. Your code calls the model again. The model is the world's most articulate intern who can fill out a request form but isn't allowed near the server room.
>
> **Jess:** So it's the act and observe half of ReAct, just written out by hand.
>
> **Marcus:** Exactly that. Now let me test you on the rule that holds the whole thing together. In your notes it's called the tool-call invariant. What links the tool message back to the request?
>
> **Jess:** The tool call I D. Every I D in the assistant's message needs exactly one tool message with that same I D, placed after the assistant message, before the next model call.
>
> **Marcus:** Perfect. So, what happens if you forget to append that tool message and just call the model again?
>
> **Jess:** I'd guess the model hallucinates the temperature, since it never got a result?
>
> **Marcus:** That's possible in some setups, but the more common outcomes are blunter. If the assistant message with the tool call is in the history but no answer follows it, most provider A P Is just reject the request outright. And if you forgot to append both, the model sees the exact same conversation as before and asks for the tool again. Your notes caught that the course snippets skip both appends. The code reads messages minus one dot tool calls, but messages minus one is still the user message, because the A I message was never added.
>
> **Jess:** Which is a very sneaky bug, because each line looks right on its own.
>
> **Marcus:** Right. One more mechanical trap: the arguments arrive as a JSON string, not a dictionary. You have to parse them before you unpack them into the function. And that parse can fail, because the model wrote the JSON, so it belongs inside a try block.
>
> **Jess:** Okay, so the course did one round trip. The exercise generalizes that into an Agent class.
>
> **Marcus:** Yes. The Agent class bundles configuration, meaning role, instructions, model, temperature, and tools, with an invoke method. Invoke builds the system and user messages, calls the model, and then loops: while the latest A I message has tool calls, run each one, append a tool message per call, call the model again. When the model finally answers in plain text, return it.
>
> **Jess:** And one of the test runs surprised me. The math assistant got "multiply three by five, then later add seven," and it sent two tool calls in a single turn: "three times five" and "open paren three times five close paren plus seven." So, parallel tool calls. I'm assuming that means the two calculations ran concurrently, like on separate threads?
>
> **Marcus:** That's a really natural reading of the word "parallel," and it's not what it means. Parallel tool calls means the model emitted several requests in one assistant turn, before seeing any results. Whether your code executes them concurrently is entirely your decision. In the exercise, they ran one after another in a plain for loop.
>
> **Jess:** Oh. So "parallel" describes the model's request, not the execution.
>
> **Marcus:** Right. And that explains the odd second expression. The model didn't have fifteen yet when it wrote the second call. So it folded the dependency into the expression itself. Which is clever, but it also tells you something: requests issued together have to be independent. If the second one truly needed the first one's result, the model would have to wait for the next loop iteration. Your notes call that chained calls, across iterations, versus parallel calls, within one turn.
>
> **Jess:** Okay, now the cold open. The game stats agent.
>
> **Marcus:** Here's the tool. Get games takes num games, which defaults to one, and a boolean called top. It returns the top or bottom N games by score. Before I explain the failure, what do you think the model can see about how big the dataset is?
>
> **Jess:** Hmm. It sees the description, the parameter schema, and whatever comes back. The description says "top or bottom N games." The schema says num games is an integer. And the result is just a list.
>
> **Marcus:** So does any of that say there are ten games?
>
> **Jess:** No. Nothing does. The list lives inside the Python function and its length never crosses the boundary.
>
> **Marcus:** That's what your notes call the observation boundary. Everything the model knows about the environment comes from the messages, the tool schemas, and the tool results. Facts outside that boundary don't exist for the model. So when you ask about all games, it has four bad options. Guess an N. Take the default of one and confidently average a single game. Ask the user, which is honest but the prompt never encouraged it. Or skip the tool and make something up.
>
> **Jess:** And even when it guesses right, it can't tell. Ten results look the same whether the dataset has ten games or ten thousand.
>
> **Marcus:** That's the deeper point. It can't verify completeness. So here's the principle worth tattooing somewhere tasteful: a tool that returns a slice must also report the size of the whole. That's why every decent paginated A P I returns a total count or a has-more flag.
>
> **Jess:** And the fix the notes rank first is returning metadata with every result. Total games, how many were returned, then the games themselves.
>
> **Marcus:** And making num games optional, where leaving it out means "everything," and saying so in the docstring. Second best is a dataset-info discovery tool, the same move a S Q L agent makes when it counts rows before querying. Third, do the aggregation in a tool, an average-score function, so the code computes and the model only explains. The weakest fix is writing "the dataset has ten games" in the prompt.
>
> **Jess:** Because that's a hard-coded fact that drifts the moment the data changes.
>
> **Marcus:** Exactly. Now, notice the other quiet problem in that exercise. When asked about the distribution of platforms, the model got the right answer, but it did the counting in its head. No tool backed it.
>
> **Jess:** It was right, though. Four Switch, two Wii, two 3 D S, and so on. Is that really a problem if it's correct?
>
> **Marcus:** Correct on ten items. Think about it as a reliability product. If the model counts each item correctly ninety-nine percent of the time, getting a hundred items all right is point nine nine to the hundredth, which is about thirty-seven percent. Move the counting into code and it becomes deterministic. Language models are fluent, not arithmetic. They're the coworker who sounds most confident in the budget meeting.
>
> **Jess:** And there's an evaluation lesson in here too. The tests passed because the question leaked the answer. "Top ten" handed the agent the one fact it couldn't discover.
>
> **Marcus:** That's the line I'd want you to remember for project work: test what the agent must discover, not what you tell it. If your eval questions contain the scope, your eval can't see the gap.
>
> **Jess:** Your notes also did a code review on the exercise. The scary one was the calculator.
>
> **Marcus:** The calculator used Python's eval on the expression. That's arbitrary code execution, and the arguments come from the model, which can be steered by any injected text it read. The fix is parsing the expression into a syntax tree and allowing only number literals and basic arithmetic operators. Your notes even left out exponentiation on purpose, because nine to the nine to the nine will happily eat your server for the afternoon.
>
> **Jess:** And the subtle one: if the model calls a tool name that isn't registered, the loop just skips it.
>
> **Marcus:** Which means that tool call I D never gets an answer, which breaks the invariant, which gets the next request rejected. The fix is to always answer every I D, even if the answer is an error object. Errors become observations. The model reads "unknown tool" or "invalid argument" and can try again. Add a step budget so it can't loop forever, and that's a respectable agent loop.
>
> **Jess:** Okay, that brings us to the third new note, structured outputs. And you said they connect.
>
> **Marcus:** Here's the bridge. What is a tool call's argument object, really?
>
> **Jess:** It's... JSON that matches the tool's schema. Oh. It's a structured output.
>
> **Marcus:** Exactly. Function calling and structured output are the same machinery. You can even define a "record ticket" function you never execute, force the model to call it, and use the arguments purely as an extraction result.
>
> **Jess:** So why does structured output matter on its own?
>
> **Marcus:** Because it's what lets an agent act on software instead of just talking to people. The reading's example: instead of summarizing a support call in prose, extract issue type, urgency, and customer email. That record can open a ticket, set priority, and notify the customer with nobody retyping anything.
>
> **Jess:** And just asking for JSON in the prompt isn't enough.
>
> **Marcus:** It works most of the time, and fails in ways that break code. Urgency comes back as "very." The email field says "none found." The JSON gets wrapped in markdown fences or a cheerful "Sure! Here's your JSON." Or the output gets cut off at the token limit. A prompt is a request, not an enforcement mechanism.
>
> **Jess:** Which is why your notes describe a reliability ladder. Rung one, prompt for JSON. Rung two, a parser plus schema validation. Rung three, function calling. Rung four, strict mode, which is constrained decoding. Rung five, semantic validators with retries.
>
> **Marcus:** Good. And there's a correction in your notes I want to reinforce, because it's the kind of thing that gets repeated in vendor blog posts. The course reading says function calling "guarantees correct format and types." That's only true at rung four, with strict mode. Plain function calling gives the model the schema as a strong hint. It usually complies, but it can still emit an invalid enum value or leave out a field.
>
> **Jess:** And the course's own helper library sits on which rung?
>
> **Marcus:** Your notes checked that. It sets additional properties to false but doesn't set strict to true. So it's rung three, not rung four. Good catch, honestly.
>
> **Jess:** Okay, here's where I want to push. If I turn on strict mode, the output is guaranteed to match my schema. So can't I drop the Pydantic validation step and save myself the code?
>
> **Marcus:** That's the most tempting shortcut in this whole topic. And no. Strict mode guarantees shape. It doesn't guarantee truth. A hallucinated email address is a perfectly valid string. Urgency "high" is a valid enum value even when the customer said "whenever you get a chance." Strict mode also can't stop a refusal, or truncation, and providers only support a subset of JSON Schema features.
>
> **Jess:** So strict mode shrinks the format gate's job, but the content and logic gates still have to run.
>
> **Marcus:** That's precisely the right way to say it. And there's a portability argument too. Strict decoding is provider-specific, with different supported subsets. If Pydantic is your single source of truth and you validate locally, you can switch providers without trusting anyone's guarantee.
>
> **Jess:** One detail surprised me. When you make a field optional in Pydantic and send it through strict mode, it shows up as required.
>
> **Marcus:** Right. In strict mode every key must be present, so "optional" becomes "required but nullable." The model must always write the customer email key, and its only escape is null. Which leads to the part of this note I think is most underrated: the schema is also a prompt.
>
> **Jess:** Meaning the shape steers what the model writes.
>
> **Marcus:** Yes. If customer email is a plain required string, and the caller never gave an email, the model must invent something. So make "not found" representable. Close your vocabularies with literal types. Include an escape value like "other" so it doesn't jam an odd case into the wrong bucket. Put a reasoning or evidence field before the answer field, because generation follows key order.
>
> **Jess:** Wait, that's the same lesson as the game tool. The default of num games equals one quietly steered the model toward averaging one game.
>
> **Marcus:** That's the connection I was hoping you'd make. On the input side and the output side of a tool, the schema decides what honest behavior is even possible. Your notes have a line I love: the schema design, not the model, decided whether the system behaved honestly.
>
> **Jess:** One thing I wondered. If you force the answer into a strict schema, does the model reason worse?
>
> **Marcus:** Fair question, and the honest answer is: the evidence is mixed. Some studies found format restrictions hurt reasoning tasks, others found little effect. It depends on the task. The common hedge is to let the model reason first, either in an early free-text field or a separate unconstrained step, then constrain only the final fields.
>
> **Jess:** And how would you evaluate an extraction system like this?
>
> **Marcus:** Not by percent valid JSON. That's the easy part to measure, which is exactly why vendors like it. Measure field-level accuracy against labeled examples: exact match on the enums, precision and recall per field. That's where the expensive errors live.
>
> **Jess:** Okay, rapid review time. Let me start with one you'll quiz me on anyway. Agent components and agent types.
>
> **Marcus:** Go for it. Five components?
>
> **Jess:** Persona, Knowledge, Prompting Strategy, Execution and Tools, and Interaction. And four types on a spectrum: Direct Prompting, Prompt Augmentation, Dynamic Context Augmentation, and Autonomous.
>
> **Marcus:** So where does today's Agent class sit?
>
> **Jess:** Dynamic Context Augmentation. Tool results update the context during the task. It's not autonomous because it doesn't plan sub-tasks or self-correct beyond the tool loop.
>
> **Marcus:** Good. And here's the gotcha from your notes' critique: that spectrum quietly mixes two axes. How dynamic the context is, and who controls the flow, code or the model. A fixed chain where step two always calls an A P I has dynamic context but code-controlled flow. Keep those axes separate in your head and a lot of design conversations get easier.
>
> **Jess:** Next, gate checks, the lecture note and the implementation note together. A gate sits between steps and decides pass, retry with feedback, reroute, or stop. Three core types from the lecture: format, content, logic.
>
> **Marcus:** And the ordering rule?
>
> **Jess:** Cheapest and deterministic first. Schema, then rules, then grounding, then anything expensive like an L L M judge, then safety and action gates. And every failure needs a destination. Never return None and carry on.
>
> **Marcus:** Now a quick number. First-attempt pass rate of point eight, three attempts max, independent retries. Expected calls per step?
>
> **Jess:** One, plus point two, plus point zero four. So one point two four calls. Escalation probability is point two cubed, which is point zero zero eight.
>
> **Marcus:** Exactly right. And the gotcha: real retries aren't independent. The same confusing input fails the same way. Rerouting to a different prompt or model breaks that correlation. Here's one design tension I'll flag between your two notes, not as an error, just something to decide deliberately. The implementation note's run-gates function short-circuits, returning only the first failing gate's feedback. But the Sonar how-to points out that sending the model all three errors at once usually lets it fix everything in one pass. Short-circuiting saves compute on expensive gates, but for cheap deterministic checks, collecting all the errors is often the better retry prompt.
>
> **Jess:** That's a good one. Okay, feedback loops. Generate, evaluate, feed back, revise, stop. Five parts: generator, evaluator, feedback formatter, stop condition, and memory.
>
> **Marcus:** And how does today's material connect?
>
> **Jess:** Oh, the agent loop is a feedback loop. When a tool returns an error object, that's external feedback, and the model revises its call.
>
> **Marcus:** Right, and external feedback is the strong kind. Your notes rank it: external tools and validation checks first, user input strong on intent but slow, and intrinsic self-correction weakest, because the critic shares the generator's blind spots. The gotchas: always have at least two stop conditions, success and a hard cap. And return the best iteration, not the last, because loops regress.
>
> **Jess:** And watch for evaluator gaming. A loop optimizes whatever the evaluator measures, which is how you get code that special-cases the test inputs.
>
> **Marcus:** Goodhart's law with a pytest badge. Next.
>
> **Jess:** The Sonar ticket and outage how-to. Two chains for an internet provider. One classifies support tickets into ticket groups, the other classifies network outages from monitoring alerts. And the design rule is compute, don't ask. If code can determine a field from data you already have, don't make the L L M guess it.
>
> **Marcus:** Give me the key case.
>
> **Jess:** Ticket ten-oh-six. "My service stopped working this morning." The text alone points to tier one support. But the account is delinquent in Sonar, so it's probably a non-payment suspension. A code rule routes it to collections before the L L M is even called, because the deciding fact isn't in the text.
>
> **Marcus:** Perfect. And here's the connection to today. That note's gated call uses JSON mode. Where's that on the ladder?
>
> **Jess:** JSON mode guarantees valid JSON but not the schema. So it's below strict mode. They rely on Pydantic to catch schema problems.
>
> **Marcus:** Right. They could move up to strict mode and cut format retries. But notice that their most valuable gates, the ones checking that quotes actually appear in the ticket, or that the root device matches topology, would still be needed. Those are truth checks, not shape checks. One more gotcha: in the triage math, low self-reported confidence, not gate failures, drives most of the triage volume. And that confidence number is not a calibrated probability. Treat it as a soft threshold you calibrate against labeled data.
>
> **Jess:** Retrieval-augmented generation. Retrieve relevant chunks at query time, put them in the prompt, answer from evidence. Use RAG for knowledge, fine-tuning for behavior.
>
> **Marcus:** Gotcha?
>
> **Jess:** Most RAG failures are retrieval failures. If the right chunk isn't in the context, no prompt saves you. So measure recall at k separately from faithfulness.
>
> **Marcus:** And today's tie-in: in agentic RAG, retrieval is just another tool. So the observation boundary applies. If your search tool returns five chunks and doesn't say whether there were five relevant documents or five hundred, the agent can't judge whether it has the full picture. Same lesson as the games. And enforce access control in the retrieval filter, not in a prompt instruction.
>
> **Jess:** Last one in rapid review, the foundational A I note. The rational agent view: choose actions expected to maximize a performance measure given percepts and knowledge. And agentic A I is the classic agent loop with an L L M as the decision policy.
>
> **Marcus:** Good. I want to tighten two lines in that note. First, it says L L Ms are deep learning transformers with R L based fine-tuning. That's a little too broad. The core of an L L M is self-supervised pretraining on next-token prediction. Reinforcement learning from human feedback is a very common fine-tuning step for chat models, but it's not part of what makes something an L L M. A base model with no R L at all is still an L L M.
>
> **Jess:** Fair. And the second?
>
> **Marcus:** The worked example says the L L M plus rules approach "needs no labels." It needs no training labels, true. But it absolutely needs labeled data for evaluation. Your own Sonar note says to export about five hundred historical tickets with the human-assigned group. Without labels you can't tell if the L L M is earning its keep over a rules-only baseline.
>
> **Jess:** That's a good correction. "No labels" sounds like "no evaluation," and that's the opposite of the lesson.
>
> **Marcus:** Exactly. Okay, blast from the past.
>
> **Jess:** Implementing the parallelization workflow. The contract review exercise. Three specialist agents, legal, compliance, and financial, analyze the same contract at the same time on Python threads, write results into a shared dictionary, and a summary agent synthesizes a report.
>
> **Marcus:** And why do threads help here, despite Python's global interpreter lock?
>
> **Jess:** Because the lock is released while a thread waits on network I O. The agents spend almost all their time waiting on the A P I, so the calls really overlap.
>
> **Marcus:** Right. Now the part your notes tested, which is the real lesson. What happens when the compliance agent's A P I call fails?
>
> **Jess:** On the first run, the thread dies, join returns normally because thread exceptions don't propagate, and the summary crashes with a key error. But on a later run, with a different contract, the global dictionary still holds the old compliance result. So the report on contract B silently includes compliance findings from contract A.
>
> **Marcus:** No error, no warning, and a fluent report. That's the worst kind of failure, because the L L M will write beautifully about whatever data you hand it. Now here's why I picked this note for today. Suppose you take today's agent loop and decide to execute parallel tool calls concurrently, to save latency. What do you inherit?
>
> **Jess:** All of this. A worker that fails silently would leave a tool call I D unanswered, so the invariant breaks. Or worse, if results go through some shared state, I could attach a stale result to the wrong I D.
>
> **Marcus:** Exactly. The fix in your notes carries over directly. Use a thread pool executor, because future dot result either returns the value or re-raises the worker's exception in the main thread. Keep results local to each run. Catch failures per worker. And in the agent version, turn each failure into an error-valued tool message, so every I D still gets answered.
>
> **Jess:** The notes also tell the synthesizer which analyses are missing, so it writes "not assessed" instead of making up a compliance section.
>
> **Marcus:** Which is the observation boundary again. If the synthesizer isn't told what's missing, it can't know. Let me add one nuance your notes only half cover. They correctly say a timeout on future dot result stops waiting but doesn't kill the thread. But notice the improved code gathers results inside a "with" block on the executor. When that block exits, it waits for every worker thread to finish. So a truly hung A P I call still blocks the whole function, timeout or not. The timeout records the failure, but it doesn't actually bound your wall-clock time.
>
> **Jess:** So the real deadline has to live on the H T T P client itself.
>
> **Marcus:** Right, which is what the note's caveat recommends. Set the timeout on the A P I client, and treat the future timeout as bookkeeping. Classic distributed-systems hygiene, wearing an A I costume.
>
> **Jess:** Okay, let's wrap it up. Three takeaways.
>
> **Marcus:** First. The model never executes anything. A tool-using agent is a message list and a bounded loop, and the one rule is that every tool call I D gets exactly one tool message, even when the answer is an error. Errors as observations are what turn a brittle script into a self-correcting loop.
>
> **Jess:** Second. The agent can only reason about what crosses the observation boundary. If a tool returns a slice, it must also return the size of the whole. Push counting and aggregation into code. And write evaluations that make the agent discover scope instead of handing it over in the question.
>
> **Marcus:** Third. Schemas guarantee shape, never truth. Strict mode removes format failures, but grounding and logic checks still have to run in your code. And design your schemas, inputs and outputs alike, so that "unknown," "none," and "other" are representable, because the schema decides whether honesty is even an option.
>
> **Jess:** And the think-about-it question.
>
> **Marcus:** Picture turning the Sonar ticket classifier into a tool-using agent. In design A, the model gets tools to look up the account, list open outages, and set the ticket group, and it runs in a loop deciding what to call. In design B, code fetches the account and outage data, the model returns a strict structured decision, and code validates it and writes the ticket group. Which design keeps ticket ten-oh-six safe from a delinquent account being sent to tier one? Where does each design's observation boundary sit, and where do the gates have to live? And if the model in design A issues the lookup and the write as parallel tool calls in the same turn, what could go wrong?
>
> **Jess:** Ooh, that last part is nasty. I'm going to sit with that one.
>
> **Marcus:** Good. Don't answer it in the car. That's it for today's MS AI Daily. I'm Marcus.
>
> **Jess:** And I'm Jess. See you tomorrow.

