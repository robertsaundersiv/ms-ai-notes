---
title: "Agentic AI Skills Scorecard – Flashcards"
type: flashcards
source: "[[Agentic AI Skills Scorecard - Study Guide]]"
created: 2026-09-26
tags:
  - flashcards
---

#flashcards/agentic-ai/scorecard

What are the core components of an AI agent's architecture?
?
The LLM (brain / next-action policy), instructions (goal, rules, persona, stop criteria), tools (act and observe), memory (short- and long-term), and an orchestrator that executes tools and enforces budgets and stop conditions.

In an agent, who actually executes a tool call: the LLM or the orchestrator?
?
The orchestrator. The LLM only proposes the action; the runtime runs the tool and returns the observation.

When should you use Chain-of-Thought instead of ReAct?
?
When the model already has all the information it needs and the challenge is reasoning (logic, maths, multi-step rules). CoT is cheaper and needs no tools.

When should you use ReAct instead of Chain-of-Thought?
?
When the task needs new or live information, or needs to take actions through tools. Observations ground the reasoning in real data.

What is the one-line difference between CoT and ReAct?
?
CoT makes the model think more; ReAct lets the model know more by acting and observing.

What four elements make a strong persona?
?
Expertise, audience, tone and style, and boundaries (what it must never do or should admit it doesn't know).

What do personas reliably change, and what should you not rely on them for?
?
They reliably change tone, register, format and vocabulary. Don't rely on them for factual accuracy or security; use context, tools and gates for that.

Name four ways to prompt Chain-of-Thought.
?
Zero-shot CoT ("think step by step"), few-shot CoT (worked reasoning examples), structured CoT (explicit steps plus output format), and self-consistency (sample several paths and vote).

What are the five components of a prompt used for refinement?
?
Role, Task, Output format, Examples, Context.

What is the core rule of systematic prompt refinement?
?
Change one component at a time, compare the outputs, and explain why they differ, as in the scientific method.

An LLM output is correct but breaks the downstream parser. Which prompt component do you fix?
?
The output format, e.g. a JSON schema or Pydantic model, ideally checked by a format gate.

What are the three steps of the ReAct loop?
?
Thought, Action (a tool call), Observation (the tool's result), repeated until a final answer or stop condition.

What is prompt chaining?
?
A multi-step workflow where the output of one LLM step becomes the input to the next.

What are the three core gate check types?
?
Format checks, content checks, and logic checks, run in code between chain steps.

What can happen when a gate check fails?
?
Retry with feedback, reroute to another path, or stop / escalate to a human.

What is a self-correcting system in the course's sense?
?
A feedback loop where an AI's output is evaluated objectively (e.g. unit tests), the failures are fed back as specific feedback, and the AI revises until it passes or hits a cap.

How is a gate check related to a feedback loop?
?
A gate that retries with its failure reason is the smallest possible feedback loop. A gate asks "may this pass?"; a loop asks "how do we make it pass?"

With 5 chain steps each succeeding with probability 0.9, what is end-to-end success?
?
About 0.59 (0.9 to the 5th power). This is why gates and retries at each step matter.

Why does structured output connect prompting to agentic patterns?
?
Structured output can be validated by code, which is what makes gate checks and feedback loops possible.

What are the four layers of the course's skill stack?
?
Control one call (persona, CoT, refinement), connect calls (ReAct, chaining), make it reliable (gates, feedback loops), and the system (agent architecture).
