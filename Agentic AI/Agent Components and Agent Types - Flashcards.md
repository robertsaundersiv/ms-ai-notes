---
title: "Agent Components and Agent Types – Flashcards"
course: Agentic AI (Cd14526) – Course 1
type: flashcards
source: "[[Agent Components and Agent Types]]"
created: 2026-09-27
---

#flashcards/agentic-ai/agent-components-types

Flashcards for [[Agent Components and Agent Types]].

What are the five core components of an AI agent?
?
Persona, Knowledge, Prompting Strategy, Execution/Tools, and Interaction.

What does the Persona component define, and how is it usually set?
?
The agent's role in the workflow: its function, tone and style, expertise boundaries, and output format. It is usually set with the system prompt.

Why does a persona specify an output format such as JSON?
?
So the next step in the workflow (code or another agent) can reliably parse and use the output.

What four sources make up an agent's Knowledge?
?
Foundational LLM training, fine-tuning, external information retrieved via tools, and memory of current or past interactions.

Which knowledge sources can be updated without retraining the model?
?
External information via tools (including RAG) and memory, because they are injected into the context at runtime.

What four elements make up a Prompting Strategy?
?
System prompts, context incorporation (from memory or earlier steps), prompt engineering techniques (CoT, ReAct, few-shot), and structured instructions with a required output format.

What four things do Execution/Tools let an agent do?
?
Interact with the external world (e.g. APIs), manipulate data (calculations, queries), connect with other systems (email, records), and orchestrate other specialized agents.

What three aspects does the Interaction component cover?
?
Receiving input, delivering output (text, JSON, or triggering an action), and inter-agent communication.

What are the four agent types, from least to most capable?
?
Direct Prompting, Prompt Augmentation, Dynamic Context Augmentation, and Autonomous Agent.

What does a Direct Prompting agent do?
?
It relays the user's prompt to the LLM unmodified and returns the response. LLM role: Responder/Generator. Context: static. Autonomy: low. Use: simple Q&A and basic text generation.

What does a Prompt Augmentation agent do?
?
It enriches the prompt before the LLM call with a persona, few-shot examples, or retrieved documents. LLM role: Guided Responder/Generator. Context: pre-augmented static (e.g. RAG). Autonomy: low–medium.

What does a Dynamic Context Augmentation agent do?
?
It updates the LLM's context in real time during the task using tools and memory, so each result informs the next action. LLM role: Adaptive Responder/Processor. Autonomy: medium. Use: multi-turn conversations, tool use.

What does an Autonomous Agent do?
?
It takes a high-level goal, plans sub-tasks, executes them with tools, and self-corrects with minimal human intervention. LLM role: Planner/Executor/Reasoner. Context: dynamic internal/external memory. Autonomy: high.

What is the key difference between Prompt Augmentation and Dynamic Context Augmentation?
?
Prompt Augmentation adds context once before the call (static). Dynamic Context Augmentation keeps updating the context during the task from tool results and memory.

If each step succeeds with probability 0.9, what is the end-to-end success rate of a 12-step autonomous task?
?
0.9^12 ≈ 0.28, which is why autonomous agents need self-correction, checkpoints, and stop conditions.

What design rule guides the choice of agent type?
?
Choose the least autonomous type that solves the task, since each step up adds cost, variance, and attack surface.
