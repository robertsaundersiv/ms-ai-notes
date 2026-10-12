---
title: "MS AI Daily – 2026-10-02"
type: podcast
created: 2026-10-02
duration_min: 17
covers:
  - "[[CEO Prompt Library]]"
  - "[[COO Prompt Library]]"
  - "[[Customer Service Director Prompt Library]]"
  - "[[Financial Controller Prompt Library]]"
  - "[[IT Director Prompt Library]]"
  - "[[Marketing Director Prompt Library]]"
  - "[[ReAct prompt Samples]]"
  - "[[Planning Agents]]"
  - "[[Model Predictive Control (MPC)]]"
  - "[[Agentic Workflow Patterns]]"
  - "[[Tool Use]]"
  - "[[Artificial Intelligence]]"
  - "[[Chain-of-Thought and ReAct]]"
  - "[[Implementing LLM Feedback Loops]]"
tags:
  - podcast
  - review
---

# MS AI Daily – 2026-10-02

![[MS AI Daily - 2026-10-02.mp3]]

> [!abstract] In this episode
> Marcus and Jess read the six Wi-Fiber prompt libraries as one system. Two things hold them together: churn dollars as the shared unit, and the "compute, don't ask" rule. They then check whether the technique labels are accurate. The four-persona "self-consistency" prompts are really multi-perspective panels. Per-competitor "Tree-of-Thought" is really parallelization. The analyst/skeptic prompts are evaluator-optimizer done as role-play. The episode closes on where gates belong: in code, in Sonar, or with a human approver, not in a model's own PASS/FAIL self-check.

## Segments
- **Cold open:** The four "independent" advisors in [[CEO Prompt Library]] prompt 3
- **Deep dive:** [[CEO Prompt Library]], [[COO Prompt Library]], [[Customer Service Director Prompt Library]], [[Financial Controller Prompt Library]], [[IT Director Prompt Library]], [[Marketing Director Prompt Library]]
  - *Common currency and compute-don't-ask:* CEO prompt 7, COO prompts 2 and 13
  - *Are the technique labels accurate:* CEO prompts 2, 3, 11 and 30; Marketing prompts 3 and 8; IT prompt 4; Controller prompt 8
  - *Where gates live:* CS prompts 1 and 6; Marketing prompt 4; CEO prompt 21 / Controller prompt 4 break-even gates; IT prompt 8 / COO prompt 29 determinism check
- **Rapid review:** [[ReAct prompt Samples]], [[Planning Agents]], [[Model Predictive Control (MPC)]], [[Agentic Workflow Patterns]], [[Tool Use]], [[Artificial Intelligence]]
- **Blast from the past:** [[Chain-of-Thought and ReAct]], [[Implementing LLM Feedback Loops]]

> [!warning] Corrections raised in the episode
> - [[CEO Prompt Library]] prompts 3 and 30 are labeled *Self-Consistency*. Self-consistency means sampling the **same** prompt several times and taking a majority vote. Running four different personas and looking at where they disagree is a multi-perspective panel (parallelization with varied prompts and a synthesizer).
> - [[Marketing Director Prompt Library]] prompt 3 is labeled *Tree-of-Thought*, but its branches are separate subtasks (one per competitor), not alternative answers that get pruned. That makes it parallelization, which is the label CEO prompt 12 uses for the same per-market structure.
> - The single-prompt "Tree-of-Thought" and "evaluator-optimizer" prompts approximate those patterns in one pass. They can't really backtrack, and the evaluator is the same generation it is judging.
> - [[Chain-of-Thought and ReAct]] draws CoT as "decompose → reason → validate → answer". Plain CoT doesn't validate anything. Validation has to be added, for example with self-consistency, a verifier or a tool.

## Think about it
Take the CEO's Priority Trade-Off Decision Memo (four advisors) and rebuild it as a real workflow instead of one prompt. Which pattern or combination of patterns would you use? Should the synthesizer vote the disagreement away or surface it? Name one failure mode the single-prompt version hides that your version would expose, and one new failure mode your version introduces.

> [!quote]- Transcript
> **Marcus:** Picture this. You're the CEO of a regional internet provider, and you want to know whether to raise prices five dollars. So you write one prompt: act as four independent advisors, a CFO, a customer advocate, an operator, and a board member, each answering without seeing the others. Then synthesize. Here's my question. How independent are those four advisors, really?
>
> **Jess:** Well, they're all the same model, writing in the same response. So advisor four can literally read what advisors one through three just wrote.
>
> **Marcus:** Exactly. The prompt says "without seeing the others," the model nods politely, and then it sees them anyway. That gap between what a prompt claims to do and what the system actually does is today's whole episode. Welcome to MS AI Daily. It's Friday, October second, twenty twenty-six. I'm Marcus.
>
> **Jess:** And I'm Jess. And I'll admit, I read right past that "without seeing the others" line the first time.
>
> **Marcus:** Here's the plan. The big new material is the set of prompt libraries built for Wi-Fiber, the fictional fixed wireless provider. CEO, COO, Customer Service Director, Financial Controller, IT Director, and Marketing Director. We'll treat them as one system, not six documents. We'll look at the design rules they share, check whether the technique labels are honest, and talk about where gates should actually live.
>
> **Jess:** Then a rapid review: ReAct prompt samples, planning agents, model predictive control, the workflow patterns hub, tool use, and the Artificial Intelligence foundations note.
>
> **Marcus:** And the blast from the past is Chain-of-Thought versus ReAct, plus the feedback loop lab, which contains a confession.
>
> **Jess:** Okay, start broad. That's a hundred prompts across six libraries. What holds them together?
>
> **Marcus:** Two things. First, a single business variable that everything maps to, which is churn. The CEO library says to start with prompt seven, the value of one point of churn. Once a tenth of a point of monthly churn has a dollar value, a generator at a tower, a save-desk offer, and a marketing channel can all be compared in the same unit.
>
> **Jess:** So churn dollars are basically the loss function for the whole company.
>
> **Marcus:** That's a nice way to put it, and the analogy is useful and dangerous at the same time. Useful, because it makes trade-offs comparable. Dangerous, for the reason any single objective is dangerous: people optimize whatever you measure. The CEO's scorecard cascade actually anticipates that. Its last stage asks what behavior each goal rewards and whether it can be gamed, like reclassifying cancel reasons or quietly excluding outages from uptime.
>
> **Jess:** Goodhart's law, with an org chart.
>
> **Marcus:** Pretty much. And the COO library supplies the prerequisite, which is prompt thirteen: one definition of uptime. Customer-experienced availability, meaning one minus the subscriber-minutes impacted, divided by total subscriber-minutes. You can't link uptime to churn if every department counts uptime differently.
>
> **Jess:** Okay. What's the second thing holding it together?
>
> **Marcus:** A rule that shows up in the shared rules of every library: compute, don't ask. Let me check you on it. Why not just paste the raw outage export and ask the model for churn rates by exposure band?
>
> **Jess:** Because it'll do the arithmetic in its head and get it wrong?
>
> **Marcus:** That's part of it. What's the bigger part?
>
> **Jess:** Hmm. Reproducibility? If I rerun it, I might get a different number.
>
> **Marcus:** Right, and auditability. An obviously wrong number, you'll catch. A plausible number that's slightly wrong, sitting in a confident board memo, you won't. So the pattern is: the model designs the analysis, a spreadsheet or SQL computes it, and the model interprets the results. COO prompt two literally says plan, then stop and show me, and it only interprets after you paste real results. The CEO library adds a labeling rule on top: every number is marked actual, calc, or assumption.
>
> **Jess:** That's the same idea as the calculate tool in the capacity-planning ReAct sample.
>
> **Marcus:** Same principle, different packaging. In an agent, the calculator is a tool. In a human-in-the-loop prompt library, the calculator is you, with Excel.
>
> **Jess:** Okay, back to the cold open. The four-advisor prompt is labeled self-consistency. Is that label wrong?
>
> **Marcus:** I'd call it mislabeled, and it's worth fixing in your notes. Self-consistency, from Wang and colleagues, means sampling the same prompt several times at nonzero temperature and taking a majority vote on the final answer. Your Chain-of-Thought note describes it exactly that way. The CEO's trade-off memo does something else: four different personas, so four different prompts, and the point is not to vote. The note itself says that if the advisors disagree, the decision really does involve a trade-off.
>
> **Jess:** So in that prompt, disagreement is the signal. In self-consistency, disagreement is the noise you vote away.
>
> **Marcus:** Perfectly put. What the CEO prompt does is closer to a multi-perspective panel, or parallelization with deliberately different prompts and a synthesizer at the end. Useful technique, wrong name. And the note does include one honest line: run each advisor in a separate chat if you want real independence. That's the fix for our cold open.
>
> **Jess:** Prompt thirty, the mergers and acquisitions screen, has the same label. Three reviewers plus a pre-mortem.
>
> **Marcus:** Same label, same correction. The pre-mortem is great, by the way. "It's two years later and this deal destroyed value. Why?" That's a cheap way to puncture deal enthusiasm.
>
> **Jess:** What about Tree-of-Thought? That label is everywhere. The three-year plan, the price increase, capital allocation, the controller's budget prioritization.
>
> **Marcus:** There I'd say it's approximately right, with an asterisk. Real Tree-of-Thought, from Yao and colleagues, is a search. Multiple model calls generate partial thoughts, an evaluator scores them, and the system can backtrack out of dead ends. A single prompt that says "generate four strategies, evaluate each, prune, recommend" is a Tree-of-Thought shaped prompt, done in one pass. It can't truly backtrack, and the evaluator is the same model that just wrote the branches.
>
> **Jess:** Does that matter in practice, though? The output still reads like a decision tree.
>
> **Marcus:** For a CEO brainstorming, the one-pass version is often fine. The structure alone fights the "just keep doing what we already do" default. But if you built it into a system, you'd want separate calls, so the evaluation isn't anchored on the branch it just finished writing. Now, a quiz. Marketing prompt three, the competitive battlecard, is also labeled Tree-of-Thought. It evaluates each competitor as its own branch, then compares. Is that Tree-of-Thought?
>
> **Jess:** I want to say yes. There are branches, and then there's a comparison across them.
>
> **Marcus:** Plausible, and that's the trap. What are the branches alternatives to?
>
> **Jess:** Oh. They're not alternatives. Cable, five G home internet, and satellite aren't competing answers to the same question. They're independent subtasks.
>
> **Marcus:** Right. Tree-of-Thought branches are candidate solutions to one problem, and you prune the losers. You don't prune a competitor because its analysis scored low. Per-competitor analysis is parallelization. And the CEO library gets this right: prompt twelve does the same per-market split and labels it parallelization. So the libraries actually disagree with each other on this one, and the CEO version is the correct label.
>
> **Jess:** What about the IT Director's tool rationalization prompt? Two or three consolidation options per overlap, evaluate each, prune the ones where migration effort outweighs the benefit.
>
> **Marcus:** That one is genuinely Tree-of-Thought shaped. Alternatives for the same decision, pruned on a criterion. Hold those two side by side and you'll never confuse the patterns again.
>
> **Jess:** Last label. Evaluator-optimizer. The CEO's retention portfolio review has an analyst and a skeptic, and marketing's referral program has a designer and a critic.
>
> **Marcus:** Those are evaluator-optimizer as role-play. One critique, one revision, inside a single response. The real pattern from your workflow patterns hub is a code loop with an LLM judge and a stop condition. The role-play version still helps, because the skeptic's questions are good ones. Was there a control group? Did the season change? Is the metric gameable? But it's the pattern wearing a costume.
>
> **Jess:** Which leads into gates. A lot of these prompts end with "self-check each rule, pass or fail." The board narrative, the CEO letter to customers, the controller's not-now budget message. Is that a gate?
>
> **Marcus:** It's a weak one. Ask who's grading. The same generation that wrote the letter now announces that the letter passed. That's like letting the intern approve their own expense report. It's useful as a nudge, and it makes the rules visible to the human reviewer, who is the real gate. The libraries are honest about that part. A person approves before anything goes out.
>
> **Jess:** So which prompts put the gate in the right place?
>
> **Marcus:** Look at the Customer Service library. Prompt one, the churn-signal classifier, has the model produce labels with verbatim evidence. But the routing rule, high risk goes to retention, runs in code or in Sonar automation. Prompt six, post-outage outreach: the customer segments are computed in Sonar, not by the model. The model only writes the messages.
>
> **Jess:** So the model handles language, and code handles decisions that have to be consistent every time.
>
> **Marcus:** Yes. And that echoes the security point in your MPC note: constraints have to be enforced outside the model, because a model can plan around a constraint that only lives in its prompt. Marketing prompt four is a nice business version. Capacity-aware acquisition. Every tower sector gets labeled open, limited, closed, or opening soon before a dollar of ad spend goes out. And if thresholds aren't provided, the model can propose them, but it has to flag them for network approval.
>
> **Jess:** And the cost-cutting gates? The CEO's churn-safe cost reduction and the controller's operations-safe expense reduction look almost identical.
>
> **Marcus:** They are, and that's a feature. Both compute a break-even: how much extra churn would wipe out the savings? Say trimming spare parts saves fifty thousand a year, and a tenth of a point of churn is worth several times that. The break-even churn is tiny, so the cut gets blocked. It's a logic gate, and its threshold comes from CEO prompt seven. That connective tissue between libraries is the real design.
>
> **Jess:** One more. The IT Director's automation screener and the COO's AI roadmap both begin with "what can be done by rules or code only, no LLM."
>
> **Marcus:** That's the most graduate-level idea in the whole set. A determinism check before you pick a pattern. Then you choose the simplest pattern that meets the quality bar, which is exactly the design principle from the workflow patterns hub. The IT version adds one line I love: check whether Sonar already does this natively. A surprising number of AI projects are lovingly rebuilding a checkbox the vendor shipped three releases ago.
>
> **Jess:** A very expensive checkbox.
>
> **Marcus:** With a vector database attached, naturally. Okay, rapid review. Jess, the ReAct prompt samples. What do the network and IT examples add that the original financial and clinical samples don't?
>
> **Jess:** Guardrails. Read-only tools, a step limit with an honest "inconclusive" exit, citing an observation for every claim, redacting secrets, and treating advisory text as data rather than instructions.
>
> **Marcus:** Good. One gotcha worth checking yourself. The capacity sample projects utilization as sixty-three, plus sixty-three minus forty-one, divided by two. Why divide by two?
>
> **Jess:** Forty-one to sixty-three happened over two quarters, so that's eleven points per quarter. Sixty-three plus eleven is seventy-four, which is over the seventy percent upgrade trigger.
>
> **Marcus:** The math checks out, and notice it went through the calculate tool, not the model's head. Planning agents, quickly.
>
> **Jess:** Plan, verify, execute, observe, re-plan. Verification checks that the tools exist, that dependencies form a graph with no cycles, and that write steps carry approval flags.
>
> **Marcus:** And the number from the self-test?
>
> **Jess:** Six steps at ninety-five percent each is about seventy-three and a half percent end to end. If re-planning recovers half the failures, each step is effectively ninety-seven and a half percent, which gets you to about eighty-six percent.
>
> **Marcus:** Which ties straight into model predictive control. Give me MPC in one sentence.
>
> **Jess:** Predict over a horizon, optimize under constraints, apply only the first move, measure, and re-plan. The feedback comes from re-planning, not from a gain.
>
> **Marcus:** And the gotcha in the worked example. At step one, the plan's second move was minus two. But at step two, the controller actually applied minus two point four, because it re-planned from the new state. Plans aren't commitments. For agents, plan-and-execute with re-planning is MPC proper. Without re-planning, it's open-loop, and fragile.
>
> **Jess:** And that note is careful to say the agent mapping is its own analogy, not an established result.
>
> **Marcus:** Good scholarship. Keep it that way. Workflow patterns hub. Name the five, and tell me who controls the flow in the last one.
>
> **Jess:** Prompt chaining, routing, parallelization, evaluator-optimizer, and orchestrator-workers. In orchestrator-workers, an LLM decides the subtasks at runtime.
>
> **Marcus:** Which is why the COO's customer journey failure map is a fair use of it. The orchestrator writes questions per journey stage, and each worker sees only its own department's data. Tool use. Who executes a tool call?
>
> **Jess:** The host application. The model only proposes a structured call. And the classic exfiltration risk is private data access, untrusted content, and an outbound channel all in one agent. Remove one of the three.
>
> **Marcus:** Last one, the Artificial Intelligence foundations note. What misconception does it kill?
>
> **Jess:** That symbolic AI is obsolete. Rules, search, and graphs are still the reliable backbone of agents.
>
> **Marcus:** And today proves it. Every one of these libraries pairs an LLM with rule gates and SQL. It's the ticket-routing example from that note: symbolic, supervised, and LLM plus rules, and production systems mix all three.
>
> **Jess:** Blast from the past time.
>
> **Marcus:** Chain-of-Thought and ReAct. Jess, the practical mental model?
>
> **Jess:** Chain-of-Thought when the model already has the information and mainly needs to reason. ReAct when it has to go get information or interact with a real system.
>
> **Marcus:** The detail I want resurfaced is unfaithful reasoning. The visible chain of steps can be a rationalization, not a true trace of how the answer was produced. That's exactly why those pass-or-fail self-checks aren't proof. One small quibble with that note, though. It sketches Chain-of-Thought as decompose, reason, validate, answer. Plain Chain-of-Thought doesn't validate anything on its own. Validation is something you add, with self-consistency, a verifier, or a tool.
>
> **Jess:** Fair. And the feedback loop lab?
>
> **Marcus:** My favorite confession in the vault. The loop printed "Success" while making zero API calls, because the generation lines were commented out and old variables were still sitting in the Jupyter kernel.
>
> **Jess:** Hidden state making a broken loop look like a working one.
>
> **Marcus:** And here's the connection to today. In that lab, the instruction telling the model to "iterate until all tests pass" did nothing, because a single completion can't run code. Only the harness iterates. That's the same lesson as the four advisors. A prompt can describe a process. Only the system around it can actually run one.
>
> **Jess:** Okay, wrap it up for us.
>
> **Marcus:** Three takeaways. One: a technique label is a claim about what the system does. Self-consistency means sampling and voting; four personas in one response is a panel. Tree-of-Thought means alternatives that get pruned; per-competitor analysis is parallelization. Name it correctly and you know what you'd have to build.
>
> **Jess:** Two: the model designs and explains, and code computes and decides. Compute, don't ask. Segments in Sonar, routing rules in code, and a common currency like churn dollars, so every gate has a real threshold.
>
> **Marcus:** Three: whatever a prompt promises, whether that's independence, iteration, or self-checking, is only real if something outside the model enforces it. Separate calls, a harness, or a human approval.
>
> **Jess:** And the think-about-it question?
>
> **Marcus:** Take the CEO's priority trade-off memo, the four advisors, and rebuild it as a real workflow instead of a single prompt. Which pattern, or combination of patterns, would you use? What should the synthesizer do with disagreement: vote it away, or surface it? Then name one failure mode that the single-prompt version hides and your version would expose, and one new failure mode your version introduces.
>
> **Jess:** That second half is a little mean.
>
> **Marcus:** Affectionately mean. That's the show. I'm Marcus.
>
> **Jess:** And I'm Jess. See you next time on MS AI Daily.
