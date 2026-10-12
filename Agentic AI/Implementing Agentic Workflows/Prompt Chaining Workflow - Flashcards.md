---
title: "Prompt Chaining Workflow – Flashcards"
course: Agentic AI (Cd14526) – Course 1
type: flashcards
source: "[[Prompt Chaining Workflow]]"
created: 2026-09-27
---

#flashcards/agentic-ai/workflow-patterns/prompt-chaining

Flashcards for [[Prompt Chaining Workflow]].

What is prompt chaining?
?
A workflow pattern that decomposes a complex task into a sequence of smaller LLM calls, where the output of one call becomes the input of the next.

What analogy does the reading use for prompt chaining?
?
A factory assembly line: specialized stations each do one task, using the output of the previous station.

What three benefits does prompt chaining offer?
?
Each LLM call is simpler, reasoning across multiple steps improves, and hallucinations can be reduced by keeping the model focused.

What is the inherent risk of prompt chaining?
?
Error propagation: because each output feeds the next step, a flawed early output can carry through and compound, derailing the whole workflow.

What is intermediate validation?
?
Checking the accuracy, relevance, and format of each step's output before it is passed to the next step, acting as quality-control gates.

What are the four intermediate validation methods?
?
Programmatic checks, LLM-based validation, rule-based validation, and confidence scoring.

What do programmatic checks verify? Give an example.
?
Specific conditions using custom code, such as valid JSON, a length limit, or numbers within an expected range.

When is LLM-based validation the right choice?
?
For subtle qualities that are hard to codify, such as factual accuracy, relevance, or tone.

How does rule-based validation differ from programmatic checks?
?
It focuses on adherence to a declared set of explicit rules (e.g. an email must have a salutation and a closing), even though the rules are often implemented in code.

How does confidence scoring work as validation?
?
The generating LLM's confidence score is compared against a threshold; outputs below it trigger corrective action.

What are the four strategies when a validation gate fails?
?
Retry, re-prompt with feedback, fallback mechanisms, and simplified critique and refinement.

When is a plain retry appropriate?
?
For transient LLM issues, where simply re-running the prompt may produce a valid output.

What does re-prompting with feedback involve?
?
Adding the validator's specific failure reasons (e.g. "summary too long") to a revised prompt and asking the LLM to regenerate.

What are the fallback options when retries fail?
?
Terminate the chain and log an error, route to an alternative simpler task, or return a predefined safe output.

What is simplified critique and refinement?
?
One prompt asks the LLM to critique its previous output against criteria; a second prompt asks it to refine the output based on that critique.

What should be logged at each step of a chain?
?
Inputs, outputs, and validation results, so you can debug where and why the chain fails.

What is selective context passing?
?
Passing only the most relevant parts of previous outputs to the next step, planned by what each step truly needs.

What is contextual reiteration?
?
Restating important context, such as the goal and constraints, within each new prompt so the LLM doesn't forget early details.

Steps succeed with p = 0.9. What is the success rate of an unvalidated 5-step chain?
?
0.9^5 ≈ 0.59.
