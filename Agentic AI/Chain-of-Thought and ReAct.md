### Overview

Two common frameworks for improving how [[Large Language Models]] solve complex problems are:

- **Chain-of-Thought (CoT)** — reason through a problem in intermediate steps before producing an answer.
- **ReAct** — combine reasoning with actions, observations, and [[tool use]] in a loop.

> **Naming note:** The correct name/casing is **ReAct** (short for "Reason + Act" / "Reasoning and Acting"), not "ReACT." It's easy to over-capitalize since it reads like an acronym, but it isn't one.

**Origin papers** (for grounding, not required reading):

- CoT — Wei et al., 2022, _"Chain-of-Thought Prompting Elicits Reasoning in [[Large Language Models]]"_
- ReAct — Yao et al., 2022, _"ReAct: Synergizing Reasoning and Acting in Language Models"_
- Self-Consistency — Wang et al., 2022
- [[Tree-of-Thought]] — Yao et al., 2023

Related notes:

- [[Large Language Models]]
- [[Prompt Engineering]]
- [[AI Agents]]
- [[Agentic AI]]
- [[Tool Use]]
- [[Retrieval-Augmented Generation]]
- [[LLM Hallucinations]]
- [[ReAct prompt Samples]]
- [[CoT prompt Samples]]

---

## Chain-of-Thought

### What is Chain-of-Thought?

**Chain-of-Thought (CoT)** is a prompting and reasoning technique where a model performs intermediate reasoning before arriving at a final answer.

Conceptually:

Problem
   ↓
Reasoning
   ↓
Intermediate conclusions
   ↓
Final answer

Instead of directly mapping:

Question → Answer

the model performs something closer to:

Question → Decompose → Reason → Validate → Answer

### Why CoT Helps

Chain-of-Thought is particularly useful for tasks involving:

- Multi-step mathematics
- Logic problems
- Troubleshooting
- Planning
- Coding
- Root-cause analysis
- Decision making
- Comparing multiple constraints

Example:

Problem:
A network has 500 devices. 4% are offline.
How many devices are online?

Reasoning:
4% of 500 = 20
500 - 20 = 480

Answer:
480 devices are online.

The intermediate reasoning reduces the likelihood of jumping directly to an incorrect conclusion.

---

### Types of Chain-of-Thought

#### Zero-Shot CoT

The model is simply instructed to reason carefully.

Example concept:

Analyze the problem step-by-step before answering.

No examples are provided.

---

#### Few-Shot CoT

Examples demonstrate the reasoning pattern before giving the real problem.

Example:
Problem A
Reasoning A
Answer A

Example:
Problem B
Reasoning B
Answer B

Now solve:
Problem C

[[Few-shot prompting]] can improve consistency by showing the model the expected reasoning structure.

See:

- [[Few-Shot Prompting]]
- [[Prompt Engineering]]

---

#### Self-Consistency

Instead of relying on one reasoning attempt, the model generates multiple possible reasoning paths and compares their conclusions.

Conceptually:

          → Reasoning Path A →
Problem   → Reasoning Path B →  Consensus → Answer
          → Reasoning Path C →

This can improve accuracy on problems where multiple valid reasoning approaches exist. In practice this is usually done by sampling the model several times at nonzero temperature and taking a majority vote over final answers.

Related:

- [[Model Evaluation]]
- [[AI Reliability]]

---

#### [[Tree-of-Thought]] (extension)

Where CoT commits to a single linear reasoning path, **[[Tree-of-Thought]]** lets the model explore multiple partial reasoning branches, evaluate them, and backtrack from dead ends — closer to a search process than a straight line. It's more expensive but can outperform plain CoT on problems with a large search space (e.g., puzzles, planning).

See: [[Tree-of-Thought]]

---

### CoT: Prompted vs. Built-In Reasoning

The examples above describe **prompted CoT** — you explicitly ask a standard model to "think step by step," and it produces reasoning text as part of its response.

Newer **reasoning models** (e.g., OpenAI's o-series, DeepSeek-R1, Claude's extended thinking) are trained — often with reinforcement learning — to generate long internal reasoning traces automatically, without needing an explicit CoT instruction in the prompt. The underlying idea is the same (intermediate steps before a final answer), but the mechanism differs: one is elicited by prompting, the other is baked into how the model was trained to respond. This distinction matters when deciding whether you need a CoT prompt at all, since it may be redundant with a model that already reasons by default.

---

### Limitations of Chain-of-Thought

Reasoning does not guarantee correctness.

Possible failures include:

- Incorrect assumptions
- Logical errors
- Hallucinated facts
- Overcomplicated reasoning ("overthinking" simple problems)
- Reasoning from incorrect source data
- Confident but invalid conclusions
- **Unfaithful reasoning** — the visible reasoning steps don't necessarily reflect what actually determined the model's answer. The model can produce a plausible-looking chain of steps as a post-hoc rationalization rather than a true trace of its computation (see Turpin et al., 2023). This means CoT output is not a reliable audit log of _why_ the model answered as it did — treat it as evidence, not proof.

A useful principle is:

> Better reasoning cannot compensate for bad information.

For real-world systems, reasoning often needs to be combined with external data or tools.

That leads to **ReAct**.

---

## ReAct

### What is ReAct?

**ReAct** stands for:

**Reason + Act** (from "Reasoning and Acting")

The framework allows an AI system to alternate between:

1. Reasoning
2. Taking an action
3. Observing the result
4. Updating its reasoning

The loop looks like:

Reason
  ↓
Act
  ↓
Observe
  ↓
Reason
  ↓
Act
  ↓
Observe
  ↓
Final Answer

It was originally demonstrated on two kinds of tasks: knowledge-intensive Q&A (where "actions" were search-API calls, e.g., against Wikipedia) and interactive decision-making in simulated environments (e.g., navigating a virtual house, shopping on a mock website). Modern usage generalizes "action" to any tool call — API, database query, code execution, etc.

This is a foundational pattern behind many [[AI Agents]].

---

## The ReAct Loop

A simplified ReAct workflow might look like:

Thought:
I need to determine whether this router is reachable.

Action:
Ping the router.

Observation:
100% packet loss.

Thought:
The device may be offline, but ICMP could also be blocked.

Action:
Attempt SNMP query.

Observation:
SNMP timeout.

Thought:
The device appears unreachable from the monitoring system.

Action:
Check upstream router.

Observation:
Upstream router is reachable.

Conclusion:
The failure is likely between the upstream router and the target device.

The important distinction is that the model is **gathering new information while reasoning**, and each new observation can change its next step — unlike CoT, where the reasoning path is fixed once generation starts.

---

## Chain-of-Thought vs ReAct

| Feature                                   | Chain-of-Thought | ReAct                                   |
| ----------------------------------------- | ---------------- | --------------------------------------- |
| Reasoning                                 | Yes              | Yes                                     |
| External tools                            | Usually no       | Yes                                     |
| New information gathered                  | No               | Yes                                     |
| Iterative                                 | Sometimes        | Usually                                 |
| Good for logic problems                   | Excellent        | Good                                    |
| Good for troubleshooting                  | Good             | Excellent                               |
| Good for autonomous agents                | Limited          | Excellent                               |
| Can act on stale/wrong internal knowledge | Yes (risk)       | Lower risk — verifies against live data |

A simplified comparison:

Chain-of-Thought

Question
   ↓
Reason
   ↓
Reason
   ↓
Answer

ReAct

Question
   ↓
Reason
   ↓
Tool / Action
   ↓
Observation
   ↓
Reason
   ↓
Tool / Action
   ↓
Answer

---

## ReAct and [[Tool Use]]

Actions may include:

- Web searches
- Database queries
- API calls
- Running code
- Querying monitoring systems
- Reading documentation
- Retrieving files
- Sending commands
- Searching knowledge bases

Examples:

LLM → Sonar API
LLM → Zabbix API
LLM → NetBox
LLM → SQL Database
LLM → Web Search
LLM → Python

This makes ReAct highly relevant to [[Tool Use]] and [[Agentic AI]].

---

## Example: Network Operations

Suppose an agent receives:

> Customers connected to Tower A are reporting packet loss.

A Chain-of-Thought system might reason:

Possible causes include:

- Backhaul congestion
- RF interference
- Sector failure
- Router CPU load
- Packet loss upstream

Note that this is where CoT alone tops out — it can list plausible causes but has no way to confirm which one is actually happening without querying real systems.

A ReAct system could actually investigate.

Reason:
First determine whether the tower itself is reachable.

Action:
Query Zabbix.

Observation:
Tower router is reachable.

Reason:
Check sector interfaces.

Action:
Query interface utilization.

Observation:
Sector 3 is at 98% utilization.

Reason:
Determine whether this is abnormal.

Action:
Query historical traffic.

Observation:
Normal utilization is approximately 55%.

Conclusion:
Sector 3 is experiencing abnormal congestion.

This is the difference between **reasoning about a system** and **interacting with the system while reasoning**.

---

## ReAct and Agentic Systems

ReAct is commonly part of larger agent architectures.

A basic agent architecture may look like:

            ┌──────────────┐
            │     Goal     │
            └──────┬───────┘
                   ↓
            ┌──────────────┐
            │    Reason    │
            └──────┬───────┘
                   ↓
            ┌──────────────┐
            │ Select Tool  │
            └──────┬───────┘
                   ↓
            ┌──────────────┐
            │    Action    │
            └──────┬───────┘
                   ↓
            ┌──────────────┐
            │ Observation  │
            └──────┬───────┘
                   ↓
                 Repeat

Additional components may include:

- [[AI Memory]]
- [[Vector Databases]]
- [[Retrieval-Augmented Generation]]
- [[Planning Agents]]
- [[Multi-Agent Systems]]
- [[Model Context Protocol]]
- [[Knowledge Graphs]]

---

## ReAct vs RAG

These concepts are related but different.

**RAG** retrieves external information, typically once, before generating an answer:

Question
   ↓
Search Knowledge Base
   ↓
Retrieve Context
   ↓
LLM
   ↓
Answer

**ReAct** decides dynamically when and how to retrieve or act, and can do so multiple times, adjusting based on what it finds:

Question
   ↓
Reason
   ↓
Search
   ↓
Observe
   ↓
Reason
   ↓
Query API
   ↓
Observe
   ↓
Answer

RAG can therefore be **one of the tools used inside a ReAct agent** — retrieval becomes just another action in the loop rather than a one-shot step before generation.

See:

- [[Retrieval-Augmented Generation]]
- [[Vector Databases]]

---

## Key Concept

The progression can be thought of as:

Basic LLM
Question → Answer

Chain-of-Thought
Question → Reason → Answer

RAG
Question → Retrieve → Answer

ReAct
Question → Reason → Act → Observe → Reason → Answer

Agentic AI
Goal → Plan → Reason → Act → Observe → Adapt → Repeat

---

## Practical Mental Model

Use **Chain-of-Thought** when the model already has enough information and primarily needs to reason.

Use **ReAct** when solving the problem requires interacting with external systems or gathering additional information.

In short:

CoT = Think through the problem.

ReAct = Think → Do something → See what happened → Think again.

And remember: neither one guarantees a _correct_ or _faithful_ answer — CoT can rationalize a wrong answer convincingly, and ReAct is only as good as the tools and observations it's given.

---

## Related Notes

- [[Artificial Intelligence]]
- [[Large Language Models]]
- [[Prompt Engineering]]
- [[Few-Shot Prompting]]
- [[Tree-of-Thought]]
- [[AI Agents]]
- [[Agentic AI]]
- [[Tool Use]]
- [[AI Memory]]
- [[Retrieval-Augmented Generation]]
- [[Vector Databases]]
- [[Knowledge Graphs]]
- [[Model Context Protocol]]
- [[Multi-Agent Systems]]
- [[LLM Hallucinations]]
- [[Model Evaluation]]
- [[AI Reliability]]

---