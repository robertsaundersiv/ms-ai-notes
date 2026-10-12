---
title: "MS AI Daily – 2026-09-28"
type: podcast
created: 2026-09-28
duration_min: 33
covers:
  - "[[Agentic Workflow Patterns]]"
  - "[[Implementing Prompt Chaining Workflow]]"
  - "[[Implementing Routing Workflow]]"
  - "[[Implementing Parallelization Workflow]]"
  - "[[Evaluator-Optimizer Workflow]]"
  - "[[Implementing Evaluator-Optimizer Workflow]]"
  - "[[Reinforcement Learning (RL)]]"
  - "[[Prompt Instruction Refinement]]"
  - "[[AI Reliability]]"
  - "[[LLM Evaluation]]"
  - "[[Model Context Protocol]]"
  - "[[AI Memory]]"
  - "[[Agentic AI]]"
  - "[[Vector Databases]]"
tags:
  - podcast
  - review
---

# MS AI Daily – 2026-09-28

![[MS AI Daily - 2026-09-28.mp3]]

> [!abstract] In this episode
> The episode opens with a recipe optimizer that prints "All dietary constraints satisfied!" for a rejected recipe, because "APPROVED" is a substring of "NOT APPROVED". Marcus and Jess use that bug to frame the four workflow-pattern exercises: in each one, the model mostly did its job, and the failures lived in the seams where plain code acts on model text. The recurring lessons are format contracts with exact checks, failing loudly instead of silently, and making sure a checker knows something the generator doesn't.

## Segments
- **Cold open:** the "NOT APPROVED" substring bug from [[Implementing Evaluator-Optimizer Workflow#^approval-test]]
- **Deep dive – the map:** [[Agentic Workflow Patterns]], with a callback to the autonomy levels in [[Agentic AI#^autonomy-levels]]
  - "Who controls the flow" as the key column. Orchestrator-workers vs parallelization: is the plan code or output? That decides whether you can unit-test it or need evals.
- **Deep dive – prompt chaining:** [[Implementing Prompt Chaining Workflow]]
  - Fan-in makes the refinery chain a small DAG. The hidden extraction call does selective context passing. No intermediate validation. `run_step` re-prompts with specific errors and fails loudly.
  - Clarification: temperature 0 is not guaranteed deterministic, and a retry only helps when something changes (here, the error message goes into the prompt).
  - The market analyst's "current" prices are invented. The note's own caveat: the percentage regex miscounts ranges.
- **Deep dive – routing:** [[Implementing Routing Workflow]]
  - Substring dispatch misroutes ("Pricing Strategist Agent, it will need Product Researcher input" goes to product), leaves lowercase replies unrouted, and crashes on `None`. The fix: a closed label set with `other`, normalization, exact match, one retry, a fallback, a dispatch table, and a status field.
  - The pricing branch is a fixed-plan orchestrator inside a router. Closed labels stop injected text from creating routes but not from steering among them. Grounding is the bigger risk.
- **Deep dive – parallelization:** [[Implementing Parallelization Workflow]]
  - The GIL misconception: threads do overlap I/O-bound API calls. Swallowed thread exceptions plus a global dict give a `KeyError` on run 1 and contract A's compliance findings in contract B's report on run 3.
  - The fix: `ThreadPoolExecutor` with `future.result()`, local results, the synthesizer told what's missing, a minimum-coverage rule, and a partial status. Also covers the timeout caveat, max-plus-summary latency (33 s vs 55 s), no token savings, and scoring recall against an expected-findings checklist.
- **Deep dive – evaluator-optimizer:** [[Evaluator-Optimizer Workflow]], [[Implementing Evaluator-Optimizer Workflow]]
  - Criteria, Actionable feedback, Stopping conditions. Refinement needs task + previous attempt + feedback. Return the best attempt, not the last. 1 − 0.5³ = 0.875. The evaluator is a classifier, and false accepts cap quality. Self-critique limits.
  - The three recipe-loop bugs map one-to-one onto the theory (a missing previous recipe, fragile approval strings, last instead of best).
  - Nuance: the improved version's "code checks" count fields the generator self-reported (`is_vegetable`, `total_minutes`). They catch miscounting, not mislabeling.
  - **Gap to fix in the note:** the improved `evaluate()` scores `len(CRITERIA) - len(failed)` from the LLM's reply, so a criterion the LLM omits counts as passed (fail-open). Loop over `CRITERIA` and treat a missing entry as a failure.
  - Judgment call: the improved loop returns the best recipe but keeps refining from the latest one, even after a regression.
- **Rapid review:** [[Reinforcement Learning (RL)]], [[Prompt Instruction Refinement]], [[AI Reliability]], [[LLM Evaluation]], [[Model Context Protocol]], [[AI Memory]], [[Agentic AI]]
  - In-context loop vs weights, GRPO's group baseline, and the note's DPO correction. Reward hacking is the same problem as gaming the evaluator.
  - Examples ≠ instructions. Refinement to the note: temperature 0 reduces noise but isn't deterministic, and you still need many inputs.
  - 0.9⁵ ≈ 0.59, and the gate-and-retry formula assumes independent retries. Silent failure.
  - With ±10 points on 50 items, a 4-point gain is noise. Validate the judge. pass@k vs pass^k.
  - MCP standardizes plumbing, not trust (tool poisoning, rug pulls). Tool selection is still a routing problem.
  - Stored memories are like a permanent stale dict and need a write gate. Expected loss of $50/task. Agent-washing: who decides the next step?
- **Blast from the past:** [[Vector Databases]]
  - Grounding the router's specialists with hybrid search and a reranker. A stale index, a stale dict, and poisoned memory are the same bug at three time scales. Similarity ≠ relevance, and absence ("contracts lacking an indemnification clause") is hard to embed.

## Think about it
You combine today's patterns: a router sends high-stakes contracts to the parallel reviewer, and you want an evaluator-optimizer loop for quality. You can put the evaluator on each specialist's analysis before synthesis, or once on the final synthesized report. Which do you choose? Consider the worst-case call count and latency, which failures each placement can detect (a missed clause vs two specialists contradicting each other), and what the synthesizer should be told when one specialist's loop hits its cap without passing.

> [!quote]- Transcript
> **Marcus:** Let's start with a puzzle. You build a recipe optimizer for someone with severe gluten, dairy, and nut allergies. The loop runs six times, and on the last attempt the evaluator says the recipe fails. Protein is too low, carbs are too high. Then the program prints, with a green check mark, "All dietary constraints satisfied!" How did that happen?
>
> **Jess:** Hmm. Did the loop return an earlier recipe that passed? Or did the success flag get set once and never reset?
>
> **Marcus:** Good guesses, and both of those are real bugs in other code. This one is dumber. The evaluator's reply started with "NOT APPROVED." The final check in the program asks whether the string "APPROVED" appears anywhere in the reply.
>
> **Jess:** Oh no. "APPROVED" is a substring of "NOT APPROVED."
>
> **Marcus:** It is. I'd call it the most passive-aggressive bug in the course. And it's not made up. You found it yourself when you tested the evaluator-optimizer exercise. Here's why it matters for today. The language model did its job. It rejected the recipe. The failure happened in the few lines of plain Python that turned the model's words into a decision.
>
> **Jess:** So the model worked and the glue failed.
>
> **Marcus:** That's today's theme: the seams. Welcome to MS AI Daily. It's Monday, September twenty-eighth, twenty twenty-six. I'm Marcus.
>
> **Jess:** And I'm Jess. So what's on the agenda?
>
> **Marcus:** You finished the implementation half of the workflow patterns section this weekend, so that's the deep dive. We'll start with the map of the five patterns. Then we'll work through four exercises: the refinery prompt chain, the retail router, the parallel contract reviewer, and the recipe evaluator-optimizer, plus its theory note. Then a rapid review covering reinforcement learning, prompt refinement, reliability, evaluation, the Model Context Protocol, memory, and your Agentic AI overview. The blast from the past is vector databases.
>
> **Jess:** Four exercises, and I'm guessing each one has a seam that breaks.
>
> **Marcus:** Each one has at least one. Let's go.
>
> **Marcus:** First, the map. Your hub note lists five patterns: prompt chaining, routing, parallelization, evaluator-optimizer, and orchestrator-workers. The most useful column in that table isn't the name. It's the column called "who controls the flow." Jess, walk down that column for me.
>
> **Jess:** Okay. Prompt chaining is code, in a fixed order. Routing is code plus an LLM classifier that picks a branch. Parallelization is code doing a fixed split, plus an aggregator. Evaluator-optimizer is a code loop with an LLM judge. And orchestrator-workers is where an LLM decides at runtime what the subtasks even are.
>
> **Marcus:** Right. So what's actually increasing as you go down that list?
>
> **Jess:** Flexibility. And cost and variance, according to the note.
>
> **Marcus:** And one more thing: how much of the control flow you've handed to the model. That's the same axis as the autonomy levels in your Agentic AI note. A fixed chain is level one, a routed workflow is level two, and orchestrator-workers starts to drift toward level three. The design principle in both notes is the same: pick the simplest pattern that meets the quality bar, and measure before you add complexity.
>
> **Jess:** Let me push on that. Isn't orchestrator-workers just parallelization where an LLM does the splitting? It feels like the same thing with a fancier name.
>
> **Marcus:** That's a fair challenge, and it's partly right. Both fan work out and gather it back. The difference is when the split is decided. In parallelization, you wrote the split in code before the request arrived: legal, compliance, financial, every time. In orchestrator-workers, the model looks at this particular request and invents the subtasks. That changes what you can test. You can write unit tests for a fixed split. A dynamic split needs evals over many inputs, because the plan itself is now an output that can be wrong.
>
> **Jess:** So the dividing line is whether the plan is code or output.
>
> **Marcus:** Exactly. Keep that in your pocket, because the router exercise blurs it in an interesting way.
>
> **Marcus:** Now the prompt chain. The course demo is a refinery optimization workflow.
>
> **Jess:** A refinery pipeline. So it's literally a pipeline.
>
> **Marcus:** Finally, a pipeline diagram where the pipes are real. There are four persona agents. A feedstock analyst describes the crude oil. A distillation planner proposes what percentage becomes each product. A market analyst looks at demand. And a production optimizer combines the plan with the market analysis to recommend a strategy. Each agent is a plain function wrapping one chat call, and the whole trick is that each output string gets pasted into the next prompt.
>
> **Jess:** Your notes say it isn't strictly linear, though.
>
> **Marcus:** Right, and that's worth seeing. The optimizer takes two earlier outputs, the distillation plan and the market analysis. That's fan-in, so the dependency structure is a small directed acyclic graph, not a line. There's also a hidden fifth LLM call between steps two and three. It extracts just the product names from the plan, so the market analyst gets a short list instead of the whole report. That's selective context passing, and it's a good instinct.
>
> **Jess:** So what's missing?
>
> **Marcus:** The thing the theory reading calls essential: intermediate validation. The planner is told to give percentages for each product, and nothing checks that they add up to a hundred. If the planner says ninety percent total, that wrong allocation flows straight into a confident final plan. As written, the demo shows how errors propagate rather than preventing it.
>
> **Jess:** And the improved version adds gates.
>
> **Marcus:** It adds a small helper called run step. It calls the model, runs a list of validators, and if any fail, it builds a new prompt containing the original task, the previous answer, and the specific error messages. For example, "Product allocation sums to ninety percent; it must sum to one hundred." After three failed attempts, it raises an exception instead of passing garbage downstream. In your fake-model test, the allocation error was fixed on the second attempt, and a missing section in the optimizer failed all three times and stopped the chain loudly.
>
> **Jess:** I like that it fails loudly. But quick question. The demo runs at temperature zero. Doesn't that make it deterministic, so retrying is pointless unless you change the prompt?
>
> **Marcus:** Two parts to that. First, temperature zero makes output more repeatable, but your note correctly says it's not guaranteed identical. Serving infrastructure can introduce small differences. Second, and this is the real point, run step does change the prompt. The retry includes the error message. That's what makes it a correction instead of a reroll. A blind retry at temperature zero is mostly the same call again, and you'd expect the same mistake.
>
> **Jess:** So a retry only helps if something about the input changes.
>
> **Marcus:** Or the model changes, or the sampling does. Hold that thought, because it comes back in the reliability review. Two more things from this note. The market analyst is asked for "current demand and pricing insights," and it has no live data. It will produce specific-sounding numbers it invented. The fix is a data tool, or at least telling it to label its figures as general rather than current. And your note flags a limit in its own validator. The percentage check grabs every number followed by a percent sign, so a line like "gasoline forty percent, range thirty-five to forty-five percent" gets miscounted. Headers and regular expressions are a weak contract. If code has to compute on something, ask for structured output.
>
> **Jess:** Which leads straight into routing, I'm guessing.
>
> **Marcus:** It does. The retail router has three specialists: a product researcher, a customer analyzer, and a pricing strategist. An LLM classifier reads the query and replies with an agent's name. Then an if-elif block checks whether the text "Product Researcher" appears in the reply, then "Customer Analyzer," then "Pricing Strategist." Quick quiz. The classifier replies, "Pricing Strategist Agent, it will need Product Researcher input." Where does the query go?
>
> **Jess:** The first check is whether "Product Researcher" is in the string, and it is. So it goes to the product researcher, even though the model clearly said pricing.
>
> **Marcus:** Exactly right. Misrouted by the model being helpful. And the other tests in your note: a lowercase reply, "pricing strategist agent," matches nothing because the check is case-sensitive, so the query is unrouted. And if the API returns empty content, you get None, and the substring check crashes with a type error.
>
> **Jess:** And the misroute is the worst of the three, because it doesn't look like a failure.
>
> **Marcus:** That's the key insight. The crash is annoying, but you see it. The misroute produces a fluent answer to the wrong question, and nobody notices. The fix follows a rule you'll use for the rest of your career: every LLM output that code acts on needs a format contract and a check. Here that means a closed set of short labels: product research, customer analysis, pricing, and other. Normalize the reply by trimming whitespace, stripping quotes and periods, and lowercasing it. Then require an exact match. If the label is invalid, re-prompt once and name the valid options. If it's still invalid, fall back to "other."
>
> **Jess:** Why does "other" matter so much? It seems like a throwaway category.
>
> **Marcus:** Without it, every query gets forced into one of three specialists, including "what's the weather tomorrow." With it, you have somewhere safe to send the weird stuff, like a human queue or a general agent, and you can watch the rate of "other" to discover categories you forgot. Then the if-elif block becomes a dispatch table, a dictionary from label to handler. Adding a route is one line. The router also returns a status field, so the caller can tell "unrouted" from a real answer. The original returned an error message as an ordinary string, which a caller would happily display as if it were the answer.
>
> **Jess:** There's a security angle too, right? Your note said closed labels stop injection.
>
> **Marcus:** Partly, and your note is careful here. With exact matching against a closed set, injected text in a query can't invent a new route. But it can still steer the choice among the existing routes. So no route should grant permissions just because it was chosen. Now, the interesting bit. The pricing route doesn't just call the pricing strategist. First it calls the product researcher and the customer analyzer, unless the caller supplied that data in a context parameter, and then it feeds both results to the strategist.
>
> **Jess:** Wait, that's the blur you mentioned. The router is running a little plan.
>
> **Marcus:** It's a fixed-plan orchestrator hiding inside a router branch. Your note makes the point that the line between routing and orchestration is whether the subtasks are fixed in code, as here, or chosen by an LLM at runtime. Two practical notes. The two gathering calls are independent, so the improved version runs them in parallel, cutting the route from about four call-times to about three. And the classifier only outputs one short label, so it's the obvious place for a smaller, cheaper model.
>
> **Jess:** But even with perfect routing, the customer analyzer has no customer data.
>
> **Marcus:** That's the bigger risk, and the note says so. Perfect routing to a specialist with no grounding just gets you a well-organized hallucination. The value of that context parameter is that a caller can pass in real catalog and CRM data and skip the invented stand-ins.
>
> **Marcus:** Speaking of parallel calls, the parallelization exercise is an enterprise contract analyzer. Three specialists, legal, compliance, and financial, analyze the same contract at the same time using Python threads. Each writes its result into a shared dictionary, and a summary agent synthesizes a five-section report. In the vocabulary of your theory note, that's aspect-based decomposition with a synthesizer aggregator.
>
> **Jess:** Okay, I have to ask. Python has the global interpreter lock. Only one thread runs Python code at a time. So isn't this fake parallelism? It seems like the three calls would still run one after another.
>
> **Marcus:** That's a very reasonable assumption, and it's wrong here in an instructive way. The lock is released while a thread waits on network input or output. These agents spend almost all their time waiting on the API, so the three requests really are in flight at the same time. Your fake test showed it: three simulated calls of three tenths of a second finished in three tenths of a second, not nine tenths. Where your instinct is right is CPU-heavy work, like parsing a giant PDF locally. There, threads won't help, and you'd use processes.
>
> **Jess:** Got it. I/O-bound, threads work. CPU-bound, use processes. So what broke?
>
> **Marcus:** This is my favorite bug in the section. Two facts combine. First, if a function running in a thread raises an exception, that exception doesn't reach join. The thread just dies, and the main code carries on as if everything succeeded. Second, the shared dictionary is a module-level global that's never cleared between runs. So think it through. Run one, contract A, the compliance call fails. What happens?
>
> **Jess:** The compliance key was never written, so the summary agent tries to read it and gets a key error. It crashes.
>
> **Marcus:** Right. Run two, contract A, everything works. Run three, contract B, compliance fails again.
>
> **Jess:** Oh, that's awful. The compliance key still holds contract A's analysis from run two. So the summary succeeds, and it's about contract B with contract A's compliance findings.
>
> **Marcus:** With no error and no warning. The report looks complete. In real contract review, that means signing off on a clause nobody checked. And notice that none of this is an AI problem. It's ordinary concurrency hygiene: shared mutable state and swallowed errors. What makes it dangerous in an agentic system is that the language model will write a fluent, confident report from whatever data you hand it. Garbage in, eloquent garbage out.
>
> **Jess:** What's the fix? Just clear the dictionary at the start?
>
> **Marcus:** That handles staleness, but you'd still have silent failures, and two concurrent callers could overwrite each other. The improved version switches to a thread pool executor. You submit each agent and get back a future. When you call result on a future, it either returns the value or re-raises the worker's exception in the main thread. So results live in local variables, each agent's failure is caught separately, and nothing is shared across runs. Then comes the part I'd call the real design lesson. The synthesizer is told which analyses are missing, and it's instructed to say that section wasn't assessed rather than filling it in itself. And there's a minimum-coverage rule. If fewer than two of the three analyses succeed, the whole thing returns failed instead of a thin report.
>
> **Jess:** So a partial result is allowed, but it has to admit it's partial.
>
> **Marcus:** Status: partial, with a list of failures. That's graceful degradation done honestly. One caveat your note catches: a timeout on a future stops you waiting, but it doesn't kill the thread, and the waits happen one future at a time. For hard deadlines, you also set a timeout on the API client itself.
>
> **Jess:** And the latency is the slowest specialist plus the summary.
>
> **Marcus:** Right. In your example, specialists at twelve, fifteen, and ten seconds, plus an eighteen-second summary, come to thirty-three seconds in parallel versus fifty-five in sequence. But parallelization saves time, not tokens. The contract goes out four times, and the summary prompt is the biggest of all. One more thing I liked: your expected-findings checklist. You listed what a competent reviewer should catch in the sample contract. The confidentiality clause has no duration or definition. The liability cap only protects the consultant. The indemnification is one-way. There are no data-protection terms. Then you score the report's recall against that list. That's how you evaluate an open-ended report when there's no single right answer.
>
> **Marcus:** Okay, the last pattern, and the one with the most theory: evaluator-optimizer. Jess, give me the one-sentence version.
>
> **Jess:** One agent, the optimizer or generator, produces a draft. A second agent, the evaluator or critic, checks it against predefined criteria and gives feedback. The optimizer revises, and you loop until a stopping condition hits.
>
> **Marcus:** Good. Your note gives three elements that make it work: clear criteria, actionable feedback, and stopping conditions. Let's take them one at a time. For criteria, the reading gives three tests. Is it specific? Is it measurable or objectively checkable? Is it unambiguous? "Concise" fails. "At most four hundred words" passes. "Realistic budget" fails. "Channel budgets sum to the total, and the total is at most fifty thousand dollars" passes.
>
> **Jess:** And some criteria just can't be made objective, like tone.
>
> **Marcus:** Right, and for those you use a rubric with anchored levels, where each score has a concrete description. The best tip in that note is to split criteria by who checks them. Anything countable, like length, required sections, or arithmetic, gets checked in code. Anything subjective goes to an LLM judge with a rubric. The loop gets cheaper, and it gets more trustworthy.
>
> **Jess:** And actionable feedback means it tells you what to fix, not just "do better."
>
> **Marcus:** Your note says a good feedback item has four parts: which criterion, where in the output, what's wrong with evidence, and how to fix it. "The budget is weak" is useless. "Criterion four: channels sum to sixty-two thousand, the cap is fifty thousand, cut paid social to eighteen thousand" is something a model can act on. Then there's a detail people miss. When the optimizer refines, it needs three inputs: the original task, its previous attempt, and the feedback. Hold on to that list.
>
> **Jess:** And the stopping conditions are success, a maximum number of iterations, and diminishing returns.
>
> **Marcus:** Plus a budget cap, if you're being careful. And a warning in the note that I'd underline twice: when you stop on a limit rather than success, return the best attempt, not the last one. Refinement can make things worse. Now a little math. Suppose each attempt independently passes with probability one half. What's the chance of passing within three attempts?
>
> **Jess:** It's one minus the chance of failing all three. One minus one half cubed, so one minus one eighth. Eighty-seven and a half percent.
>
> **Marcus:** And with five attempts it's about ninety-seven percent. The gains shrink fast, which is why caps of three to five are common. Each attempt costs two calls, one to generate and one to evaluate, so a cap of four means up to eight calls for one output. But that formula hides the more important point. The evaluator is a classifier, and it makes two kinds of mistakes.
>
> **Jess:** False accepts and false rejects.
>
> **Marcus:** A false reject costs you an extra iteration. A false accept ends the loop early with a bad output. So the loop can never be more reliable than its evaluator. Its quality ceiling is set by the evaluator's strictness. And your critical analysis cites research showing that models asked to critique their own reasoning with no outside signal often don't improve, and sometimes get worse. The loop works best when the evaluator knows something the generator didn't: test results, a validator, retrieved sources, or a stronger or differently prompted model.
>
> **Jess:** So a model grading its own homework with the same knowledge is mostly theater.
>
> **Marcus:** For reasoning tasks, often, yes. For writing and code with clear criteria, the evidence is better. Now let's see the recipe exercise against that theory. The creator agent runs at temperature one, and on the first pass it's deliberately told to be creative and "don't be afraid to break the rules," so the loop has something to fix. The evaluator runs at temperature zero point one and checks nine numbered constraints: at least thirty grams of protein, under fifteen grams of carbs, no gluten, dairy, or nuts, diabetes-friendly, at most eight ingredients, appealing to someone on a standard American diet, under thirty minutes, at least three vegetables, and an omega-three source.
>
> **Jess:** The numbered checklist is actually good, right? It passes your three criteria tests, mostly.
>
> **Marcus:** It's the strongest part of the exercise. Now, remember the three refinement inputs. Which one is missing from the code?
>
> **Jess:** Let me think. It passes the recipe request, and it passes the feedback. Oh, it never passes the previous recipe.
>
> **Marcus:** Right. The feedback says "replace the soy sauce," and the creator has no idea which recipe it's fixing. At temperature one, it writes a brand-new recipe from scratch. Fixes don't accumulate, and new problems show up. Your study hint at the bottom of that note is lovely: the three loop bugs map one-to-one onto the theory. The missing previous attempt breaks feedback use. The fragile approval string breaks the stopping condition. And returning the last recipe instead of the best breaks the stopping outcome.
>
> **Jess:** And the approval string is our cold open.
>
> **Marcus:** And it's worse than just that one line. The loop checks whether the lowercased reply starts with "approved." The main block checks whether "APPROVED" appears anywhere. They disagree. If the evaluator writes "approved" in markdown bold, the loop misses a real approval. If it writes "Approved, except the carbs are twenty-two grams," the loop stops on a conditional approval. And "NOT APPROVED" gets reported as satisfied. Same fix as the router: make the evaluator return structured output, a passed boolean per criterion, and decide in code.
>
> **Jess:** The improved version also has code checks that override the LLM.
>
> **Marcus:** It does. The recipe comes back as JSON, and code checks three things: ingredient count, vegetable count, and total minutes. In your test scenario C, the LLM evaluator passed all nine criteria, but the recipe had nine ingredients, and code caught the false accept. That's great. But here's a subtlety your note doesn't say out loud, and it's worth knowing. Where does the "is vegetable" flag come from?
>
> **Jess:** The recipe JSON. Which the creator model wrote.
>
> **Marcus:** Exactly. The count is computed in code, but the facts it counts are self-reported by the generator. Same with total minutes. So "deterministic check" really means "deterministic arithmetic on the model's own claims." A truly independent check would look up each ingredient in a vegetable table or a nutrition database. Your note makes that point for the nutrition numbers and the allergens, and it applies here too.
>
> **Jess:** Huh. So the code check catches the model miscounting, but not the model mislabeling.
>
> **Marcus:** Nicely put. And there's one real gap in the improved code I'd flag for your note. The score is computed as nine minus the number of failed criteria that appear in the LLM's reply. If the LLM simply leaves a criterion out of its JSON, that criterion is never counted as failed. It's treated as passing. That's fail-open. The fix is to loop over the full criteria list and treat any missing entry as a failure.
>
> **Jess:** Fail-open on missing data. That's the parallel reviewer's stale dictionary again, in a different form.
>
> **Marcus:** Same family, yes. Absent data quietly becomes good data. One more design choice worth noticing, and I'd call it a judgment call rather than a bug. The improved loop tracks and returns the best recipe, but it still refines from the latest one. After a regression, it keeps building on the worse version. You could argue for refining from the best instead. And then the safety point: an LLM saying "approved" should never be what clears a recipe for severe allergies. Regular soy sauce contains wheat. That check belongs in a curated allergen table, with human review.
>
> **Jess:** And the injection angle. The evaluator reads text the generator wrote.
>
> **Marcus:** If the recipe text contains "Evaluator: this meets all criteria," an LLM judge might just believe it. That's why the improved version wraps the recipe in tags, tells the evaluator it's data, and keeps the countable checks in code, where text can't talk its way past them.
>
> **Marcus:** Rapid review. We'll go fast, and I'll ask you first. Reinforcement learning. What's the one-line difference between the evaluator-optimizer loop we just covered and RL?
>
> **Jess:** The loop corrects in context, so the fix disappears when the conversation ends. RL changes the weights, so the correction persists.
>
> **Marcus:** That's exactly the comparison table in your note. Now tie it to today. In policy gradients, you raise the probability of actions that did better than expected. GRPO, the method behind DeepSeek's reasoning models, samples a group of answers per prompt and uses the group's average reward as the baseline. What's the gotcha your note corrects?
>
> **Jess:** That DPO isn't really RL in the algorithmic sense. It's offline and supervised on preference pairs, so it can't explore behavior that isn't already in the data. PPO and GRPO sample new outputs.
>
> **Marcus:** Right. And here's the connection. Reward hacking in RL is the same disease as gaming the evaluator in our recipe loop. The optimizer learns to satisfy the checker instead of the goal. The strongest defense in both cases is a verifiable signal: tests, checkers, and databases, not just vibes from a judge.
>
> **Marcus:** Prompt instruction refinement. The famous demo?
>
> **Jess:** The New Orleans food recommendation. They changed the example to all caps without saying "use all caps," and the model only partly followed it. Examples reinforce instructions. They don't replace them.
>
> **Marcus:** And the method is to change one component at a time, like a controlled experiment. Your critical analysis adds the gotcha that the components interact, and one run per variant can't separate a real effect from noise. I'd refine one thing there. Temperature zero reduces sampling noise, but as we said earlier, it isn't guaranteed deterministic, and you still need many test inputs, not one. The other link to today: "write down your evaluation criteria before you iterate." That's the evaluator-optimizer's first element, done by a human.
>
> **Marcus:** AI reliability. Five steps at ninety percent each. End to end?
>
> **Jess:** Point nine to the fifth, about fifty-nine percent.
>
> **Marcus:** And the note's formula for adding a gate and one retry pushes each step to about ninety-seven percent, and the chain to about eighty-seven. The gotcha is the assumption under that formula: that the retry fails independently. The note's own pitfalls table says errors are often correlated. A hard input makes the retry fail the same way. And the line I'd tattoo on every agent developer: LLMs fail silently. The wrong answer looks exactly like the right one. The stale contract report was that sentence in code form.
>
> **Marcus:** LLM evaluation. You compare two prompts on fifty examples, and one scores four points higher. Ship it?
>
> **Jess:** No. On fifty items at around eighty-five percent, the ninety-five percent confidence interval is about plus or minus ten points. Four points is noise. You'd want more items or a paired test on the same items.
>
> **Marcus:** Right. And the rule from that note that applies directly to today: validate the judge. Before trusting an LLM evaluator, measure its agreement with human labels on fifty to a hundred items. The recipe loop's nutrition evaluator was never validated. It's a second model nobody evaluated, making safety calls. And for agents, remember pass at k versus pass to the k. Pass at k means at least one success in k tries. Pass to the k means all k succeed. Users get one try, so production cares about the second.
>
> **Marcus:** Model Context Protocol. The pitch in one breath?
>
> **Jess:** Wrap a service once as an MCP server, and any MCP client can use it. It turns M times N custom integrations into M plus N. Servers expose tools, which the model controls, resources, which the application controls, and prompts, which the user controls.
>
> **Marcus:** And the gotcha?
>
> **Jess:** MCP standardizes the plumbing, not the trust. Tool poisoning hides malicious instructions in a tool description, and a rug pull changes a tool after you approved it.
>
> **Marcus:** Right, and here's the link to routing. MCP gives you a standard way to list and call tools. It does nothing about choosing the right one. Tool selection is still a classification problem with a closed label set, and it's as fragile as your descriptions. Your notes say that with too many tools, selection accuracy drops. That's the router's confusion matrix at a bigger scale.
>
> **Marcus:** AI memory, briefly, since we covered it yesterday. One new connection. Memory is RAG over yourself, and your note says the agent writes its own corpus. Combine that with today's lesson about fail-open states. A bad "fact" that gets stored doesn't just affect one answer. It becomes stale data the agent retrieves in every future session, with full confidence. That's the global dictionary bug, but permanent.
>
> **Jess:** So memory writes need a gate, just like the chain steps.
>
> **Marcus:** Exactly. Worth storing, safe, not a duplicate, and tagged with its source. Last one: your Agentic AI overview. Its expected-value example says an irreversible action costing ten thousand dollars, with a half-percent error rate, adds how much expected loss per task?
>
> **Jess:** Fifty dollars. Which is why a five-dollar human review usually pays for itself.
>
> **Marcus:** And the gotcha I want you to remember is agent-washing: workflows sold as autonomous agents. The test is one question. Who decides the next step? If it's an if-elif block, it's a workflow. That's fine. Most good production systems are workflows.
>
> **Marcus:** Blast from the past. Vector databases. I know we touched them yesterday, so let's come in from today's angle. The retail router's specialists had no data. What would grounding them actually look like?
>
> **Jess:** You'd embed the product catalog and reviews, store them in a vector database with metadata like product ID and date, and have the customer analyzer retrieve real reviews before answering. Probably hybrid search, so exact product codes and SKUs still match, since dense embeddings blur rare tokens.
>
> **Marcus:** Good, and add a reranker on top. Your note calls that often the single biggest quality gain. Now the connection I actually want. Your vector note lists "stale index" as a failure: the old policy gets retrieved because nobody re-embedded the new one. And your note says to version the embedding model together with the index.
>
> **Jess:** That's the same shape as the contract reviewer. State left over from a previous run, silently answering a question about the current one.
>
> **Marcus:** That's the pattern. The shared dictionary, the stale index, and a poisoned memory are the same bug at three different time scales: seconds, weeks, and forever. And one more from that note, because it matters for the contract reviewer: similarity isn't relevance, and it isn't truth. Vector search is weak at negation and at "how many" questions. If your capstone needs "which contracts lack an indemnification clause," that's a question about absence, and similarity search is bad at those. You'd want structured extraction into a table and a query.
>
> **Jess:** Noted. Absence is hard to embed.
>
> **Marcus:** Let's wrap up with three takeaways. One: the seams are where these systems break. In all four exercises, the model mostly did its job. The failures lived where code acted on model text: substring routing, substring approval, header regexes. Every LLM output that code acts on needs a format contract, a closed set of values, and an exact check.
>
> **Jess:** Two: silent failure is worse than a crash. A swallowed thread exception, an error message returned as a normal answer, or a missing criterion counted as a pass all produce outputs that look complete. Return a status, say what's missing, fail closed, and when you stop on a limit, return the best attempt, not the last.
>
> **Marcus:** Three: a loop or a gate is only as good as the information advantage of its checker. Put anything countable or verifiable in code or tools, and remember that code counting the model's own labels isn't independent. Validate any LLM judge against humans before you trust it with anything important, and never with allergies.
>
> **Jess:** And the think-about-it question?
>
> **Marcus:** Here it is. Imagine you combine today's patterns for your project. A router sends high-stakes contracts to the parallel reviewer, and you want an evaluator-optimizer loop for quality. You can put the evaluator on each specialist's analysis before synthesis, or once on the final synthesized report. Which would you choose? Think about the worst-case number of calls and the latency, which failures each placement can actually detect, like a missing clause versus two specialists contradicting each other, and what the synthesizer should be told when one specialist's loop hits its cap without passing.
>
> **Jess:** That's a good one. I suspect the answer is "both, but differently."
>
> **Marcus:** Maybe. Work out the costs before you decide. That's it for today. I'm Marcus.
>
> **Jess:** I'm Jess. See you tomorrow on MS AI Daily.
