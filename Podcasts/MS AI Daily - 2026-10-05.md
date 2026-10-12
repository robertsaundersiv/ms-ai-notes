---
title: "MS AI Daily – 2026-10-05"
type: podcast
created: 2026-10-05
duration_min: 18
covers:
  - "[[Agent State Management]]"
  - "[[Implementing Agent State Management with Python]]"
  - "[[Implementing Prompt Chaining Workflow]]"
  - "[[Task Decomposition]]"
  - "[[Model Evaluation]]"
  - "[[Knowledge Graphs]]"
  - "[[Network Operations Engineering Manager Prompt Library]]"
  - "[[AI Memory]]"
  - "[[ReAct prompt Samples]]"
  - "[[Agentic AI]]"
tags:
  - podcast
  - review
---

# MS AI Daily – 2026-10-05

![[MS AI Daily - 2026-10-05.mp3]]

> [!abstract] In this episode
> Marcus and Jess go deep on agent state: why LLMs are stateless, how the state machine pattern (S to S prime, conditional routing) structures the agent loop, and why the history in state makes cost grow quadratically. They walk through the AI-free workflow engine and its shallow-overwrite merge trap. Marcus flags that `state_machine.py` was changed after the implementation note was written: the `max_steps` loop guard and the declared-target check that the note describes are no longer in the code.

## Segments
- **Cold open and deep dive:** [[Agent State Management]], [[Implementing Agent State Management with Python]]
- **Rapid review:** [[Implementing Prompt Chaining Workflow]], [[Task Decomposition]], [[Model Evaluation]], [[Knowledge Graphs]], [[Network Operations Engineering Manager Prompt Library]]
- **Blast from the past:** [[AI Memory]], [[ReAct prompt Samples]], [[Agentic AI]]

> [!warning] Corrections raised in this episode
> - [[Implementing Agent State Management with Python]] describes an earlier version of `lib/state_machine.py`. The current file (saved about two hours after the note) differs in these ways:
>   - It has no `max_steps` loop guard.
>   - It doesn't check a condition's return value against the declared targets.
>   - It appends multiple `connect` calls per source; if they produce more than one next step, it raises `NotImplementedError`.
>   - It doesn't snapshot `Termination`, so the counter demo produces 11 snapshots, not 12.
>   - It silently drops returned keys that aren't in the schema.
>   - Self-test Q4 (the answer of 98) no longer applies.
> - [[Agent State Management]]: the "deterministic" claim really means deterministic control flow given the state. The lecture's "self-awareness" wording is overstated.
> - [[Knowledge Graphs]]: "GraphRAG" covers several approaches: hybrid vector-entry-plus-traversal, and Microsoft's community summaries. Say which one you mean.

## Think about it
Suppose you build the NOC triage agent from [[ReAct prompt Samples]] on the current state machine, which has no step budget and doesn't check routes against declared edges, and you add an approval step for write actions. What kind of budget do you add: steps, tokens, or wall-clock time? And what exactly must you checkpoint so an approval that arrives at 7 a.m. can resume the run without replaying, and paying for, the LLM calls from 2 a.m.?

> [!quote]- Transcript
> **Marcus:** Here's a scenario. You build an agent on a little state machine engine. Your notes say the engine has a loop guard: if the agent runs past a hundred steps, it raises an error and stops. So you go to bed. Overnight, the model keeps asking for the same tool, again and again. What does your bill look like in the morning?
>
> **Jess:** If the guard works, it's capped at a hundred steps and I sleep fine. I'm guessing you're about to tell me the guard doesn't work.
>
> **Marcus:** I'm about to tell you the guard isn't in the code anymore. We'll get to that. Welcome to MS AI Daily. It's Monday, October fifth, twenty twenty-six. I'm Marcus.
>
> **Jess:** And I'm Jess. Today is all about agent state, which sounds dull until you realize it's where most agent bugs actually live.
>
> **Marcus:** Here's the plan. The deep dive covers your two newest notes: the agent state management lecture, and the Python state machine that implements it. Then a rapid review of prompt chaining, task decomposition, model evaluation, knowledge graphs, and your network engineering prompt library. And we close with a blast from the past: AI memory, the ReAct prompt samples, and the big-picture agentic AI note.
>
> **Jess:** Let's start at the bottom. The lecture opens with "LLMs are stateless." But I've had long conversations with chat models that clearly remember what I said ten messages ago. So in what sense are they stateless?
>
> **Marcus:** Good place to start. Where do you think that memory actually lives?
>
> **Jess:** In the context window?
>
> **Marcus:** Close, but go one level further. Who puts it in the context window?
>
> **Jess:** Oh. The client. The application resends the whole history on every call. The model itself keeps nothing between requests.
>
> **Marcus:** Exactly. The model is a pure function from tokens in to tokens out. Statefulness is something your code builds around it. The lecture defines agent state as everything the agent has to track during a task: the user query, the system instructions, the message history, any pending tool calls, and intermediate results.
>
> **Jess:** And it's called ephemeral, meaning it's thrown away when the run ends.
>
> **Marcus:** Right. It's working memory, not long-term memory. The lecture uses an online checkout as the analogy. The cart remembers your items, checkout uses them to compute a total, and the system knows where you are in the process. Close the tab and it's gone.
>
> **Jess:** So the big idea is to model the agent as a state machine.
>
> **Marcus:** Yes. Every step has the same contract. It takes in the current state, call it S, and returns an updated state, S prime. Then a transition function looks at that new state and picks the next step. The core loop goes like this. Prepare the messages. Call the LLM. Check whether the model asked for tools. If it did, run them, append the results, and go back to the LLM. If it didn't, produce the final answer and stop.
>
> **Jess:** That's the agent loop from the tools lesson, just drawn as a graph.
>
> **Marcus:** It's the same loop, with the structure made explicit. And here's a distinction worth holding onto. Is this graph a directed acyclic graph, like the workflows we diagrammed earlier?
>
> **Jess:** No. LLM to tools and back to the LLM is a cycle. So it's not acyclic.
>
> **Marcus:** And what does a cycle force you to add?
>
> **Jess:** A stop condition. And, I'm guessing, a second stop condition for when the first one never fires.
>
> **Marcus:** That's exactly the point your note makes. The lecture's loop has no step budget. If the model keeps requesting tools, it loops forever. Production systems add a maximum iteration count or a token budget as a second way out.
>
> **Jess:** Now the part I want to push on. The lecture says this design makes agents "deterministic." The model is still sampling, though.
>
> **Marcus:** Your note already calls that out, and it's right to. What's deterministic is the control flow given a state. If tool calls are present, code always routes to the tool step. But the LLM step itself is stochastic, so two runs of the same query can take different paths. One run makes one tool call, another makes three.
>
> **Jess:** So what you really get is traceability, not determinism.
>
> **Marcus:** Well put. To reproduce a run, you have to record the model's outputs, not just rerun the code. The lecture also calls conditional routing "a lightweight form of self-awareness." I'd retire that phrase. It's an if-statement that reads a field the model wrote. Calling it self-awareness is like calling your thermostat introspective.
>
> **Jess:** Fair. So the useful framing is: the model decides whether tools are needed by writing into state, and code decides what happens next by reading it.
>
> **Marcus:** Yes, and that split keeps control flow inspectable. Okay, now some math. Your note works out the cost of carrying the full history. Say the first prompt is a thousand tokens, and each loop adds five hundred. Over six LLM calls, how many input tokens do you send in total?
>
> **Jess:** Call one sends a thousand. Call two, fifteen hundred. Each call adds five hundred, so it's six thousand of base, plus five hundred times zero plus one plus two plus three plus four plus five. That's five hundred times fifteen, so seventy-five hundred. Thirteen thousand five hundred total.
>
> **Marcus:** Correct. Now double the run to twelve calls.
>
> **Jess:** Twelve thousand base, plus five hundred times sixty-six, which is thirty-three thousand. So forty-five thousand. That's more than three times the cost for twice the steps.
>
> **Marcus:** That's quadratic growth. The takeaway is that deciding what stays in state isn't only about correctness. It's one of the biggest cost levers you have. Trim old turns, summarize them, or store large tool outputs by reference instead of pasting them in.
>
> **Jess:** Okay, let's move to the code. The implementation note describes state machine dot p y as a workflow engine with no AI in it. Why does an AI course have you build a file with no model calls?
>
> **Marcus:** Because the orchestration should be separate from the model. The engine only knows how to sequence steps and carry state between them. An LLM call is just a step function. A tool call is a step function. A human review is a step function. That gives you three benefits. You can test the routing with plain Python before spending a single token. You can swap models without touching the engine. And code, not the model, decides what runs next.
>
> **Jess:** And the demo proves it with arithmetic. One workflow adds one and then doubles, which is the prompt chaining shape. The other increments a counter until it hits a max, which is the agent loop shape.
>
> **Marcus:** Right. Replace "count is less than max" with "the model requested tools," and you have the agent loop. Now, a question about how updates are merged. A step returns only the fields it changed, and the engine merges them into the old state. Suppose your LLM step returns messages equal to a list holding only the new reply. What happens to the history?
>
> **Jess:** It gets merged in, so the new message is added to the list?
>
> **Marcus:** That's the reasonable assumption, and it's the trap. The merge is a shallow overwrite. The key is replaced wholesale. Your history is now a list with one item in it, and on the next call the model has forgotten the whole conversation.
>
> **Jess:** So I have to return the old list plus the new message every time.
>
> **Marcus:** Every time. That's exactly why LangGraph lets each field declare a reducer, so the messages field can say "append" while the tool calls field says "overwrite." This engine has no reducers, so you do it by hand. Related bug: the tool step has to clear the pending tool calls. If you forget, what happens?
>
> **Jess:** The router still sees tool calls after the next LLM step, so it runs the same tools again. Duplicate side effects, maybe a loop that never ends.
>
> **Marcus:** Which brings us back to the cold open. I need to correct your note here, because the code moved under it. The implementation note was written Saturday evening. The state machine file in your notebooks folder was saved again about two hours later, and the current version doesn't match several things the note describes.
>
> **Jess:** Like what?
>
> **Marcus:** First, the note says run takes a max steps argument and raises an error past the cap. The current run method has no max steps at all. It's a plain while loop. A model that keeps asking for tools will loop until something else stops it. Second, the note says a condition can only route to targets you declared in connect, and that a hallucinated step name gets rejected. In the current code, the condition's return value isn't checked against the declared targets. An unregistered name fails with a key error, but any registered step is reachable, declared edge or not.
>
> **Jess:** So the safety property my note praises isn't really there.
>
> **Marcus:** Not in this version. Third, the note says calling connect twice on the same source silently drops the first edge. The current code appends transitions to a list. If they resolve to more than one next step, it raises a not-implemented error about parallel execution. Fourth, the termination step now ends the loop before it's snapshotted, so the counter demo gives eleven snapshots, not twelve. And the merge now quietly drops any returned key that isn't in the schema. That's a bit stricter than the note says, but a typo in a field name now disappears silently instead of crashing.
>
> **Jess:** That last one would be a nightmare to debug. My step "works" and the field just never updates.
>
> **Marcus:** Exactly. The conceptual lessons in the note still hold, including shallow overwrite, clearing tool calls, and keeping state JSON-friendly. But re-check the mechanics against the current file, and update the self-test question about a maximum value of ninety-eight, because there's no budget to compute against anymore. If you want that guard, add it yourself. Count the steps, and raise once the count passes a limit.
>
> **Jess:** Let me connect this to the design question at the end of both notes. Human approval before any tool that sends email. Where does it go?
>
> **Marcus:** You tell me.
>
> **Jess:** A conditional edge after the LLM step. Email tool calls go to an approval step, other tool calls go to tools, and no tool calls goes to termination. From approval, approved goes to tools, and rejected goes back to the LLM with a message saying the user declined.
>
> **Marcus:** Good. And what does that do to the idea that state is ephemeral?
>
> **Jess:** It breaks it. If a human takes three hours to approve, the process can't just sit in memory. You'd have to save the state and the current step ID, then reload it later.
>
> **Marcus:** That's the key insight in your note: human in the loop forces ephemeral state to become durable. And because every step already returns a clean state object, checkpointing is cheap. You save S after each step under a run ID. That's the whole trick behind durable execution.
>
> **Jess:** Last implementation question. Snapshots deep-copy the entire state after every step. Doesn't that have the same problem as the token math?
>
> **Marcus:** Same shape, yes. If the message list grows each loop, snapshot memory grows quadratically with the number of steps. That's fine for a teaching engine. At scale you'd store diffs or share structure between snapshots. And one security point: tool output written into messages flows straight into the next prompt, and every snapshot keeps it. So prompt injection defenses belong in the step functions, and secrets never belong in state.
>
> **Jess:** Rapid review time. Let me start with prompt chaining, since the state machine's linear demo is literally a chain.
>
> **Marcus:** Go for it. What's the one thing the refinery demo is missing?
>
> **Jess:** Intermediate validation. Four persona agents pass free text forward, and nothing checks it. The distillation planner can return percentages that add up to ninety, and the optimizer happily builds a plan on top of that.
>
> **Marcus:** And the fix in your improved version?
>
> **Jess:** A run step helper. Call the model, run validators, and if anything fails, re-prompt with the specific errors. After three attempts, raise loudly. In the fake model test, the allocation error got fixed on the second try, and the missing strategic notes section failed all three times and stopped the chain.
>
> **Marcus:** Good. Two gotchas. Step four takes two earlier outputs, so it's really a small directed acyclic graph, not a straight line. And the market analyst is asked for current pricing with no data source, so any specific price it gives is invented. Also notice the worst case: three attempts on each of five calls is fifteen calls. Gates aren't free.
>
> **Jess:** Task decomposition is the math behind that. End-to-end success is the product of the step success rates. One prompt at seventy percent, versus three steps at ninety-five percent, gives about eighty-six percent. That's a win.
>
> **Marcus:** And six steps at ninety-three percent?
>
> **Jess:** Point nine three to the sixth is about sixty-five percent. Worse than the single prompt. So more steps isn't automatically better.
>
> **Marcus:** Right. Split where you can write a check, and put the deterministic work in code. One caution on that formula: it assumes the steps fail independently and that any failure kills the run. Gates with retries break that assumption in your favor, which is the whole point of pairing decomposition with validation.
>
> **Jess:** Model evaluation. The trap I always remember is the outage classifier. Ninety-six percent accuracy sounds great, until you notice that always saying "no outage" gets ninety percent.
>
> **Marcus:** So which metric do you care about there?
>
> **Jess:** Recall, because a missed outage costs far more than a false alarm. Then set a floor on precision so the NOC isn't buried in false alarms.
>
> **Marcus:** And the other gotcha: with two hundred test items at eighty-five percent, the ninety-five percent confidence interval is about plus or minus five points. So when one prompt scores eighty-eight and another scores eighty-five, you can't call a winner from that alone. Use a paired test on the same items.
>
> **Jess:** Knowledge graphs. Vector search finds text that sounds relevant. A graph follows explicit relationships. "Which business accounts sit behind OLT seven, port three" is three hops, and a graph query answers it exactly.
>
> **Marcus:** And when the LLM writes that query for you?
>
> **Jess:** Treat it as untrusted code. Read-only credentials, block write clauses, add a limit, set a timeout.
>
> **Marcus:** One clarification on your note. The takeaway says GraphRAG means using vectors to find entry nodes, then traversing the graph. That's one common pattern. But earlier in the same note, GraphRAG means the Microsoft approach of building community summaries for global questions. People use the term loosely, so when someone says GraphRAG, ask which one they mean.
>
> **Jess:** And the network engineering prompt library ties a lot of this together. The rule I like is "engineering tools compute, the LLM reviews." Link budgets and subnet math come from real tools. The model questions the assumptions.
>
> **Marcus:** That's task decomposition applied to a job. And the operational readiness prompt is a gate check with hard blockers. If monitoring, backup power, out-of-band access, or site access info isn't ready, the verdict is "not ready," whatever else looks good. It's the same idea as the run step validator, applied to a tower handoff.
>
> **Jess:** Blast from the past. AI memory. Today's notes said state is working memory. So where exactly is the line between state and memory?
>
> **Marcus:** What do you think?
>
> **Jess:** Scope. State lives for one run. Memory persists across runs: episodic for events, semantic for facts, procedural for how-to. But once I checkpoint state to a database, it starts to feel like memory.
>
> **Marcus:** That's the right tension. I'd draw the line by purpose. A checkpoint exists so this run can resume. Memory exists to shape future runs. And memory adds a risk that state doesn't: if an injected "preference" gets written to long-term memory, a one-time attack turns into a permanent one.
>
> **Jess:** The ReAct samples are the same state machine wearing a prompt. Think, act, observation, repeat until the final answer tool.
>
> **Marcus:** And look at what the network examples add that the financial one doesn't: read-only tools, citing observations, and "if it's inconclusive after eight steps, say so." That eight-step rule is a step budget, written in the prompt. One design point worth debating: the vulnerability triage rules put an internet-facing, unpatched, but mitigated appliance at P3, the same priority as a fully patched one. That's consistent with the rules as written, but I'd argue it deserves its own tier.
>
> **Jess:** And the agentic AI note gives the umbrella principle: grant the minimum autonomy that solves the task.
>
> **Marcus:** With the expected-value math to back it up. One percent errors at two thousand dollars each is twenty dollars of expected loss per task. A five-dollar review that catches ninety percent of errors brings it down to seven. Approval steps are cheap insurance, and today you saw how to wire one into a state machine.
>
> **Jess:** Okay, takeaways.
>
> **Marcus:** Takeaway one. Statefulness lives in your code, not the model. The state machine gives you traceable control flow, not deterministic behavior, so record model outputs if you want to replay a run.
>
> **Jess:** Takeaway two. Merge semantics are a correctness issue. Shallow overwrite silently wipes history, stale tool calls re-run tools, and full history makes cost grow quadratically.
>
> **Marcus:** Takeaway three. Verify the safety properties in the code, not in your notes. The loop guard and the declared-target check your note describes aren't in the current file, and human approval turns ephemeral state into something you have to checkpoint.
>
> **Jess:** And the think-about-it question?
>
> **Marcus:** Suppose you build the NOC triage agent from the ReAct samples on top of the current state machine, which has no step budget and doesn't check routes against declared edges. You add an approval step for any write action. What kind of budget do you add: steps, tokens, or wall-clock time? And what exactly do you need to checkpoint so an approval that arrives at seven a.m. can resume the run without replaying, and paying for, the LLM calls from two a.m.?
>
> **Jess:** That's a good one. I'm Jess.
>
> **Marcus:** And I'm Marcus. Clear your tool calls, and we'll see you tomorrow.
