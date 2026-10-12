---
title: "MS AI Daily – 2026-09-29"
type: podcast
created: 2026-09-29
duration_min: 29
covers:
  - "[[Orchestrator-Workers Workflow]]"
  - "[[Implementing Orchestrator-Workers Workflow]]"
  - "[[Agentic Workflow Patterns]]"
  - "[[Implementing Parallelization Workflow]]"
  - "[[Evaluator-Optimizer Workflow]]"
  - "[[Implementing Evaluator-Optimizer Workflow]]"
  - "[[Tool Descriptions in Agentic Systems]]"
  - "[[LLM Feedback Loops]]"
  - "[[Implementing LLM Feedback Loops]]"
  - "[[Agentic AI Skills Scorecard - Study Guide]]"
  - "[[AI Memory]]"
  - "[[Sequential Prompting]]"
  - "[[Prompt Chaining Workflow]]"
  - "[[Artificial Intelligence]]"
tags:
  - podcast
  - review
---

# MS AI Daily – 2026-09-29

![[MS AI Daily - 2026-09-29.mp3]]

> [!abstract] In this episode
> The episode opens with a lab report whose abnormal blood counts vanish from the final report. The planner called the task "CBC", the worker lookup didn't recognize the name, and the task was dropped without any error in the report. Marcus and Jess use that bug to cover orchestrator-workers: parallelization where the LLM chooses the split, the missing synthesis step, and a plan gate that turns out to be a small evaluator-optimizer loop with code as the evaluator. The review segments trace the same idea through tool selection, feedback loops, and the older chain of sequential prompting → prompt chaining → symbolic planning.

## Segments
- **Cold open:** the dropped "CBC" task ([[Implementing Orchestrator-Workers Workflow#^helper-tests]], test 8)
- **Deep dive – what the pattern is:** [[Orchestrator-Workers Workflow]], [[Agentic Workflow Patterns]]
  - What separates it from parallelization is who decides the split. The dividing-line rule ([[Orchestrator-Workers Workflow#^ow-vs-neighbours]]). The lab solution is really parallelization plus routing. "Orchestrator" means two things: the LLM planner and the runtime ([[Agentic AI Skills Scorecard - Study Guide]]).
- **Deep dive – the course scripts:** [[Implementing Orchestrator-Workers Workflow]]
  - Where the contractor analogy breaks: the planner never sees the worker registry, which is a tool-selection problem ([[Tool Descriptions in Agentic Systems]]). The "website" → site-plan substring bug. Stapling pages together is not synthesis.
  - The `parse_tasks` off-by-one: `<description>` is 13 characters. A task written on one line gives an empty plan with no error. The fix is a JSON plan with a schema.
  - Silent partial results: the dropped CBC task, empty findings, and a callback to the contract A/B stale-dictionary bug in [[Implementing Parallelization Workflow#^thread-failure-test]]. Fallback worker vs. reporting the gap. Run statuses.
- **Deep dive – hardening it:** [[Implementing Orchestrator-Workers Workflow#^plan-gate-extension]], [[Evaluator-Optimizer Workflow]], [[Implementing Evaluator-Optimizer Workflow]]
  - Parallel workers with `ThreadPoolExecutor`: 44 s → 29 s, with a synthesis step included.
  - The plan gate with one retry *is* an evaluator-optimizer loop (criteria, actionable feedback, stopping condition), but validity is not quality. Computed lab flags work as an evaluator that knows something the generator doesn't ([[Implementing Orchestrator-Workers Workflow#^lab-flags]]).
  - Dependency waves: [A, B] → [C] → [D]; B fails → partial. **Classroom vs. production:** the wave latency (sum of each wave's maximum) can exceed the DAG critical path because of the barrier between waves.
  - Reliability: 0.9 × 0.95⁵ × 0.95 ≈ 0.66. Capping *k* is a reliability control. Security: a closed registry, least privilege, and human approval.
- **Rapid review:** [[Tool Descriptions in Agentic Systems]], [[LLM Feedback Loops]], [[Implementing LLM Feedback Loops]], [[Agentic AI Skills Scorecard - Study Guide]], [[AI Memory]]
  - The five things a tool description states. 40 tools × 250 tokens. Error messages are prompts.
  - The five parts of a loop and the ranking of feedback sources. **Correction to the note:** in the illustrative `sort_numbers` trace ([[LLM Feedback Loops#^code-refinement-trace]]), iteration 2 calls `nums.sort()` on `'abc'`, which raises `AttributeError`; it doesn't return `['a','b','c']`. The test still fails, but the feedback text is wrong. `['a','b','c']` belongs to iteration 3 (`sorted`). Also covers the control-theory lens.
  - Stale kernel state, the same "hidden state" family as the global dict. Tests are the spec. `(x,)`. An empty namespace is not a sandbox.
  - "The LLM is only the policy." CoT vs. ReAct quick calls.
  - Semantic, episodic, and procedural memory. Persistent injection. The orchestrator's shared memory is whatever the runtime passes along.
- **Blast from the past:** [[Sequential Prompting]], [[Prompt Chaining Workflow]], [[Artificial Intelligence]]
  - Who connects the steps (human → code → LLM) and who checks them (you → gates → plan gate).
  - The gated-reliability numbers from [[Prompt Chaining Workflow#^gated-reliability]] (0.59 → 0.89). Contextual reiteration is why workers get the original task.
  - Old ideas under the new pattern: HTN planning and blackboard systems. **Refinement to the note:** "LLMs are deep learning with RL-based fine-tuning" is true of many models, not by definition. SFT-only and DPO-tuned models exist.

## Think about it
Your lab-report orchestrator receives a panel that no specialist covers, say a thyroid panel. You can send it to a generic fallback worker, report it as "not assessed", or let the orchestrator re-plan and request a new kind of worker. Which would you choose for clinical decision support, and would your answer change for the permit assistant? What would your run statuses, logs, and evaluation set need to record so that, a month into production, you could tell whether that choice was causing harm?

> [!quote]- Transcript
> **Marcus:** Jess, here's a puzzle. A patient's lab report comes in. The white blood cell count is high and the platelets are low. An orchestrator reads it, plans three subtasks, and three specialist workers run. The final report covers kidney function and liver function in careful detail. It says nothing at all about blood counts. No crash, no error in the report. Which component failed?
>
> **Jess:** My first instinct is the hematology worker. It must have returned something empty.
>
> **Marcus:** Reasonable guess, and wrong. The hematology worker never ran. The planner labeled the task "C B C", which is the common name for that panel. The code that picks a worker only recognized the word "hematology". It raised an error, caught its own error, printed one line to the console, and dropped the task. Every model call did its job. The failure lived in about four lines of plain Python.
>
> **Jess:** So the most important finding in the report quietly disappeared.
>
> **Marcus:** Exactly. Welcome to MS AI Daily. It's Tuesday, September twenty-ninth, twenty twenty-six. I'm Marcus.
>
> **Jess:** And I'm Jess. Today we finish the workflow-patterns section with pattern five, orchestrator-workers.
>
> **Marcus:** Here's the plan. The deep dive covers orchestrator-workers, theory and code together: what makes it different from parallelization, why the course scripts don't really synthesize anything, and how a plan gate, run statuses, and dependency waves harden it. Then a rapid review of tool descriptions, feedback loops, the skills scorecard, and agent memory. Then we go back to sequential prompting, prompt chaining, and some very old A I ideas that turn out to be this same pattern.
>
> **Jess:** Let's start with the definition. Put it in one sentence for me.
>
> **Marcus:** A central model breaks a task into subtasks at runtime, hands each subtask to a worker, and then combines the results. Before I go on, you've got parallelization fresh in your head. What's the difference?
>
> **Jess:** Is it basically parallelization with a smarter splitter? In parallelization you split the work and fan it out. Here the model does the splitting.
>
> **Marcus:** That's the right answer, and your notes say almost exactly that. In parallelization, code fixes the subtasks before any input arrives. Legal, compliance, financial, every contract, every time. In orchestrator-workers, the model decides how many subtasks there are, what they are, and which worker gets each one. The question is who decides the split.
>
> **Jess:** That sounds like a small change.
>
> **Marcus:** It changes a lot. When code decides the split, you can unit-test the split. When a model decides it, the plan is model output. It varies from run to run, it can leave things out, and nothing downstream can do better than the plan allows. Your theory note calls the planner a single point of failure. Every worker can be perfect and the answer still fails if the plan missed a subtask.
>
> **Jess:** So when is it worth it?
>
> **Marcus:** The note gives a clean dividing line. If you could write the list of subtasks in code before seeing the input, use parallelization or chaining. Use orchestrator-workers only when the subtasks depend on the input in ways you can't list ahead of time.
>
> **Jess:** Let me test that against the two course scripts. The demo plans building permits for a pool in The Woodlands, Texas. The exercise plans a lab-report interpretation.
>
> **Marcus:** Good. Apply your own rule.
>
> **Jess:** The permit one feels dynamic. A pool needs different permits than a kitchen remodel, and I can't list every project type ahead of time. The lab one is one task per panel. If the panels are hematology, renal, and liver, I could find them with a regular expression.
>
> **Marcus:** That's the critique your implementation note makes. The lab solution is really parallelization with routing, dressed up as an orchestrator. It's a fine exercise for learning the pattern, but the pattern only pays for itself when the subtasks can't be predicted. The retail router's pricing route from a few days ago is the same situation in reverse. It calls two other agents on a fixed plan, so it's routing with context gathering, not orchestration.
>
> **Jess:** One vocabulary thing is bugging me. In the skills scorecard, "orchestrator" meant the runtime code that executes tools and enforces budgets. Now it's a model that plans.
>
> **Marcus:** Yes, the word is overloaded, and your theory note flags it. A real system has both. The model orchestrator proposes a plan. The runtime orchestrator decides whether to run it. Keep that split in mind, because the plan gate we'll get to is the runtime vetoing the model.
>
> **Jess:** The course explains the code with a general contractor analogy. The orchestrator class is the contractor, the task list is the project plan, the worker lookup function is the contact list, the specialist agents are subcontractors, and the generic agent is the handyman.
>
> **Marcus:** It's a good analogy, and it's useful to see where it breaks. A real general contractor knows who's in their contact list. What does the planning prompt tell the model about the available workers?
>
> **Jess:** Hmm. It shows one example task with the type "zoning". I don't think it lists the others.
>
> **Marcus:** It doesn't. The planner is inventing type names and hoping the code recognizes them. That's how you get "C B C" when the code expects "hematology". Imagine a contractor who writes "call the pipe person" on the schedule and an office manager who only has "plumber" in the phone.
>
> **Jess:** This sounds like the tool-descriptions note. The planner is choosing among workers the same way an agent chooses among tools.
>
> **Marcus:** It's the same problem. Picking a worker is tool selection. The fix follows the tool-design principles. Put the worker registry in the planning prompt, give each worker a clear description, and make the type field a closed set. Better still, constrain it in the schema as an enum instead of in prose. The schema gets enforced. Prose is only a suggestion.
>
> **Jess:** And the demo's worker lookup is substring matching, right? If the type contains "zoning", send it to zoning. If it contains "site", send it to site plan.
>
> **Marcus:** Yes. So a task called "website update" goes to the site plan agent, because "website" contains "site". That lookup code is putting in less effort than the model it's trusting.
>
> **Jess:** So the fix is exact matching after normalization. Lowercase it, strip the spaces, look it up in a dictionary, and if it's not there, use the fallback.
>
> **Marcus:** Right. Now the analogy's second break. A general contractor doesn't just staple the subcontractors' reports together and hand you the stack. What do the course scripts do at the end?
>
> **Jess:** They print the analysis, then each worker's result under a heading.
>
> **Marcus:** That's stapling. The theory says synthesis is more than stapling pages together. It connects findings, reconciles contradictions, and says what's missing. Neither script has a synthesis step. Your note puts it bluntly: the orchestrator does half its job.
>
> **Jess:** Okay, before we fix things, there's a bug in the parser I want to understand properly. My note says every description comes out with a stray angle bracket on each end.
>
> **Marcus:** This one is a good lesson. The planner returns tasks in XML-style tags, and the parser reads line by line. When a line starts with the description tag, it slices the text from character twelve up to thirteen characters from the end. Count the characters in the opening tag: angle bracket, the eleven letters of "description", closing angle bracket.
>
> **Jess:** Thirteen. So starting at twelve grabs the closing angle bracket of the tag.
>
> **Marcus:** And the closing tag has fourteen characters, not thirteen, so the end is off by one as well. Every description gets a stray bracket at each end, even in the exact format the prompt asks for. It gets worse. If the model puts a whole task on one line, which is perfectly valid XML, the parser finds zero tasks. The report contains only the analysis. Nothing errors.
>
> **Jess:** I'll push back a bit. Models are pretty good at copying a format example. Isn't a line parser fine most of the time?
>
> **Marcus:** Most of the time, yes. But "most of the time" gets multiplied by every run in production, and when this parser fails it fails silently. The fix isn't a better slice. Stop hand-parsing XML line by line. Ask for JSON, parse it with the standard JSON loader, and validate it against a schema. Then a format problem becomes a loud error you can retry, not a quietly shorter plan.
>
> **Jess:** Now the cold open. The lab solution's lookup raises an error for unknown types, catches it, and drops the task.
>
> **Marcus:** Yes. And there's a second silent path. If a worker's reply is missing its response tags, the solution returns an empty string. That's blank findings, no warning. The demo at least falls back to the raw reply.
>
> **Jess:** This is the same family as the parallelization bug. A thread died, the shared dictionary still held the previous contract's compliance analysis, and the report for contract B quietly used contract A's findings.
>
> **Marcus:** Same family. I'd call it the silent partial result, and it's the worst failure in these systems. A crash gets fixed on Monday. A fluent report that's missing a section, or has a section about the wrong document, gets signed. The model will write a confident synthesis from whatever you hand it.
>
> **Jess:** So what's the fix? A generic fallback worker for anything unmatched?
>
> **Marcus:** That's one option, and the demo's handyman is good design for permits. But think about the lab case. What does the generic fallback hide?
>
> **Jess:** That no specialist looked at it. The report would read as if the hematology panel had been reviewed.
>
> **Marcus:** Right. So the improved version supports either choice, but never silence. If there's no worker and no fallback, the task becomes an explicit problem entry. The problems list goes to the synthesizer, which is told to state which parts couldn't be covered. Then the extension adds run statuses: ok, partial, plan failed, and all workers failed. A caller can tell a full answer from a partial one without reading the prose.
>
> **Jess:** Walk me through the rest of the improved version.
>
> **Marcus:** One configurable worker class instead of near-identical subclasses. A worker is a type, a role, and a focus, so the team is just a list of configurations. The registry is shown to the planner, and the plan must use only those types. The plan is JSON, capped at a maximum number of tasks. And the workers run in parallel with a thread pool executor, which is the same fix you learned for parallelization.
>
> **Jess:** Because calling result on a future either returns the value or re-raises the worker's exception in the main thread. With a raw thread, the exception just vanishes.
>
> **Marcus:** Exactly. And to head off the usual objection, threads really do help here despite Python's global interpreter lock. The lock is released while a thread waits on network input and output, and these workers spend nearly all their time waiting on the A P I.
>
> **Jess:** And the fake-model test showed that?
>
> **Marcus:** Three workers with simulated delays finished in the time of one. An odd type name with a capital letter and a trailing space was normalized correctly. And a task type with no specialist showed up as a visible problem for the synthesizer instead of disappearing. Let's do the latency math. Planning takes six seconds. Four workers take nine, twelve, seven, and ten. Synthesis takes eleven. Compare the original with the improved version.
>
> **Jess:** The original runs the workers one after another with no synthesis, so six plus nine plus twelve plus seven plus ten. That's forty-four seconds. The improved version is six, plus the slowest worker at twelve, plus eleven for synthesis. Twenty-nine seconds.
>
> **Marcus:** So it's faster and it produces an actual synthesized report. The extra synthesis call more than pays for itself once the workers run in parallel. That's rare. Usually you pay for quality.
>
> **Jess:** Now the extension I found most interesting, the plan gate. It's pure code that accepts or rejects the plan before any worker runs.
>
> **Marcus:** What does it check? Go from memory.
>
> **Jess:** Valid JSON. A task list that isn't empty and isn't over the cap. Unique IDs. Every type in the allowed set. No empty descriptions. Dependencies that point at real IDs. And no cycles.
>
> **Marcus:** That's all of it. If the plan fails, the gate re-prompts once with the specific error, something like "subtask three uses unknown type catering, allowed types are venues, travel, budget." After two failures, the status is plan failed, and no worker or synthesis call is made.
>
> **Jess:** Wait. That's an evaluator-optimizer loop. The planner is the optimizer, the gate is the evaluator, the error message is the feedback, and two attempts is the stopping condition.
>
> **Marcus:** Yes, and that's the connection I most want you to see today. It's the smallest evaluator-optimizer loop, and it has the strongest evaluator there is: code. The three elements from the evaluator-optimizer note are all there. The criteria are specific and checkable. The feedback is actionable. The stopping condition is explicit. In the test, the first plan came back as chatty prose around the JSON, something like "Sure! Here's the plan." The gate rejected it, the retry was clean, and the run finished with status ok.
>
> **Jess:** But here's my worry. The gate checks whether the plan is valid. If the planner forgot the renal panel completely, the gate passes that plan, right?
>
> **Marcus:** It does, and that's the right worry. Validity isn't quality. Your note says it directly: a fake model can check the control flow, but not whether the planner chose sensible, complete, non-overlapping subtasks. The evaluator-optimizer note says the loop can't be more reliable than its evaluator. A gate that only checks format has a detection rate of about zero for missing coverage.
>
> **Jess:** So what catches missing coverage?
>
> **Marcus:** An evaluator that knows something the generator doesn't. The lab exercise has a lovely example. Whether a value is outside its reference range is arithmetic, not interpretation. Your note computes the flags in code. White cells, eleven point five against a normal range up to eleven, high. Platelets, a hundred and forty against a floor of a hundred and fifty, low. Creatinine and B U N, both high. A S T at sixty against an upper limit of forty, high. And A L T at fifty-five, with an upper limit of fifty-six.
>
> **Jess:** Normal, but only just.
>
> **Marcus:** Normal, and that's a trap. So the flag table becomes an automatic checklist. A correct report mentions all five abnormal values and does not call A L T abnormal. That's a precise test of the whole orchestrator and its workers, and it doesn't need a model to judge a model. The same idea tells you to pass those flags to the workers, so the model explains why a value matters but never does the comparison itself.
>
> **Jess:** Okay, dependency waves. The basic version runs every subtask blind. But some subtasks need each other. You can't do the budget until you have the venue and the travel costs.
>
> **Marcus:** So each subtask can list the IDs it depends on, and the plan becomes a directed acyclic graph. The waves function groups subtasks. Wave one is everything with no dependencies. Wave two is everything whose dependencies are all in wave one, and so on. If at some point nothing is ready, there's a cycle. Try one. A and B have no dependencies. C depends on A. D depends on B and C. What are the waves, and what happens if B fails?
>
> **Jess:** Waves are A and B together, then C, then D. If B fails, C still runs, because it only needs A. D gets skipped, because one of its dependencies failed. The run ends as partial, and the synthesizer is told that B failed and D was skipped.
>
> **Marcus:** Perfect. Now a point about the classroom model versus production. Your implementation note gives the latency with waves as the sum, over the waves, of each wave's slowest subtask. The theory note says the latency is the critical path of the graph. Those aren't the same thing.
>
> **Jess:** Why not? They sound equivalent.
>
> **Marcus:** Waves put a barrier between each round. Say A takes one second, B takes ten, and C depends on A and takes ten. The critical path is A then C, eleven seconds. But with waves, C can't start until the whole first wave finishes, and that includes the slow B. So you get ten plus ten, twenty seconds. A production scheduler starts each task as soon as its own dependencies finish, so it achieves the critical path. The wave version is simpler and easier to reason about, which makes it a good teaching design. Just know which one your code actually does.
>
> **Jess:** That's a good distinction. Let's do the reliability math. The theory note multiplies the probabilities.
>
> **Marcus:** If the answer needs all k subtasks, success is roughly the plan's reliability, times the per-worker reliability to the power k, times the synthesizer's reliability. With a plan at zero point nine, workers at zero point nine five, five subtasks, and synthesis at zero point nine five, you get about zero point six six.
>
> **Jess:** That's lower than I'd expect. My instinct is that more workers make the answer more thorough.
>
> **Marcus:** That's a very common assumption, and the math says otherwise. With three subtasks it's about zero point seven three. With six it's about zero point six three. Every extra subtask is another chance to fail, and here the model chooses k. So the note's most important line might be this: capping k is a reliability control, not only a cost control. If the synthesizer can tolerate partial failure, say four of five subtasks is enough, the probability becomes a binomial tail, which is much higher. That's what the partial status is for.
>
> **Jess:** And that zero point six six matches the scorecard's capstone, eight stages at zero point nine five each.
>
> **Marcus:** Yes, same number, same lesson. Compounding doesn't care whether the steps are in a chain or spread across workers. Last point in the deep dive: security. The planner turns untrusted input into actions. If the lab data comes from another system, or the permit request comes from a user, injected text can try to create a subtask like "email this data to someone."
>
> **Jess:** And the closed registry limits the damage. The planner can only choose workers that exist.
>
> **Marcus:** The closed registry limits who can act. Least-privilege tools limit what each worker can do. Human approval covers anything with side effects. You need all three. One of them alone isn't enough.
>
> **Jess:** Rapid review. Let's start with tool descriptions, since it already showed up today.
>
> **Marcus:** You tell me. What five things should a strong tool description state?
>
> **Jess:** Purpose. When to use it. When not to use it, and which tool to use instead. What it returns, including shape, units, and limits. And side effects, meaning whether it writes, sends, deletes, or costs money, and whether that's reversible.
>
> **Marcus:** All five. Now the cost. Forty tools at about two hundred fifty tokens each, in a twelve-step ReAct run.
>
> **Jess:** Ten thousand tokens of definitions on every call, so about a hundred and twenty thousand input tokens before any task content. Caching lowers the bill, but the definitions still take up context.
>
> **Marcus:** And selection accuracy tends to drop as you add similar tools. Here's the gotcha to remember. A description can tell the model a tool is destructive. Only the runtime can require confirmation. And your error messages are prompts. "Device ID not found, call search devices first" gets the agent unstuck. "Error five hundred" gets you the same bad call again.
>
> **Jess:** Next, feedback loops. Five parts: generator, evaluator, feedback formatter, stop condition, and memory, meaning what carries over between iterations.
>
> **Marcus:** And the ranking of feedback sources?
>
> **Jess:** External tools and validation checks at the top, because they're objective. User input is strongest on intent, but slow. Self-correction is the weakest on its own, because the critic has the same blind spots as the generator.
>
> **Marcus:** Good. Now a correction to the note itself. The illustrative code-refinement trace has an iteration where the function sorts the list in place and returns it. The note says that when this is called with the string "a b c", the feedback is "expected a type error, got the list a, b, c."
>
> **Jess:** That sounds plausible.
>
> **Marcus:** It isn't what happens. Strings don't have an in-place sort method. Calling it on a string raises an attribute error. It doesn't return a list. The test still fails, because it expected a type error, so the pass-fail pattern in the table holds. But the feedback text is wrong. The "got the list a, b, c" behavior belongs to the next iteration, where the code calls the built-in sorted function, which happily turns a string into a list of characters.
>
> **Jess:** It's a small slip, but it matters, because the feedback text is the next prompt.
>
> **Marcus:** Exactly. A formatter that misreports the actual error sends the model after the wrong fix. It's worth correcting in the note. One more idea from that note: the control-theory lens. A basic loop acts like a proportional controller. It reacts only to the current error. That's why it can overshoot and oscillate. Carrying a list of already-fixed issues works like an integral term. It gives the loop some memory of past errors.
>
> **Jess:** Then the lab, implementing feedback loops. My takeaway was that the model went from eight of twelve tests to twelve of twelve in one revision.
>
> **Marcus:** What's the debrief lesson, though?
>
> **Jess:** The loop cell never actually called the model. The lines that did the work were commented out, and the loop printed success because the variables were still sitting in the notebook kernel from earlier cells.
>
> **Marcus:** Hidden state made a broken loop look like it worked. That's the same family as the global dictionary in parallelization, and the silent drop in today's orchestrator. Restart and run all before you trust a result, and put loops inside functions so they can only see their arguments. Two quick gotchas. Parentheses around a single list don't make a tuple. You need the trailing comma. And running generated code with an empty namespace dictionary is not a sandbox. Python injects the built-ins automatically, so the code can still import the O S module.
>
> **Jess:** And the bigger idea: the tests are the specification. The task description never mentioned median mode or raising a value error. The model learned those requirements only from failing-test feedback.
>
> **Marcus:** Which means the loop is only as good as the tests. Twelve tests leave most of the behavior unspecified. Now the skills scorecard. Give me its best interview line.
>
> **Jess:** "The model is only the policy. The orchestrator decides what the model is allowed to do. It executes the tools, holds the memory, and enforces the stop conditions."
>
> **Marcus:** And today's plan gate is that sentence in code. Quick decision. Someone asks whether edge router two is dropping packets right now. Chain-of-thought or ReAct?
>
> **Jess:** ReAct. It needs live data the model doesn't have. If they'd asked what seventeen percent of a two point four million dollar budget is, and whether it's over four hundred thousand, that's chain-of-thought. It's four hundred eight thousand, so yes.
>
> **Marcus:** The scorecard sums it up: chain-of-thought can't fix missing information, and ReAct can't fix bad reasoning. Last in this segment, agent memory. Classify these three. "The user's timezone is Central European Time." "On September third, the deploy failed." "Always run tests before committing."
>
> **Jess:** Semantic, episodic, procedural.
>
> **Marcus:** Right. The gotcha is that memory turns a one-time injection into a persistent one. If a malicious "preference" gets stored, it affects every future session, so writes need a gate. And there's a connection to today. Workers don't share memory. The only shared memory in an orchestrator is what the runtime chooses to pass along, like dependency outputs going into a worker's prompt or findings going to the synthesizer. That's a context budget decision, the same one the memory note asks you to make.
>
> **Jess:** Blast from the past. Let's go back to sequential prompting.
>
> **Marcus:** I'll ask it as a question, because it ties the whole section together. Sequential prompting, prompt chaining, orchestrator-workers. In each one, who connects the steps?
>
> **Jess:** In sequential prompting, a human does, usually by hand in a chat. In prompt chaining, code does, in a fixed order. In orchestrator-workers, a model decides the steps and code runs them.
>
> **Marcus:** And who checks each step?
>
> **Jess:** In sequential prompting, I do. I'm the manual gate. In chaining, code gates between steps. In orchestrator-workers, the plan gate, plus whatever evaluates the workers' results.
>
> **Marcus:** That's the progression. It's the same decomposition idea, with less of it in human hands at each stage, and each stage needs more automated checking to make up for that. Your sequential prompting note also warns that the research step is the riskiest, because without sources it's the model recalling from memory, and every later step builds on it. That's the planner problem in miniature. The first step caps everything after it.
>
> **Jess:** From the prompt chaining note I remember the gated reliability formula. Each step succeeds with probability p. The gate catches a bad output with detection rate d, and you get k attempts.
>
> **Marcus:** Give me the numbers from the note.
>
> **Jess:** With p at zero point nine, detection at zero point eight, and three attempts, each step ends correct about ninety-eight percent of the time. A five-step chain goes from about zero point five nine with no gates to about zero point eight nine.
>
> **Marcus:** And the lesson under it?
>
> **Jess:** Gates help only as much as they detect. And when retries run out, the step fails visibly instead of passing a wrong answer downstream.
>
> **Marcus:** Which is today's lesson again, from three days earlier. One more callback from that note. Contextual reiteration, restating the goal in every prompt, is exactly why each orchestrator worker gets the original task along with its own subtask. Without it, workers write generic memos that don't fit the big picture.
>
> **Jess:** And the Artificial Intelligence note, the foundations one?
>
> **Marcus:** Its core claim is that agentic A I puts old ideas on top of new learned models, and today's pattern shows it well. Breaking a task into subtasks and assigning them is decades old. Classic symbolic planning had hierarchical task networks, which decompose a goal into subtasks until each one can be done directly. There were also blackboard systems, where a controller coordinated specialist knowledge sources around shared data. The new part is that a language model does the decomposing, which gives you flexibility and also the variance we talked about.
>
> **Jess:** Anything in that note to fix?
>
> **Marcus:** One overbroad line. The key takeaways say large language models are deep learning, meaning Transformers, with R L based fine-tuning. Reinforcement learning from human feedback is common, but it isn't part of the definition. Plenty of models are fine-tuned with supervised instruction data, and preference methods like direct preference optimization skip the reinforcement learning loop. So say "commonly", not "by definition". And one line from that note is worth keeping: symbolic A I isn't obsolete. Rules and search are still the reliable backbone. Every plan gate we wrote today is a little rule system checking a neural network's output.
>
> **Jess:** I like that. The old A I is standing guard over the new A I.
>
> **Marcus:** Let's wrap up with three takeaways. First: orchestrator-workers is parallelization where the model chooses the split. Use it only when you can't list the subtasks in advance, because the plan becomes output. It varies between runs, it's a single point of failure, and it needs a code gate for validity and separate evaluations for quality.
>
> **Jess:** Second: wherever code acts on model text, meaning plan formats, worker names, response tags, or approval strings, use structured output and a closed vocabulary checked in code, and fail loudly. The worst failure in these systems isn't a crash. It's a fluent report with a missing section.
>
> **Marcus:** Third: gates, evaluators, and loops only help as much as they detect, and the best ones know something the generator doesn't, like computed lab flags or real tests. Capping fan-out is a reliability decision, not only a budget decision.
>
> **Jess:** And the think-about-it question?
>
> **Marcus:** Here it is. Your lab-report orchestrator receives a panel that no specialist covers, say a thyroid panel. You can send it to a generic fallback worker, report it as not assessed, or let the orchestrator re-plan and request a new kind of worker. Which would you choose for clinical decision support, and would your answer change for the permit assistant? Then the harder part: what would your run statuses, logs, and evaluation set need to record so that, a month into production, you could tell whether that choice was causing harm?
>
> **Jess:** I'll be thinking about that one on the drive in.
>
> **Marcus:** Good. That's MS AI Daily. Keep your registries closed and your failures loud. See you tomorrow.

