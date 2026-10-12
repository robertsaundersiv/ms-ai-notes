---
title: "MS AI Daily – 2026-09-23"
type: podcast
created: 2026-09-23
duration_min: 16
covers:
  - "[[Prompt Instruction Refinement]]"
  - "[[Chain-of-Thought and ReACT Prompting]]"
  - "[[Chain-of-Thought and ReAct]]"
  - "[[ReAct prompt Samples]]"
  - "[[Prompt Chaining for Agentic Reasoning - Study Guide]]"
tags:
  - podcast
  - review
---

# MS AI Daily – 2026-09-23

![[MS AI Daily - 2026-09-23.mp3]]

> [!abstract] In this episode
> Marcus and Jess cover the whole path from a single prompt to an agent. They start with the five components of a prompt and refining one variable at a time. Next come chain-of-thought (including the Demand-Spike Detective lab and unfaithful reasoning) and ReAct loops with THINK/ACT tool prompts. The episode ends with prompt chaining patterns, error compounding (p to the n), and a lightning-round quiz.

## Segments
- **Deep dive:** [[Prompt Instruction Refinement]], [[Chain-of-Thought and ReACT Prompting]], [[Chain-of-Thought and ReAct]], [[ReAct prompt Samples]], [[Prompt Chaining for Agentic Reasoning - Study Guide]]
- **Lightning round:** self-test questions from [[Prompt Chaining for Agentic Reasoning - Study Guide]] and [[Prompt Instruction Refinement]]
- **Rapid review / Blast from the past:** skipped (the vault has no notes older than 2 days yet)

## Think about it
Go back to the Demand-Spike Detective. If you rebuilt it as a ReAct agent, what three tools would you give it, and what gate would you put in place so it doesn't report a confident but unsupported cause, like the competitor price drop?

> [!quote]- Transcript
> **Marcus:** Here's a question to start your morning. You build a five-step AI pipeline, and every step works ninety-five percent of the time. How reliable is the whole thing?
>
> **Jess:** Ninety-five percent? Maybe a little lower?
>
> **Marcus:** About seventy-seven percent. Almost one run in four goes wrong. Today we'll look at why that happens and what you can do about it.
>
> **Jess:** Okay, that's a little scary. Welcome to MS AI Daily. It's Wednesday, September twenty-third, twenty twenty-six. I'm Jess.
>
> **Marcus:** And I'm Marcus. Good to have you here.
>
> **Jess:** So, Marcus, what's on the agenda?
>
> **Marcus:** Everything today comes from notes you wrote in the last two days, and they fit together really well. First, prompt instruction refinement: the five parts of a prompt and how to improve them. Then chain-of-thought, including your hands-on sales-spike lab. Then ReAct, the reason-and-act loop, with the sample agent prompts you saved. And to finish, prompt chaining, which ties all of it together. We'll close with a quick lightning round.
>
> **Jess:** Let's start with the basics, then. Prompt refinement.
>
> **Marcus:** Your notes split a prompt into five components: role, task, output format, examples, and context. Role sets the persona and tone. Task is what the model actually has to do. Output format is the shape of the response, like JSON or markdown. Examples are one-shot or few-shot demonstrations. Context is the background facts and data, and in an agentic system it's also the description of the agent's environment.
>
> **Jess:** And the refinement part is basically "change something and see what happens"?
>
> **Marcus:** Change one thing at a time, then figure out why the output changed. The course calls it the scientific method applied to prompting. The New Orleans food demo shows it well. The baseline is a cheerful food blogger recommending a unique local dish in under seventy-five words, with no restaurant names. It recommends yakamein and meets every constraint. Then they swap only the role, to a high-end food critic, and the tone shifts. They tighten the task to fifteen words and the response gets tighter. They switch the format to JSON and get output ready to parse.
>
> **Jess:** I remember the all-caps one, where it didn't really work.
>
> **Marcus:** That's the most important demo in the set. They rewrote the example in all caps and gave no instruction about capitalization. The model only partly copied it: the start came out capitalized, the rest didn't. And the instructor points out the model wasn't failing. It was never told to use caps.
>
> **Jess:** So examples aren't instructions.
>
> **Marcus:** Right. Examples back up instructions, they don't replace them. If a requirement matters, write it down. Your notes add something worth underlining: the components aren't independent. The task, the examples, and the format section can all affect formatting, and when they conflict, the result is unpredictable.
>
> **Jess:** Which is kind of a problem for "change one variable at a time," isn't it? If the variables interact?
>
> **Marcus:** Good catch. Your critical-analysis section makes the same point. There's a second problem too: these models are stochastic. One run per variant can't tell a real effect from sampling noise. On the job, you run several samples per variant against an eval set with a written rubric, and you compare the distributions. It's closer to an A B test than to eyeballing two outputs.
>
> **Jess:** And the pirate ship? Why did that one matter?
>
> **Marcus:** The pirate agent was asked how old the ship was and gave an evasive answer, because the age was never in its context. That's actually the good outcome, since it didn't invent an age. The lesson is to fix the context instead of hoping. It lines up with the pitfalls list: ambiguity is the most common pitfall, missing context leads to hallucination, and too much or conflicting context dilutes the prompt. And one more for agent builders: tool descriptions are prompt engineering.
>
> **Jess:** Put a pin in that, because I think it comes back.
>
> **Marcus:** It does, in the ReAct section. But first, chain-of-thought.
>
> **Jess:** Okay, chain-of-thought. The "think step by step" trick.
>
> **Marcus:** That's zero-shot chain-of-thought. The idea is that the model writes out intermediate reasoning before it answers, so it goes from question to decomposition to reasoning to answer instead of jumping straight to a conclusion. Your notes cover three variants. Zero-shot is just the instruction. Few-shot shows worked examples of the reasoning pattern. Self-consistency samples several reasoning paths at a nonzero temperature and takes a majority vote on the final answers. Tree-of-thought is the extension: it explores branches, evaluates them, and backtracks, which makes it more like search.
>
> **Jess:** Let's talk about the lab. The Demand-Spike Detective.
>
> **Marcus:** Great exercise. You had synthetic sales data, a promotions calendar, weather, and competitor pricing, and the goal was to explain an unexpected sales spike. In your reflection, product five spikes on January twelfth. There was a Weekend Special promotion that started that day, but it was for product two. There was heavy rain that day. And one competitor dropped its price on product five that same day.
>
> **Jess:** Wait. If a competitor cut their price, wouldn't our sales go down?
>
> **Marcus:** That's exactly the kind of thing you want the model to reason about. Your own reflection offered a plausible reading: the competitor's move might have come with a broader ad campaign that raised interest in the whole product category. Maybe. The point is that it's a hypothesis. The data can't confirm it. Hold onto that thought.
>
> **Jess:** And the lab compared prompts with and without "think step by step."
>
> **Marcus:** Yes, on a small model, GPT four point one nano. The lab also has a note I'd highlight: many modern models reason step by step without being told, because it's built into their training. Your concept note makes the same distinction between prompted chain-of-thought and reasoning models trained with reinforcement learning to produce long internal traces. With those models, an explicit chain-of-thought instruction may be redundant. So test it both ways, and run each version more than once.
>
> **Jess:** Then part two made the prompt much more structured.
>
> **Marcus:** Right, and look at what it used. An instructions section with specific steps: find every spike, give its date, amount, and percentage increase, and check causes against each data source. A strict output format: a structured analysis, then a largest-spike JSON block with the date, before and after amounts, percentage, and a list of causes. And a context section with the data. That's role, task, format, and context straight from the refinement lesson. And there's code downstream that splits on the JSON fence and parses it, and it raises an error if the block is missing.
>
> **Jess:** So the output format matters because a program is reading it, not a person.
>
> **Marcus:** Exactly. Now for the big limitation, which your notes cover well: reasoning isn't the same as being right. The model can hallucinate, reason from bad data, or overthink. And there's unfaithful reasoning, from Turpin and colleagues, twenty twenty-three. The reasoning the model shows may be a rationalization after the fact, not a real trace of how it got the answer.
>
> **Jess:** So basically, I shouldn't treat the chain-of-thought as an audit log.
>
> **Marcus:** Treat it as evidence, not proof. Your notes also have a line I love: better reasoning cannot compensate for bad information. In the sales lab, chain-of-thought can list reasons for the spike, but it can't look anything up to check them. That's where ReAct comes in.
>
> **Jess:** Quick pronunciation note first. It's ReAct with only the A capitalized, right? Not all caps?
>
> **Marcus:** Your notes flag it too. It's R, e, capital A, c, t, short for reasoning and acting, from Yao and colleagues in twenty twenty-two. It isn't an acronym, even though the lab title spells it in all caps. The loop goes: think, act by calling a tool, observe the result, then think again, until the model can answer. The key difference from chain-of-thought is that each observation can change what the model does next. Chain-of-thought's path is fixed once generation starts. ReAct gathers new information as it goes.
>
> **Jess:** Give me the real-world version.
>
> **Marcus:** Your network-operations example is a good one. Customers on Tower A report packet loss. A chain-of-thought system can list likely causes: backhaul congestion, RF interference, a sector failure, router CPU. And that's as far as it can go. A ReAct agent queries Zabbix and finds the tower is reachable. It checks sector interfaces and sees sector three at ninety-eight percent utilization. It pulls the history and sees normal is about fifty-five percent. Conclusion: abnormal congestion on sector three. Your notes put it as reasoning about the system versus interacting with the system while reasoning.
>
> **Jess:** How is that different from RAG, retrieval-augmented generation? That also pulls in outside data.
>
> **Marcus:** Common confusion. Classic RAG retrieves once, before it generates. ReAct decides at runtime when to retrieve, what to retrieve, and how many times. So RAG can be one tool inside a ReAct agent. Retrieval becomes just another action in the loop.
>
> **Jess:** Okay, let's get to the sample prompts. The financial analyst and the life sciences assistant.
>
> **Marcus:** Both follow the same template, and it's worth memorizing. A persona. A required format where each turn is exactly one THINK and one ACT. A list of tools, each with a signature, a usage note, and an example call. A special final answer tool the agent may only call once it has everything. And a worked example that starts the loop. In the finance prompt, the user wants MegaCorp's price-to-earnings ratio compared with Innovate Inc's, plus recent news. The first THINK splits that into two questions, and the first ACT calls get stock quote for MegaCorp. The clinical-trials prompt searches for trials targeting EGFR, gets back a list with phases, and then pulls details only for the Phase three trial.
>
> **Jess:** Why only one tool call per turn?
>
> **Marcus:** So the model has to wait for a real observation before it reasons again. That leads to a failure mode I'd add to your notes: if you don't stop generation after the ACT, the model may write its own OBSERVATION and make up the tool's result. In practice, you stop at the end of the action, run the tool in your code, and insert the real observation. Native tool-calling APIs do that for you.
>
> **Jess:** And that pin from earlier. Tool descriptions.
>
> **Marcus:** There it is. Look at how much those samples spell out: what each tool returns, when to use it, an example call. That's what your refinement notes meant by optimizing tool descriptions. A vague description means the agent calls the wrong tool or calls it at the wrong time.
>
> **Jess:** Last deep-dive topic: prompt chaining. How is that different from chain-of-thought? They sound almost the same.
>
> **Marcus:** Your study guide sums it up in one line. Chain-of-thought is thinking step by step inside one call. Chaining is you writing the steps as separate prompts, with your code in between. Think of an assembly line. Each station has one job, a defined input contract, a defined output contract, and ideally a quality gate before the work moves on.
>
> **Jess:** What's the payoff? More calls means slower and more expensive.
>
> **Marcus:** True, and the notes list those costs: latency, tokens, engineering overhead, and context that gets lost between steps. The benefits are accuracy, since each call focuses on one subtask; debuggability, since you can inspect every intermediate output; control, since deterministic code can validate or branch; and right-sizing, meaning a cheap model for easy steps and a strong one for hard steps. Now back to the cold open. If each step succeeds with probability p, an n-step chain succeeds with p to the n. Zero point nine five to the fifth is about seventy-seven percent. Gates and retries are what stop that compounding.
>
> **Jess:** So a gate is a checkpoint.
>
> **Marcus:** It can be code, like "is this valid JSON, are the required fields there," or it can be an LLM judge with a rubric that answers pass or fail. The bigger idea in this note is the spectrum. At one end is a single prompt. Then a fixed chain. Then a workflow with LLM-based routing. Then an agent, where the model picks its steps in a loop. Then multi-agent. What changes along the way is who decides the next step, your code or the model.
>
> **Jess:** And ReAct sits at the agent end.
>
> **Marcus:** Right. Your notes describe ReAct as a chain whose length and steps the model chooses at runtime. The principle is to move toward the agent end only when the task requires it. Autonomy buys flexibility, and you pay for it in cost, latency, and unpredictability. Say you're building a support-ticket system. A router that sends billing, technical, and other tickets to specialized chains is usually a better starting point than a fully autonomous agent.
>
> **Jess:** Run me through the other patterns quickly.
>
> **Marcus:** Sequential: outline, draft, edit, format. Routing: a classifier picks the branch, and always include an "other" route. Parallelization: either sectioning the work or voting on it. Map-reduce for inputs too big for one context window. Orchestrator-workers, where an LLM decides the subtasks at runtime. That's the difference from parallelization, where the subtasks are fixed in code. Evaluator-optimizer, a generate-and-critique loop, and always cap the iterations. And plan-and-execute, which gives you a plan you can inspect and even have a human approve.
>
> **Jess:** What goes wrong in practice?
>
> **Marcus:** Four big ones. Error propagation. Context loss. Goal drift, where each step optimizes for the previous step's output instead of the real goal; the fix is to re-inject the original user request at later steps. And the security one: chains amplify prompt injection. Untrusted text from a web page or email gets passed into several downstream prompts, and some of them may have tools. So keep tool-using steps separate from steps that read untrusted content, and require confirmation before anything irreversible.
>
> **Jess:** And how do you know a chain is worth the complexity?
>
> **Marcus:** Evaluate end to end on a fixed test set. Evaluate each step against its own contract so you can find where failures happen. Then ablate: remove or merge steps and see whether quality actually drops. That's the refinement mindset, applied to the structure of the chain.
>
> **Jess:** Lightning round time. You ask, I answer.
>
> **Marcus:** Six steps, each ninety percent reliable. Chain reliability?
>
> **Jess:** Zero point nine to the sixth, so about fifty-three percent. Add gates with retries.
>
> **Marcus:** Correct. You changed only the examples to all caps. Why wasn't the output all caps?
>
> **Jess:** Because nothing told it to. Examples reinforce instructions, they don't replace them.
>
> **Marcus:** Parallelization versus orchestrator-workers?
>
> **Jess:** In parallelization, code defines the subtasks. In orchestrator-workers, the LLM decides them at runtime.
>
> **Marcus:** Chain-of-thought or ReAct for a logic puzzle where all the facts are in the prompt?
>
> **Jess:** Chain-of-thought. It doesn't need to go get anything.
>
> **Marcus:** Perfect score. Let's wrap up. Three takeaways. One: a prompt has five components. Change one at a time, measure over several runs, and write down anything that matters instead of hoping the examples imply it. Two: chain-of-thought reasons over what the model already has, and its reasoning isn't always faithful. ReAct reasons while gathering new observations through tools, and it's only as good as those tools and their descriptions. Three: chaining lets you inspect and control each step, but reliability compounds as p to the n, so use gates and retries, re-inject the goal, and give the model more control only when the task needs it.
>
> **Jess:** And the think-about-it question?
>
> **Marcus:** Go back to the Demand-Spike Detective. If you rebuilt it as a ReAct agent, what three tools would you give it, and what gate would you put in place so it doesn't report a confident but unsupported cause, like that competitor price drop?
>
> **Jess:** Ooh, I like that one. That's it for today's MS AI Daily. Thanks, Marcus.
>
> **Marcus:** Thanks, Jess. Keep reasoning, keep acting, and we'll see you tomorrow.
