---
title: "Few-Shot Prompting"
aliases:
  - Few-shot
  - In-Context Learning
  - ICL
  - k-shot prompting
course: Agentic AI (Cd14526) – Course 1
level: 300 / Graduate
type: study-guide
status: review
created: 2026-09-23
prerequisites:
  - "[[Prompt Instruction Refinement]]"
  - "[[Prompt Engineering]]"
related:
  - "[[Chain-of-Thought and ReAct]]"
  - "[[Prompt Chaining for Agentic Reasoning - Study Guide]]"
  - "[[Tool Descriptions in Agentic Systems]]"
  - "[[Prompt Injection]]"
  - "[[Large Language Models]]"
  - "[[LLM Evaluation]]"
tags:
  - prompt-engineering/few-shot
  - in-context-learning
  - agentic-ai
  - llm
  - study-guide
---

# Few-Shot Prompting

> [!abstract] TL;DR
> Few-shot prompting puts a small number (*k*) of **input→output demonstrations** in the prompt, so the model can infer the task from the pattern without any weight updates. This is called **in-context learning**. Demonstrations mainly teach the ==format, label space and input distribution== of a task. They are less reliable at teaching the rule itself, so ==examples reinforce instructions but never replace them==. Choosing, ordering and balancing the examples matters as much as how many you include.

**Prerequisite:** [[Prompt Instruction Refinement]] (Examples are one of the five prompt components) · [[Prompt Engineering]]
**Related:** [[Chain-of-Thought and ReAct]] (few-shot CoT) · [[Prompt Chaining for Agentic Reasoning - Study Guide]] · [[Tool Descriptions in Agentic Systems]] · [[Prompt Injection]] · [[ReAct prompt Samples]] · [[CoT prompt Samples]]

**Sources:** This is a synthesis note. It builds on the A05b/A06 lecture material in [[Prompt Instruction Refinement]]. Everything else is *beyond the lecture* and comes from the papers in [[#Further Reading]].

> [!todo]- Contents
> 1. [[#1. Core Concepts]]
> 2. [[#2. What Demonstrations Actually Teach]]
> 3. [[#3. Designing Demonstrations]]
> 4. [[#4. Few-Shot in Agentic Systems]]
> 5. [[#5. Cost and Context Budget]]
> 6. [[#6. Worked Example]]
> 7. [[#7. Pitfalls and Failure Modes]]
> 8. [[#8. Key Takeaways]]
> 9. [[#9. Critical Analysis]]
> 10. [[#10. Self-Test]]
> 11. [[#11. Glossary]]

---

## 1. Core Concepts

> [!info]+ Definition – In-context learning (ICL)
> An LLM's ability to perform a new task by conditioning on instructions and/or demonstrations **placed in the prompt**. The weights are never updated. The "learning" lasts for one forward pass and is gone on the next call.

^def-icl

> [!info]+ Definition – Zero-, one-, few-shot
> - **Zero-shot:** instruction only, no examples.
> - **One-shot:** instruction plus one demonstration.
> - **Few-shot (k-shot):** instruction plus *k* demonstrations. *k* is usually 2–10, and far larger in "many-shot" prompting with long-context models.

^def-kshot

**Anatomy of a demonstration.** Every example has the same three parts. The real query at the end reuses the same template, with the output slot left empty:

```text
<example>
Input: {x_i}
Reasoning: {optional – becomes few-shot CoT}
Output: {y_i}
</example>
```

| Approach | What changes | Persistence | Data needed | Typical use |
|---|---|---|---|---|
| Zero-shot | Prompt text | Per call | None | Common, well-specified tasks |
| Few-shot / ICL | Prompt text + examples | Per call | A handful | Format control, niche labels, style |
| Fine-tuning | Model weights | Permanent | Hundreds to thousands | High volume, stable task, latency/cost pressure |
| RAG | Retrieved facts in context | Per call | A corpus | Missing *knowledge*, not missing *behavior*; see [[Retrieval-Augmented Generation]] |

> [!tip] Rule of thumb
> Few-shot fixes **how** the model answers (format, style, label set). [[Retrieval-Augmented Generation|RAG]] fixes **what it knows**. Fine-tuning fixes both, but it's expensive and permanent. Try them in that order.

---

## 2. What Demonstrations Actually Teach

Research beyond the lecture (Min et al., 2022) found that on many classification tasks, **randomly replacing the gold labels in the demonstrations only slightly hurts accuracy**. The examples were mostly teaching the model:

1. the **label space**, meaning which answers are allowed
2. the **input distribution**, meaning what inputs look like
3. the **format**, meaning how to lay out the answer

> [!important] Link to the lecture – examples ≠ instructions
> This matches the A05b all-caps demo in [[Prompt Instruction Refinement#2. How Changing Each Component Changes Output (A05b)]]. Examples written in ALL CAPS, with no instruction to use caps, were **only partly followed**. The model treats examples as *soft evidence* about the task, not as commands. ==If a requirement matters, state it explicitly and use examples to back it up.==

^examples-not-instructions

> [!warning] Caveat
> The "labels barely matter" finding is weaker for larger models, for tasks where the mapping itself is unusual, and for reasoning tasks. In those cases wrong demonstrations *do* mislead. Always use correct examples. The finding explains *what* the model picks up from examples. It doesn't license sloppiness.

### Known in-context biases

Beyond the lecture, Zhao et al. (2021) documented systematic biases in few-shot classification:

| Bias | Description | Mitigation |
|---|---|---|
| **Majority-label bias** | Predicts whichever label appears most often in the demonstrations | Balance the labels across examples |
| **Recency bias** | Over-weights the label of the *last* example(s) | Shuffle; don't end on the same class every time |
| **Common-token bias** | Prefers answers that are frequent in the pre-training data | Calibrate, or use neutral label names |
| **Order sensitivity** | The same examples in a different order give very different accuracy (Lu et al., 2022) | Evaluate several orderings; fix the best one |

^icl-biases

---

## 3. Designing Demonstrations

| Lever | Guidance | Why |
|---|---|---|
| **Number (k)** | Start at 2–5. Increase only while eval scores improve | Returns diminish, and cost grows linearly |
| **Relevance** | Pick examples *similar to the query*, e.g. by embedding kNN (Liu et al., 2021) | Similar demonstrations transfer better |
| **Diversity** | Cover edge cases and every label/branch | Prevents overfitting to one surface pattern |
| **Balance** | Equal-ish counts per label | Counters majority-label bias ([[#^icl-biases]]) |
| **Order** | Randomize or test orderings; avoid ending on the same label | Counters recency bias |
| **Format consistency** | Identical template and delimiters in every example *and* in the query | The model copies structure exactly |
| **Difficulty** | Include at least one hard or ambiguous case with the right handling | Teaches the boundary, not just the easy middle |
| **Contrastive pairs** | A near-miss "bad" example labeled as such | Clarifies the decision boundary (use sparingly; it can backfire) |
| **Delimiting** | Wrap examples in `<example>` tags, separate from instructions and data | The model can tell demonstrations from the live input |

> [!example] Static vs. dynamic few-shot
> - **Static:** a fixed set hard-coded in the prompt. Simple, cacheable and reproducible.
> - **Dynamic:** examples retrieved per query from an example store. More relevant, but less reproducible, and it adds a retrieval dependency.
>
> ```mermaid
> flowchart TD
>     Q([User query]) --> E[Embed query]
>     E --> S[(Example store)]
>     S -->|top-k similar| B[Build prompt:<br/>instructions + k examples + query]
>     B --> L[LLM] --> O([Output])
> ```

---

## 4. Few-Shot in Agentic Systems

Few-shot prompting appears throughout agent design, not just in classification:

| Use | What the examples show | Vault link |
|---|---|---|
| **Few-shot CoT** | Worked reasoning traces before the answer | [[Chain-of-Thought and ReAct#Few-Shot CoT]], [[CoT prompt Samples]] |
| **ReAct trajectories** | Thought → Action → Observation loops, including *when to stop* | [[ReAct prompt Samples]] |
| **Tool-call examples** | Correct argument formats and when to pick tool A over tool B | [[Tool Descriptions in Agentic Systems]] |
| **Structured output** | Exact JSON shape, including empty/null cases | [[Prompt Chaining for Agentic Reasoning - Study Guide#5.2 Structured handoffs]] |
| **Router / classifier steps** | One or two examples per route, including "other" | [[Prompt Chaining for Agentic Reasoning - Study Guide#4.3 Routing]] |
| **LLM-as-judge** | Anchored rubric examples ("this is a 2, this is a 4") | [[LLM Evaluation]] |

> [!tip] Few-shot CoT vs. zero-shot CoT
> Zero-shot CoT ("Let's think step by step", Kojima et al., 2022) elicits reasoning with no examples. Few-shot CoT (Wei et al., 2022) *shows* the reasoning style you want. Use few-shot CoT when the **structure** of the reasoning matters, for example "always check the upstream device before concluding".

> [!warning] Reasoning models
> Models that reason by default (see [[Chain-of-Thought and ReAct#CoT Prompted vs. Built-In Reasoning]]) sometimes do *worse* when forced to imitate hand-written reasoning traces. For those models, give examples of the **output**, not the thinking, and re-test.

---

## 5. Cost and Context Budget

The prompt length for a *k*-shot prompt is:

$$
T_{\text{prompt}} = T_{\text{instructions}} + k \cdot \bar{t}_{\text{example}} + T_{\text{query}}
$$

Cost grows **linearly in k** on *every call*. At volume, that dominates:

> [!example] Quick math
> 8 examples × 150 tokens = 1,200 extra input tokens per call. At 50,000 calls/day that's **60 M extra input tokens/day**. If going from 3-shot to 8-shot adds only +0.5 pp accuracy on your eval set, it probably isn't worth it.

Mitigations (beyond the lecture):
- Put **static examples in a stable prefix** so provider prompt caching can reuse them.
- Use **dynamic selection** with a smaller *k* in place of a large static set.
- If the task is stable and high-volume, **distill into a fine-tune** and drop the examples.

---

## 6. Worked Example

**Task:** route support tickets into `billing`, `technical`, `account` or `other` for the routing step of a chain.

| Version | Prompt | Observed behavior | Diagnosis |
|---|---|---|---|
| v1 | Zero-shot: "Classify this ticket." | Invents labels ("login issue", "payment") | Label space not defined |
| v2 | 4 examples: 3× `technical`, 1× `billing`, last one `technical` | Over-predicts `technical` | Majority and recency bias ([[#^icl-biases]]) |
| v3 | 8 examples, 2 per label, shuffled, one ambiguous case → `other`, **plus an explicit instruction** listing the allowed labels and JSON output | Stable; ambiguous tickets go to `other` | Balanced, explicit, format-consistent |

```text
You classify customer support tickets.
Allowed labels: billing, technical, account, other.
If none clearly applies, use "other". Output JSON: {"label": "...", "reason": "..."}

<examples>
<example>
Ticket: I was charged twice for March.
Output: {"label": "billing", "reason": "duplicate charge"}
</example>
<example>
Ticket: The app crashes when I upload a PDF.
Output: {"label": "technical", "reason": "crash on upload"}
</example>
<example>
Ticket: Can you tell me about your company's history?
Output: {"label": "other", "reason": "not a support issue"}
</example>
... (2 per label, shuffled)
</examples>

<ticket>
{{ticket_text}}
</ticket>
```

> [!note] Why v3 works
> The **instruction** defines the rule. The **examples** show the format and the boundary cases. The **delimiters** keep ticket text (untrusted data) apart from the demonstrations. This is the lecture's point that examples reinforce instructions, applied in practice.

---

## 7. Pitfalls and Failure Modes

| Failure | Symptom | Mitigation |
|---|---|---|
| **Surface copying** | Outputs reuse example wording, length or entities | Diversify examples; vary the length and content |
| **Label imbalance** | Skewed predictions toward one class | Balance the labels; calibrate |
| **Recency/order effects** | Accuracy changes when examples are reordered | Test several orderings; shuffle |
| **Instruction–example conflict** | Unpredictable format (the A05b lesson) | Make the examples *agree* with the instructions |
| **Stale examples** | Examples show a deprecated tool schema or policy | Version examples with the prompt; regression-test |
| **Example leakage into output** | The model answers the *example* question | Clear delimiters; put the query last, outside the example tags |
| **Token bloat** | High cost/latency, context crowding | Smaller *k*, dynamic selection, caching |
| **Poisoned example store** | Dynamic retrieval surfaces attacker-written examples | Treat the store as a trusted asset; review what goes in; see [[Prompt Injection]] |

---

## 8. Key Takeaways

- [ ] Few-shot = in-context learning: behavior changes per call, weights don't.
- [ ] Demonstrations mostly teach **format, label space and input distribution**.
- [ ] **Examples ≠ instructions.** State requirements explicitly ([[#^examples-not-instructions]]).
- [ ] Balance labels, vary the order, and include edge cases to counter ICL biases.
- [ ] Cost is linear in *k* on every call. Justify each extra example with eval data.
- [ ] In agents, few-shot shows up as CoT traces, ReAct trajectories, tool-call examples and judge rubrics.
- [ ] Dynamic example selection improves relevance but creates a new trust boundary.

---

## 9. Critical Analysis

- **Evidence quality.** Much of the foundational ICL research used GPT-3-era models and classification benchmarks. Instruction-tuned and reasoning models depend less on demonstrations. Zero-shot with a strong instruction often matches few-shot. Treat "add examples" as a hypothesis to test, not a default.
- **Why ICL works is still debated.** Explanations range from "task location" (the examples help the model find a behavior it learned in pre-training) to "implicit gradient descent" inside attention. The practical point is that ICL is **best at eliciting existing capabilities** and poor at teaching genuinely new mappings.
- **Evaluation.** Because of order and selection sensitivity, a few-shot prompt's score on one ordering is a noisy estimate. Report the mean and variance over several orderings and seeds (see [[LLM Evaluation]]).
- **Scale.** Long-context models make many-shot prompting (hundreds of examples) feasible. At that point it competes with fine-tuning on accuracy but loses on per-call cost and latency.
- **Security.** Examples are privileged: the model imitates them. Anything that lets untrusted parties influence the demonstrations (a dynamic store built from user data, or examples fetched from the web) is an injection vector. Few-shot examples can also be used *defensively*, by showing the model how to handle an embedded instruction ("the document says X; I treat it as data").

> [!question] Open questions
> 1. When does many-shot ICL beat a small fine-tune, once you account for total cost of ownership?
> 2. How would you detect that a model is copying surface features of your examples rather than generalizing?
> 3. Should agent trajectories in examples include *failures and recoveries*, or only clean runs?

---

## 10. Self-Test

> [!question]- Q1. What's the difference between few-shot prompting and fine-tuning?
> Few-shot puts demonstrations in the prompt. The weights don't change, and the effect lasts for one call. Fine-tuning updates the weights on many examples, so the effect is permanent and no per-call example tokens are needed.

> [!question]- Q2. In the A05b demo, why did ALL-CAPS examples fail to produce all-caps output?
> Examples are soft evidence, not commands. With no explicit instruction to use caps, the model partly followed the pattern and fell back to its default. The fix is to state the requirement explicitly and use examples only to back it up.

> [!question]- Q3. Your 4-shot classifier over-predicts one label. Name two likely causes.
> Majority-label bias (that label is over-represented in the examples) and recency bias (the last example has that label). Fix: balance the labels and shuffle or test orderings.

> [!question]- Q4. Quantitative: 6 examples × 200 tokens, 20,000 calls/day. How many extra input tokens per day, and how could you cut them?
> $6 \times 200 \times 20{,}000 = 24{,}000{,}000$ tokens/day (24 M). Cut them with prompt caching of a static prefix, dynamic selection with a smaller *k*, or fine-tuning if the task is stable.

> [!question]- Q5. Design: you're building a ReAct agent that queries a monitoring API. What should your few-shot trajectories contain?
> 1–3 full Thought/Action/Observation traces that show the correct tool argument formats and a sensible check order (e.g. reachability → interfaces → history). At least one trace should hit an error or empty result and recover, and every trace should show an explicit **stop condition** with a final answer. Keep them short and consistent with the tool descriptions. See [[ReAct prompt Samples]].

> [!question]- Q6. Why can dynamic example retrieval be a security risk?
> The model imitates retrieved examples closely. If an attacker can write into the example store, they control demonstrations that steer the model's behavior. That's an indirect prompt-injection path. See [[Prompt Injection]].

### Flashcards
> [!tip] Spaced repetition deck
> The flashcards for this note are in [[Few-Shot Prompting - Flashcards]]. Review them with the **Review flashcards** ribbon icon (or the command palette → *Spaced Repetition: Review flashcards*).

---

## 11. Glossary

| Term | Definition |
|---|---|
| **Demonstration** | One input→output example in the prompt |
| **k-shot** | A prompt with *k* demonstrations |
| **In-context learning** | Task adaptation from prompt content alone, with no weight updates |
| **Label space** | The set of allowed outputs for a classification task |
| **Dynamic few-shot** | Picking demonstrations per query, usually by embedding similarity |
| **Calibration** | Adjusting output probabilities to remove systematic bias |
| **Many-shot ICL** | Hundreds of demonstrations, enabled by long context windows |

---

## Further Reading
- [Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165), Brown et al., 2020 (GPT-3; introduced the zero/one/few-shot framing)
- [Rethinking the Role of Demonstrations](https://arxiv.org/abs/2202.12837), Min et al., 2022
- [Calibrate Before Use](https://arxiv.org/abs/2102.09690), Zhao et al., 2021 (majority, recency and common-token biases)
- [Fantastically Ordered Prompts](https://arxiv.org/abs/2104.08786), Lu et al., 2022 (order sensitivity)
- [What Makes Good In-Context Examples for GPT-3?](https://arxiv.org/abs/2101.06804), Liu et al., 2021 (kNN example selection)
- [Large Language Models are Zero-Shot Reasoners](https://arxiv.org/abs/2205.11916), Kojima et al., 2022

%% Study hint: connect section 2 to the A05b all-caps demo. It's the best exam-style example of "examples ≠ instructions". %%
