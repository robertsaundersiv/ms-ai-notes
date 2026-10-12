---
title: "Implementing LLM Feedback Loops – Flashcards"
type: flashcards
source: "[[Implementing LLM Feedback Loops]]"
created: 2026-09-26
tags:
  - flashcards
---

#flashcards/agentic-ai/feedback-loops/lab

What are the four stages of a feedback loop's architecture, per Lesson 5?
?
Generation, programmatic evaluation, feedback construction, and iterative re-prompting.

In a code-generation feedback loop, what are the two non-LLM components?
?
An evaluator that runs the generated code against test cases, and a feedback formatter that turns the results into text the model can act on.

What does a good revision prompt contain, beyond the original task?
?
The model's prior output plus specific, actionable feedback: each failing test's inputs, expected value, and actual value or error message.

How can tests communicate requirements the task description never mentions?
?
New requirements show up only as failing tests in the feedback, so the test suite effectively becomes the specification.

How can a test harness check that code correctly raises an error?
?
Treat the expected exception type as the expected result, and count the test as passed when the call raises an exception of that type.

Why do test-input packaging mistakes cause confusing argument-count errors?
?
If a harness unpacks test inputs as arguments, a single list input that isn't wrapped correctly gets spread into many arguments. The harness is wrong, not the generated code.

Why is extracting code from the model's reply a fragile part of the loop?
?
Exact-match parsing of Markdown fences fails when the model omits or alters them. A parse failure should trigger a retry, not crash the loop.

How can notebook state make a broken feedback loop look like it works?
?
Variables left over from earlier cells get reused, so the loop can report success without making any new LLM calls. Restart and run everything, or wrap the loop in a function.

Why isn't running generated code in an empty namespace a sandbox?
?
The language still gives it built-in access to imports, files and the network. You need process or container isolation with resource limits and no network.

Why is "iterate until you pass all tests" a poor instruction inside a feedback prompt?
?
A single completion can't execute code or see results. The harness does the iterating, so ask the model for one corrected attempt.

What does a successful feedback-loop run typically show in a lab?
?
The pass count rises across iterations as the model adds the missing behaviors that failing tests revealed, without being told about them directly.

Name two harness weaknesses that can make correct code fail or wrong code pass.
?
Exact float equality (correct averages can fail) and loose type comparison (ints and floats, or booleans and ints, can't be told apart).

Why should a code-correcting loop return the best iteration rather than the last?
?
Later revisions can regress. Tracking pass counts and returning the best guards against shipping a worse version.

What makes a feedback loop a self-correcting system rather than just retrying?
?
Each attempt gets objective, external evaluation, and that evaluation is fed back as actionable text. Retries are directed by evidence instead of being independent re-rolls.
