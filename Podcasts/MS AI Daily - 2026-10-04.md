---
title: "MS AI Daily – 2026-10-04"
type: podcast
created: 2026-10-04
duration_min: 15.5
covers:
  - "[[Agent State Management]]"
  - "[[Implementing Agent State Management with Python]]"
  - "[[Runtime or Orchestration Layer]]"
  - "[[Agentic AI Skills Scorecard - Study Guide]]"
  - "[[Vector Databases]]"
  - "[[Marketing Director Prompt Library]]"
  - "[[COO Prompt Library]]"
  - "[[Large Language Models]]"
  - "[[Planning Agents]]"
  - "[[Prompt Injection]]"
tags:
  - podcast
  - review
---

# MS AI Daily – 2026-10-04

![[MS AI Daily - 2026-10-04.mp3]]

> [!abstract] In this episode
> Agent state: why a stateless model needs your code to carry query, messages and tool calls through a state-machine loop, and how the Python workflow engine's shallow-overwrite merge can silently erase history. Marcus flags that the implementation note describes an earlier version of the engine (`lib/state_machine_test1.py`). The current `lib/state_machine.py` has no `max_steps` loop guard, doesn't enforce declared transition targets, silently drops non-schema keys, and doesn't snapshot the termination step.

## Segments
- **Deep dive:** [[Agent State Management]], [[Implementing Agent State Management with Python]]. Covers statelessness, ephemeral working memory, the step contract and router, traceability vs determinism, quadratic token cost, merge semantics, the note-vs-code correction, and human approval forcing durable state.
- **Rapid review:** [[Runtime or Orchestration Layer]] (durable execution, budget-cap math), [[Agentic AI Skills Scorecard - Study Guide]] (CoT vs ReAct, reliability math), [[Vector Databases]] (hybrid search, tenant filters), [[Marketing Director Prompt Library]] and [[COO Prompt Library]] (compute-don't-ask, gates, correlation vs causation)
- **Blast from the past:** [[Large Language Models]] (statelessness, KV cache), [[Planning Agents]] (plan-execute-replan on a state machine), [[Prompt Injection]] (state as an injection channel, the lethal trifecta)

> [!warning] Note correction to review
> [[Implementing Agent State Management with Python]] describes `max_steps`, rejection of undeclared targets, one transition per source, and deep-copied input. Those match `lib/state_machine_test1.py`, not the current `lib/state_machine.py` (updated 2026-10-03 21:45). In the current file:
> - `run()` has no iteration cap.
> - A condition's return value isn't checked against the declared targets.
> - `connect` appends transitions, and more than one resolved next step raises `NotImplementedError`.
> - The merge keeps only schema fields.
> - `Termination` isn't snapshotted.

## Think about it
Your agent needs human approval before sending email, and approvals can take a day. Once you checkpoint state to survive that wait, where is the line between ephemeral working state and long-term memory? And what new risks appear (stale state, injected content) when a paused run resumes hours later in a world that has changed?

> [!quote]- Transcript
> **Marcus:** Here's a puzzle to start the day. You build an agent, it answers a weather question perfectly, and you're feeling great. Then you change one line, so the language model step returns only its newest message instead of the whole conversation. Nothing crashes. No error. But now the agent acts like it has amnesia every other turn. Where did the memory go?
>
> **Jess:** My gut says the model forgot something, but I have a feeling you're about to tell me the model never remembered anything in the first place.
>
> **Marcus:** That's exactly where we're headed. Welcome to MS AI Daily. It's Sunday, October fourth, twenty twenty-six. I'm Marcus.
>
> **Jess:** And I'm Jess. Today is all about agent state, what it is and how you actually implement it, plus a correction to one of the notes that I think is going to matter for the lab.
>
> **Marcus:** Right. The deep dive covers Agent State Management and the companion Python implementation. Then a rapid review of the orchestration layer, the course skills scorecard, vector databases, and the two executive prompt libraries. And in Blast from the Past we'll revisit large language models, planning agents, and prompt injection, because all three plug straight into today's topic.
>
> **Jess:** Okay, so let's start at the foundation. Why does an agent need state at all?
>
> **Marcus:** Because the model is stateless. Every call to a large language model is a blank slate. It knows only what's in the prompt you send right now. When a chat app seems to remember you, that's the application resending the entire history on every call. So statefulness is something your code builds around the model, not something the model has.
>
> **Jess:** So the state is basically the agent's working memory for one task.
>
> **Marcus:** Good, that's the lecture's framing. Agent state holds five things. The original user query, the system instructions, the message history, any tool calls the model has requested but that haven't run yet, and intermediate results. And it's ephemeral. When the run ends, it's gone unless you deliberately save it.
>
> **Jess:** Is ephemeral a weakness, though? It sounds like a limitation we're just accepting.
>
> **Marcus:** It's a design choice, and for short tasks it's a good default. It keeps the agent focused and avoids piling up stale or sensitive data. Long-term memory, things that survive across sessions, is a separate concern with separate risks, like stale or poisoned facts. Where ephemeral bites you is long-running work. We'll come back to that.
>
> **Jess:** Okay. And the lecture's big move is modeling the agent as a state machine.
>
> **Marcus:** Right. Every step follows one contract: it takes the current state and returns an updated state. Then a transition function looks at that new state and picks the next step. The lecture's loop is prepare the messages, call the model, check whether the model asked for tools. If yes, run the tools, append the results, and go back to the model. If no, produce the final answer and stop.
>
> **Jess:** That sounds a lot like the ReAct loop from earlier in the course. Thought, action, observation.
>
> **Marcus:** It's the same loop with the plumbing exposed. ReAct describes the reasoning pattern. The state machine describes how your code carries data between the turns. Let me ask you something. Who decides whether a tool runs?
>
> **Jess:** The model, right? It says "call get weather," so the weather tool runs.
>
> **Marcus:** Half right, and the missing half is the important part. The model decides whether tools are needed by writing tool calls into state. Code decides what happens next by reading that state. The router is a plain function: if tool calls is non-empty, go to the tool step, otherwise finish. That split is what keeps control flow inspectable even when the model is driving.
>
> **Jess:** The lecture called that router a lightweight form of self-awareness. I liked that phrase.
>
> **Marcus:** It's a memorable phrase, but don't take it literally. There's nothing self-aware happening. It's conditional branching on the model's output. The model's text steers the flow, and an if statement makes the call. If you describe it in an interview as self-awareness, someone will raise an eyebrow.
>
> **Jess:** Fair. What about the claim that this makes agents deterministic? Your notes push back on that too.
>
> **Marcus:** And they're right to. The control flow is deterministic given a state. But the model step is still stochastic. Run the same umbrella question twice and one run might call the weather tool once, the other might call it three times. What you gain is traceability. If you log the state after every step, you can reconstruct exactly why the agent answered the way it did. To actually reproduce a run, you have to record the model outputs, not just rerun the code.
>
> **Jess:** Okay, so the cost side. The note has a quadratic growth argument I want to make sure I understand.
>
> **Marcus:** Walk me through it. You've got the numbers from the self-test.
>
> **Jess:** Six model calls, the first prompt is a thousand tokens, and each loop adds five hundred. Call one sends a thousand, call two sends fifteen hundred, and so on. Total is six thousand plus five hundred times fifteen, so thirteen and a half thousand. Double it to twelve calls and it's forty-five thousand.
>
> **Marcus:** Exactly. More than three times the cost for twice the loop. Because you resend the growing history every time, total input tokens grow with the square of the loop length. So state design, what you keep, summarize, or drop, is a cost lever, not just a correctness one.
>
> **Jess:** Now I want to get to the implementation, because I think this is where the cold open comes from.
>
> **Marcus:** It is. The companion lesson builds a small workflow engine in Python with no AI inside at all. You register steps, connect them with fixed or conditional transitions, and run threads a shared typed dictionary from an entry point to a termination step, taking a snapshot after each step.
>
> **Jess:** Which honestly confused me at first. Why does an AI course teach an AI-free file?
>
> **Marcus:** Because the machine part should be independent of the model. You can test routing with plain functions before you spend a single token. Any step can call any model, tool, or human. And code, not the model, decides what runs next. The demo shows it with arithmetic. A linear chain that adds one and doubles, which is the prompt-chaining shape. And a counter that loops until it hits a max value, which is the agent-loop shape. Swap "count is less than max" for "the model requested tools" and you've got the agent.
>
> **Jess:** Okay, so back to the amnesia bug.
>
> **Marcus:** The merge is a shallow overwrite. When a step returns a key, it replaces the old value entirely. There's no append. So if your model step returns messages equal to a list with just the new reply, the whole history collapses to one message. You have to return the existing messages plus the new one.
>
> **Jess:** So if I implemented a tool step that returns only the tool results for messages, I'd wipe out the system prompt and the user's question.
>
> **Marcus:** You would, and the next model call would have no idea what it was doing. Same family of bug: if the tool step forgets to clear tool calls, the router sees them again and reruns the tools forever. Frameworks like LangGraph address the first one with reducers, where each field declares a merge rule, like "append to messages." This engine doesn't have reducers, so you do it by hand.
>
> **Jess:** Here's the part I flagged. Your note on the implementation describes a max steps guard, edges that reject undeclared targets, and so on. Is that accurate?
>
> **Marcus:** This is the correction for today, and it's a useful one. Your note matches an earlier version of the engine, the one that's now in the file named state machine test one. The current state machine file in the lib folder, which was updated later the same evening, behaves differently in a few ways that matter.
>
> **Jess:** Go ahead.
>
> **Marcus:** First, the current run method has no max steps parameter. There's no loop guard at all. A cycle that never terminates just keeps going. Second, the note says a condition can only return one of the declared targets, so a hallucinated step name gets rejected. In the current code, the condition's return value is used directly. It never gets checked against the declared targets. Third, connect now appends transitions to a list instead of replacing them, and if more than one next step comes back, it raises a not-implemented error for parallel execution. And fourth, the merge now quietly drops any key that isn't in the schema.
>
> **Jess:** Wow. So several of the safety properties I wrote down aren't true of the code I'll actually be running.
>
> **Marcus:** Correct. And the reason it matters: the no-loop-guard issue is the exact failure mode both your notes warn about. A model that keeps requesting tools will loop until you kill the process or your bill does. So in the lab, add your own iteration cap around the loop, and validate that the condition picks a step you actually connected. Also, the snapshot counts in the note's demo walkthrough assume termination gets snapshotted. In the current code, the loop breaks before running termination, so you'll see one fewer snapshot than the note predicts.
>
> **Jess:** And the dropped-keys thing. That sounds harmless, but I bet it isn't.
>
> **Marcus:** It's a silent failure. If your step writes a field you forgot to add to the schema, say approval status, it just vanishes. No error. Your router reads a missing field and routes somewhere you didn't expect. Silent misrouting is worse than a crash. To be clear, I'm not saying the newer code is wrong as a teaching engine. I'm saying update your note so you don't rely on guarantees that aren't there.
>
> **Jess:** Last piece. Both notes have the same design question: add a human approval step before any tool that sends email.
>
> **Marcus:** And the answer reveals the whole point. You add a branch after the model step: email tool calls go to an approval step, other tool calls go to tools, none goes to termination. But the human might answer tomorrow. This engine can't pause and resume. So human in the loop forces ephemeral state to become durable. You checkpoint the state and the current step, keyed by a run ID, and pick it back up when the approval arrives.
>
> **Jess:** Which is a perfect handoff to the rapid review, because that's the orchestration layer.
>
> **Marcus:** It is. Quick check. What does the orchestration layer control that prompts don't?
>
> **Jess:** Step order and branching, the state passed between steps, running the gates, retries, budgets, logging, and permissions. Prompts say what a step produces. The orchestrator decides when, with what data, and under what limits.
>
> **Marcus:** Perfect. And the gotcha is durable execution. Persist state after every step, so a crash at step five doesn't rerun steps one through four and repeat their side effects. The minimal runtime in your note checks the budget before each step, not after, and sends every failure to a real destination, a queue or an alert, never a silent none. And there's a nice bit of math there. If an agent finishes on any given turn with probability point two, then with a ten-turn cap about eleven percent of runs hit the cap. You'd need about twenty-one turns to get under one percent.
>
> **Jess:** Which is another argument for adding that loop guard to the state machine.
>
> **Marcus:** Exactly. Next, the skills scorecard. Give me the one-sentence distinction between Chain-of-Thought and ReAct.
>
> **Jess:** Chain-of-Thought makes the model think more. ReAct lets it know more, by acting and observing. Chain-of-Thought can't fix missing information, and ReAct can't fix bad reasoning.
>
> **Marcus:** That's the line. The gotcha there is reliability math. Chain eight steps at ninety-five percent each and end-to-end success is only about sixty-six percent. Gates and feedback loops exist to raise each step's success rate. And personas change tone and format reliably, but don't count on "you are an expert" to make the answers more accurate.
>
> **Jess:** Vector databases. Embeddings map meaning to geometry, and the database finds the nearest vectors using approximate search like HNSW, trading a little recall for a lot of speed.
>
> **Marcus:** Good. The gotcha is that semantic search blurs exact tokens. Search for a specific error code and dense retrieval may miss it entirely. That's why you add hybrid lexical search, B M twenty-five, and a reranker on top. And for multi-tenant systems, metadata and permission filters aren't optional. Without them, one customer's documents leak into another's answers.
>
> **Jess:** And the two prompt libraries, the Marketing Director and the COO ones for Wi-Fiber.
>
> **Marcus:** Those are applied work, so I'll pull out the transferable lesson. Both lean on a rule your notes call compute, don't ask. The model designs the analysis, the churn score, the uptime metric, and code computes the numbers. That's the same principle as today's deep dive. The model proposes, code decides and computes. The marketing library's capacity-aware targeting prompt is literally a gate check. Only sell into tower sectors that can actually serve the customer.
>
> **Jess:** And the COO library flags correlation versus causation for the uptime-to-churn analysis.
>
> **Marcus:** Right. That's the gotcha. An outage followed by a cancellation is a correlation until you control for things like market, tenure, and competitor entry.
>
> **Jess:** Time for Blast from the Past. Large language models.
>
> **Marcus:** Here's the connection. Your LLM note says the model is stateless, bounded by its context window, and every answer is a sample. Today's state machine is the scaffolding for the first property. And the quadratic token cost we talked about lands in the context window and the KV cache, the stored attention keys and values, which grows with every token of history you carry.
>
> **Jess:** Planning agents.
>
> **Marcus:** Plan-and-execute writes the plan up front, then runs it, and re-plans when an observation doesn't match expectations. It's receding-horizon control, like model predictive control. On a state machine, a planner step writes the plan into state, an executor step works through it, and a conditional edge routes back to the planner on a mismatch. Same engine, different graph. Remember to verify the plan, since language models produce plenty of invalid ones.
>
> **Jess:** And prompt injection.
>
> **Marcus:** Everything in state ends up in a prompt. A tool result written into messages flows straight into the next model call. So a web page your tool fetched can carry instructions. The deterministic defense lives in code: the router, the tool allow-list, and approval for irreversible actions. Check every design against the lethal trifecta: private data, untrusted content, and a way to send data out. Remove one leg.
>
> **Jess:** Let's wrap it up. Three takeaways?
>
> **Marcus:** One. The model doesn't remember anything. State is your code's job, and with a shallow-overwrite merge, a step that returns only the new message silently erases the history. Two. In the state machine, the model decides whether tools are needed, but code decides what runs next. That split gives you traceability, not determinism. Three. Check your safety guarantees against the code you're actually running. Today's engine has no loop guard and no target enforcement, so you add the iteration cap and route validation yourself.
>
> **Jess:** And the think-about-it question?
>
> **Marcus:** Your agent needs human approval before sending email, and approvals can take a day. Once you checkpoint state to survive that wait, where exactly is the line between ephemeral working state and long-term memory, and what new risks show up, from stale state to injected content, when a paused run resumes hours later in a world that has changed?
>
> **Jess:** That's a good one to sit with before the next lab. Thanks, Marcus.
>
> **Marcus:** Thanks, Jess. That's MS AI Daily. Go add a loop guard, and we'll see you tomorrow.
