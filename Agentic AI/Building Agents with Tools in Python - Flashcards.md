---
title: "Building Agents with Tools in Python – Flashcards"
type: flashcards
source: "[[Building Agents with Tools in Python]]"
created: 2026-09-30
tags:
  - flashcards
---

#flashcards/agentic-ai/tools-in-python

What is the simplest way to interact with a chat model?
?
A single-turn query: send one user message and get one response back.

How do you structure a multi-turn or role-framed conversation?
?
As an ordered list of role-tagged messages (system, user, assistant, tool) sent together on each call.

What does the system message do?
?
Sets the model's role, persona and behavior, including telling it which tools exist and when to use them.

Why must you resend the whole conversation on every call?
?
The model is stateless. The conversation exists only in the message history your code keeps.

How does a tool definition get its schema from a Python function?
?
The function name becomes the tool name, the docstring becomes the description, and the type hints become the parameter types.

Why does a tool function need clear documentation and typed parameters?
?
The description tells the model when to use the tool, and the types define the arguments it must supply. Both come from the code.

What does binding tools to a model do?
?
It attaches the tool schemas to every request so the model can reply with a tool call. It doesn't run anything.

When the model decides to use a tool, what does it return?
?
A structured tool-call request containing a call ID, the tool name and the arguments, instead of a text answer.

Who actually executes the tool?
?
The host application's code, never the model. The model only proposes the call.

What form do tool-call arguments usually arrive in?
?
A serialized JSON string, which your code must parse (and may need to validate) before calling the function.

How is a tool's result returned to the model?
?
As a tool-role message containing the result, the tool name, and the ID of the call it answers.

What links a tool result to the request it answers?
?
The call ID. The result must carry the same ID as the tool call in the preceding assistant message.

What is the tool-call invariant?
?
Every tool call in an assistant message must get exactly one matching tool result, placed after that message and before the next model call.

What two steps are easy to forget in a manual tool-calling flow?
?
Adding the model's tool-call message to the history, and adding the tool result to the history before calling the model again.

What happens if the tool result never reaches the history before the next call?
?
The model sees the same history and asks for the tool again, or the API rejects the request.

Why is handling only the first tool call fragile?
?
The model can request several tool calls in one turn (parallel calls), and each one needs its own result.

What turns a single tool round trip into an agent?
?
A bounded loop: call the model, run any requested tools, append the results, and repeat until it answers without tool calls or hits a step limit.

Why look up tools in an explicit allow-list rather than calling whatever name the model gives?
?
The model can then only trigger functions you deliberately exposed, never arbitrary code.

Why return tool errors as results instead of crashing?
?
The error becomes an observation, so the model can fix its arguments and retry.

How does history growth affect cost in a tool loop?
?
Each call resends the full, growing history, so total input tokens grow faster than linearly with the number of steps.

How can you detect that a model hallucinated a tool answer?
?
Check the trajectory. A factual answer with no tool call before it means the model answered from its priors.
