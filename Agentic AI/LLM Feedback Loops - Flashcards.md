---
title: "LLM Feedback Loops – Flashcards"
type: flashcards
source: "[[LLM Feedback Loops]]"
created: 2026-09-23
tags:
  - flashcards
---

#flashcards/agentic-ai/feedback-loops

What is an LLM feedback loop?
?
Generate an output, evaluate it, feed the evaluation back into the next prompt, and revise. Repeat until a stop condition is met.

What is the core mechanism underneath a feedback loop?
?
Prompt chaining. The output (plus its evaluation) of one step becomes the input to the next.

What five parts does every feedback loop need?
?
Generator, evaluator, feedback formatter, stop condition, and memory (what carries between iterations).

What are the four sources of feedback named in the lecture?
?
Self-correction, external tools, validation checks, and user input.

Which feedback source is weakest on its own, and why?
?
Self-correction. The critic shares the generator's knowledge and blind spots, so without new information or a rubric it often misses errors.

Why are external tools the strongest feedback source for code?
?
Running code gives objective ground truth: errors, stack traces, and actual vs expected output.

What details should test-failure feedback include?
?
The input, the expected output, and the actual output (plus the location of the error if known).

How can a user supply feedback in the middle of an agent run?
?
Through a blocking tool call that pauses the agent until the user responds.

What are the four stop conditions a production loop should have?
?
Success criteria met, an iteration cap, a no-progress check, and a budget limit.

Why return the best iteration instead of the last one?
?
Loops can regress. A later iteration can be worse than an earlier one.

What three purposes does monitoring serve?
?
Evaluating effectiveness, debugging, and optimizing the process.

What four metrics does the lecture say to monitor?
?
Output quality, error rate, goal adherence, and the step-by-step trace log.

Why is the trace log called crucial?
?
It records the prompt, response and feedback at every step, which shows the agent's reasoning and makes debugging possible.

What does a score pattern like 2, 4, 3, 4, 3 indicate?
?
Oscillation: fixing one issue breaks another. Carry a fixed-issues list and evaluate against all criteria.

What is evaluator gaming in a feedback loop?
?
The output satisfies the evaluator without achieving the real goal, e.g. code that special-cases the test inputs.

How do you prevent goal drift across iterations?
?
Re-inject the original task into every iteration's prompt.

How do feedback loops differ from RL in what they change?
?
Feedback loops change outputs in context (temporary). RL changes the model's weights (permanent).

What baseline should a feedback loop beat to justify its cost?
?
Best-of-k sampling with the same compute budget.
