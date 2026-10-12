---
title: "Implementing Orchestrator-Workers Workflow"
aliases:
  - Orchestrator-Workers Implementation
  - Permit Orchestrator
  - Lab Report Orchestrator
course: Agentic AI (Cd14526) – Course 1
level: 300 / Graduate
type: lecture-notes
status: review
created: 2026-09-28
prerequisites:
  - "[[Orchestrator-Workers Workflow]]"
  - "[[Implementing Routing Workflow]]"
  - "[[Implementing Parallelization Workflow]]"
related:
  - "[[Agentic Workflow Patterns]]"
  - "[[Implementing Agentic Workflows in Python]]"
  - "[[Gate Checks]]"
  - "[[Pydantic for Structured LLM Output - Study Guide]]"
  - "[[Runtime or Orchestration Layer]]"
  - "[[Prompt Injection]]"
tags:
  - agentic-ai/workflows/patterns/orchestrator-workers
  - agentic-ai/workflows/implementation
  - python
  - agentic-ai
  - lecture-notes
---

# Implementing Orchestrator-Workers Workflow

> [!abstract] TL;DR
> Two scripts implement the pattern with the same skeleton. The **demo** (`demo_orchestrator.py`) plans building-permit research for a pool with zoning, site-plan, and generic workers. The **exercise solution** (`solution.py`) plans a lab-report interpretation with hematology, renal, and liver workers. In both, an `Orchestrator` asks an LLM for an XML plan, `parse_tasks` turns it into task dicts, `get_worker` maps each task type to a worker class, and workers run **one after another**. The structure teaches the pattern well. Testing, though, showed that ==the task parser mangles every description and silently drops tasks written on one line==, worker matching is substring-based, the solution ==drops unmatched tasks without telling anyone==, and ==neither script actually synthesizes==: both print the worker outputs one after another. The improved version adds a worker registry the orchestrator can see, a JSON plan, parallel workers, failure reporting, and a real synthesis step. An extension adds a ==code-only plan gate with one retry==, explicit run statuses, and ==dependency waves== for subtasks that need each other's output.

**Section:** [[Agentic Workflow Patterns]] – pattern 5 of 5 (implementation)
**Previous:** [[Orchestrator-Workers Workflow]] (theory)
**Related:** [[Implementing Routing Workflow]] (the same substring-dispatch problem) · [[Implementing Parallelization Workflow]] (the same `ThreadPoolExecutor` fix) · [[Implementing Agentic Workflows in Python]] (the definitions / instantiation / workflow split)

**Sources:** Course demo and exercise solution, stored in the vault at `python notebooks/Orchestrator-Workers Pattern/demo_orchestrator.py` and `…/solution.py`, plus the course's code walkthrough reading (the general-contractor analogy, summarized in [[#4. Code Principles Review]]). The tests, the improved version, the plan-gate and dependency extension (merged from an earlier version of this note), the lab range checker, and the critical analysis are *beyond the lecture*. All tests used a fake OpenAI client; nothing here was run against the live API.

> [!todo]- Contents
> 1. [[#1. Setup]]
> 2. [[#2. The Two Scripts]]
> 3. [[#3. Code Walkthrough]]
> 4. [[#4. Code Principles Review]]
> 5. [[#5. Review Against the Theory]]
> 6. [[#6. Testing the Helpers]]
> 7. [[#7. Improved Version]]
> 8. [[#8. Deterministic Checks for the Lab Exercise]]
> 9. [[#9. Cost and Latency]]
> 10. [[#10. Pitfalls and Failure Modes]]
> 11. [[#11. Key Takeaways]]
> 12. [[#12. Critical Analysis]]
> 13. [[#13. Self-Test]]
> 14. [[#14. Glossary]]

---

## 1. Setup

Same environment as [[Implementing Prompt Chaining Workflow#1. Setup]]. Both scripts use `gpt-4` through an `llm_call(prompt)` wrapper with a generic system message ("You are a helpful assistant."), so each role lives entirely in the user prompt. Temperature is `0.3` in the demo and `0.2` in the solution. They also use `re` for tag extraction and `typing` for hints (`Optional` is imported but unused).

---

## 2. The Two Scripts

| | Demo: `demo_orchestrator.py` | Exercise solution: `solution.py` |
|---|---|---|
| Domain | Pool permits in The Woodlands, Texas | Interpreting a patient lab report |
| Orchestrator persona | Permitting expert: "break it into permitting-related subtasks" | Clinical lab data analyst: "one task for each major panel" |
| Plan size | 2–4 tasks | One task per panel found in the data |
| Workers | `ZoningAgent`, `SitePlanAgent`, `GenericAgent` | `HematologyAgent`, `RenalFunctionAgent`, `LiverFunctionAgent` |
| Unmatched task type | → `GenericAgent` (handyman) | → `ValueError`, caught, printed, ==task dropped== |
| Worker reply without `<response>` tag | Falls back to the raw reply (with a warning) | ==Returns an empty string== |
| What's dynamic | The plan depends on the kind of project | The plan depends on which panels are in the data |

^two-scripts

Both scripts share `llm_call`, `extract_xml`, `parse_tasks`, the `WorkerAgent` base class, and the same `Orchestrator.process` structure.

---

## 3. Code Walkthrough

### 3.1 The plan – an XML contract

```python
orchestrator_prompt = """
You are a permitting expert. Your job is to analyze a high-level construction request
and break it into permitting-related subtasks.
<analysis>
Provide an overall explanation of what steps are involved.
</analysis>
<tasks>
Provide 2–4 <task> entries with a <type> and <description>. Use this format:
<task>
  <type>zoning</type>
  <description>Verify land is zoned for commercial use.</description>
</task>
</tasks>
Task: {task}
"""
```

The orchestrator is asked for two things: a free-text `<analysis>` and a machine-readable `<tasks>` list. This is the ==plan as structured data== idea from [[Orchestrator-Workers Workflow#3. Orchestration – Dynamic Decomposition and Delegation]], using XML-style tags.

### 3.2 Parsing the plan

```python
def extract_xml(text, tag):                      # first <tag>...</tag> block, or ""
    match = re.search(rf"<{tag}>(.*?)</{tag}>", text, re.DOTALL)
    return match.group(1).strip() if match else ""

def parse_tasks(xml):                            # line-by-line parser
    for line in xml.splitlines():
        line = line.strip()
        if line.startswith("<task>"):          current_task = {}
        elif line.startswith("<type>"):        current_task["type"] = line[6:-7].strip()
        elif line.startswith("<description>"): current_task["description"] = line[12:-13].strip()
        elif line.startswith("</task>"):       ...append if it has a description; default type "default"
```

(Condensed.) The parser assumes each tag sits **on its own line, exactly as in the example**. See [[#6. Testing the Helpers]] for what happens otherwise.

### 3.3 Workers – one class per specialty

```python
class WorkerAgent:
    def __init__(self, task_type): self.task_type = task_type
    def run(self, original_task, task_description): raise NotImplementedError

class ZoningAgent(WorkerAgent):
    def run(self, original_task, task_description):
        prompt = f"""You are a zoning permit expert.
Main Task: {original_task}
Subtask Type: {self.task_type}
Subtask Description: {task_description}
<response>
- Explain the purpose of this step.
- Describe required documents or portals.
- Note any blockers like zoning conflicts or variances.
</response>"""
        raw_output = llm_call(prompt)
        result = extract_xml(raw_output, "response")
        return result or raw_output            # demo: fall back to the raw reply (with a warning)
```

Every worker receives **both** the original task and its subtask description, so it knows the big picture ([[Prompt Chaining Workflow#^context-management|contextual reiteration]]). The `<response>` block in the prompt doubles as instructions and output format.

### 3.4 Delegation and the main loop

```python
def get_worker(self, task_type):
    t = task_type.lower()
    if "zoning" in t:   return ZoningAgent(task_type)
    elif "site" in t:   return SitePlanAgent(task_type)
    else:               return GenericAgent(task_type)

def process(self, task):
    response = llm_call(self.orchestrator_prompt.format(task=task))    # 1. plan
    analysis = extract_xml(response, "analysis")
    tasks = parse_tasks(extract_xml(response, "tasks"))
    results = []
    for task_info in tasks:                                            # 2. delegate, one at a time
        agent = self.get_worker(task_info["type"])
        results.append({**task_info, "result": agent.run(task, task_info["description"])})
    return {"analysis": analysis, "worker_results": results}           # 3. return the pieces
```

(Condensed.) The `__main__` block then prints the analysis followed by each worker's result under a heading.

---

## 4. Code Principles Review

### 4.1 The general-contractor analogy

The course's walkthrough explains the code as a **general contractor building a house**:

| Analogy | Code | Role |
|---|---|---|
| General contractor | `Orchestrator` class | Understands the big picture, makes the plan, delegates |
| Project plan / to-do list | The `<tasks>` list from the planning LLM call | What needs doing for *this* request |
| Contact list | `get_worker()` | Finds the right specialist for each job |
| Specialist subcontractors | `ZoningAgent`, `SitePlanAgent` (demo); `HematologyAgent`, `RenalFunctionAgent`, `LiverFunctionAgent` (solution) | Each has expertise defined by its prompt |
| Reliable handyman | `GenericAgent` | Handles anything else |
| Final package | The returned dict / printed report | All the specialists' reports together |

^contractor-analogy

The walkthrough's four steps:

1. **The plan is made:** the orchestrator uses its LLM to turn the request into a to-do list (e.g. a "zoning" task and a "site plan" task).
2. **The work is delegated:** for the first item, `get_worker` finds the specialist, and the orchestrator hands over the specific task.
3. **The job gets done:** the specialist reports its findings; the orchestrator moves to the next item.
4. **The final report:** the orchestrator gathers all reports "into one neat, final package."

The walkthrough stresses that ==the planning step is dynamic==: a kitchen remodel would produce a different plan from a pool. That is what makes it agentic rather than a fixed pipeline.

### 4.2 Principles and how the code applies them

| # | Principle | How the scripts do it | Verdict | Better |
|---|---|---|---|---|
| 1 | **Separate planning from doing** | Orchestrator plans; workers execute; the orchestrator never does a subtask itself | ✅ | – |
| 2 | **Plan as a structured contract** | XML tags parsed by a fragile line parser | ⚠️ | JSON plan validated with a schema ([[Pydantic for Structured LLM Output - Study Guide]]) |
| 3 | **Common worker interface** | `WorkerAgent.run(original_task, task_description)` base class | ✅ | – |
| 4 | **Specialization by prompt** | Each worker's expertise is its prompt | ✅ | One configurable `Worker` class instead of near-identical subclasses |
| 5 | **The orchestrator knows its team** | The planning prompt ==doesn't list the available worker types==; the LLM guesses type names | ❌ | Put the worker registry in the planning prompt |
| 6 | **Deterministic delegation** | Substring checks on free-text types | ⚠️ | Exact match on a closed set, then fallback ([[Implementing Routing Workflow#^dispatch-test]]) |
| 7 | **Give workers the big picture** | Original task + subtask description | ✅ | – |
| 8 | **Graceful fallback** | Demo: `GenericAgent`. Solution: drop the task | ⚠️ | Fallback worker, or report the gap explicitly |
| 9 | **Synthesis** | ==None==: results are printed one after another | ❌ | A synthesis LLM call that connects, reconciles, and structures the findings |
| 10 | **Independent workers run concurrently** | Sequential `for` loop | ⚠️ | `ThreadPoolExecutor` ([[Implementing Parallelization Workflow#6. Improved Version]]) |
| 11 | **Observability** | Prints the raw orchestrator output and each result | ⚠️ | `logging` with task IDs; keep the plan with the results |

^code-principles

> [!important] The biggest gap
> The theory says synthesis is "more than just stapling pages together" ([[Orchestrator-Workers Workflow#^def-synthesis]]). The walkthrough's step 4 ("one neat, final package") and both scripts' output are exactly that: stapled pages. ==The orchestrator does half its job.==

---

## 5. Review Against the Theory

| Theory element ([[Orchestrator-Workers Workflow]]) | In the scripts | Verdict |
|---|---|---|
| Orchestrator analyzes the task | `<analysis>` section | ✅ |
| Dynamic decomposition at runtime | LLM plan varies with the request / data | ✅ |
| Delegation to the most suitable worker | `get_worker` substring matching | ⚠️ |
| Specialized workers | Prompt-defined specialists + generic (demo) | ✅ |
| Synthesis into one coherent output | Not implemented; outputs listed | ❌ |
| Workers may run in parallel | Sequential | ⚠️ |

---

## 6. Testing the Helpers

*Beyond the lecture.* I loaded both scripts with a fake OpenAI client and tested the helpers directly.

| # | Test | Result | Problem |
|---|---|---|---|
| 1 | `parse_tasks` on the **exact format from the prompt's own example** | `description = '>Verify land is zoned for residential pools.<'` | ==Off-by-one slice==: `<description>` is 13 characters, not 12, so every description keeps a stray `>` and `<` |
| 2 | Description wrapped over two lines | `description = '>Prepare a site plan sho'` | The slice assumes the closing tag is on the same line; the text is cut short |
| 3 | Whole `<task>` on one line | `[]`: no tasks | ==Plan silently empty==; the report would contain only the analysis |
| 4 | Demo `get_worker("HOA approval")`, `("building permit")` | `GenericAgent` | Fine: the handyman fallback works |
| 5 | Demo `get_worker("website update")` | `SitePlanAgent` | Substring `"site"` in "website" |
| 6 | Solution `get_worker("CBC")`, `("metabolic panel")` | `ValueError` → task dropped | "CBC" is the panel's common name and appears in the prompt's own example description |
| 7 | Worker reply without `<response>` tags | Demo: raw reply used. Solution: `''` | Solution ==returns empty findings== with no warning |
| 8 | Full solution run with a plan containing a `CBC` task and a `renal` task | Report contains only `renal` | ==The hematology panel silently disappears== from the final report |

^helper-tests

> [!danger] Why test 8 matters
> In the lab exercise the CBC panel has two abnormal values (high WBC, low platelets). A plan that labels the task "CBC" makes those findings vanish from the report, and the only sign is an `--- ERROR ---` line in the console. That's the same "silent partial result" failure found in [[Implementing Parallelization Workflow#^thread-failure-test]].

A fixed slice for the description would be `line[len("<description>"):-len("</description>")]`. But the real fix is not to hand-parse XML line by line at all: ask for JSON and parse it with `json.loads`, or use a regex over the whole `<tasks>` block.

---

## 7. Improved Version

*Beyond the lecture.* Changes, mapped to the principles in [[#^code-principles]]:

- **One configurable `Worker` class** (principle 4); the team is a list of configurations.
- **Worker registry in the planning prompt** (principle 5): the orchestrator may use ==only== the listed types.
- **JSON plan**, parsed with `json.loads`, capped at `max_tasks` (principle 2).
- **Exact-match delegation after normalization**, then a fallback worker or an explicit problem entry (principles 6 and 8).
- **Parallel workers** with per-task error capture (principle 10).
- **A real synthesis step** that is told which subtasks were not completed (principle 9).

```python
import json
import logging
from concurrent.futures import ThreadPoolExecutor

log = logging.getLogger("orchestrator")

class Worker:
    """A specialist defined by configuration, not a subclass per specialty."""
    def __init__(self, task_type, role, focus):
        self.task_type, self.role, self.focus = task_type, role, focus

    def run(self, original_task, description):
        return llm_call(
            f"Main task:\n{original_task}\n\nYour subtask ({self.task_type}): {description}\n\n{self.focus}",
            system=f"You are {self.role}. Answer only your subtask.")

class Orchestrator:
    def __init__(self, workers, fallback=None, max_tasks=6):
        self.workers = {w.task_type: w for w in workers}      # capability registry
        self.fallback, self.max_tasks = fallback, max_tasks

    def plan(self, task):
        menu = "\n".join(f"- {w.task_type}: {w.role}" for w in self.workers.values())
        raw = llm_call(
            f"Break the task into 1-{self.max_tasks} independent subtasks.\n"
            f"Use ONLY these worker types:\n{menu}\n\n"
            'Return JSON: {"analysis": str, "tasks": [{"type": str, "description": str}]}\n\n'
            f"<task>\n{task}\n</task>",
            system="You are an orchestrator. You plan and delegate; you do not do the subtasks.",
            json_mode=True)
        plan = json.loads(raw)
        tasks = plan.get("tasks", [])
        if not tasks:
            raise ValueError("Orchestrator produced no subtasks")
        return plan.get("analysis", ""), tasks[: self.max_tasks]

    def get_worker(self, task_type):
        return self.workers.get(task_type.strip().lower(), self.fallback)   # exact match, then fallback

    def process(self, task):
        analysis, tasks = self.plan(task)
        results, problems = [], []
        with ThreadPoolExecutor(max_workers=len(tasks)) as pool:          # workers are independent
            jobs = []
            for t in tasks:
                worker = self.get_worker(t["type"])
                if worker is None:
                    problems.append({**t, "error": "no worker for this type"})
                    continue
                jobs.append((t, pool.submit(worker.run, task, t["description"])))
            for t, job in jobs:
                try:
                    results.append({**t, "result": job.result(timeout=120)})
                except Exception as exc:
                    problems.append({**t, "error": repr(exc)})
        report = self.synthesize(task, analysis, results, problems)
        return {"analysis": analysis, "worker_results": results, "problems": problems, "report": report}

    def synthesize(self, task, analysis, results, problems):
        findings = "\n\n".join(f"[{r['type']}] {r['description']}\n{r['result']}" for r in results)
        gaps = "\n".join(f"- {p['type']}: {p['error']}" for p in problems) or "none"
        return llm_call(
            f"<task>\n{task}\n</task>\n\nPLAN SUMMARY: {analysis}\n\nWORKER FINDINGS:\n{findings}\n\n"
            f"SUBTASKS NOT COMPLETED:\n{gaps}\n\n"
            "Write one coherent answer to the task: introduction, one section per theme, conclusion. "
            "Connect related findings across workers, resolve or flag contradictions, "
            "and state clearly which parts could not be covered.",
            system="You are the orchestrator synthesizing your team's work.")
```

`llm_call(prompt, system, temperature, json_mode)` extends the scripts' wrapper with a system message and `response_format={"type": "json_object"}` for the plan. Setting up the demo's team:

```python
team = [Worker("zoning", "a zoning permit expert",
               "Explain the purpose, required documents or portals, and blockers such as variances."),
        Worker("site_plan", "a site planning advisor",
               "Explain what's involved, required drawings and approvals, and who reviews them.")]
orchestrator = Orchestrator(team, fallback=Worker("generic", "a permitting assistant",
                                                 "Describe the subtask, how to do it, and challenges."))
```

### 7.1 Test run with a fake LLM

The fake orchestrator returns a plan with three tasks: `zoning`, `"Site_Plan "` (odd case and a trailing space), and `hoa` (no specialist). Each worker call sleeps 0.3 s.

| Configuration | Worker results | Problems | Synthesis told about gaps | Time | LLM calls |
|---|---|---|---|---|---|
| No fallback | zoning, Site_Plan | ==hoa: no worker for this type== | yes | 0.30 s | 4 |
| Generic fallback | zoning, Site_Plan, hoa | none | n/a | 0.30 s | 5 |

^orch-fake-test

The test also checked that the planning prompt contained the worker list. What this shows:
- Normalization handles odd casing and spacing.
- A missing specialist becomes a ==visible problem entry passed to the synthesizer==, not a silent drop.
- Three workers finished in the time of one (parallel).

### 7.2 Extension – Plan Gate, Run Statuses, and Dependency Waves

*Beyond the lecture.* Three further additions, merged in from an earlier version of this note:

| Addition | What it does | Why |
|---|---|---|
| **Plan gate** | `validate_plan()` is pure code that accepts or rejects the orchestrator's plan: valid JSON, 1–`max_tasks` subtasks, unique ids, known worker types, non-empty descriptions, valid dependencies, no cycles. `plan()` re-prompts **once** with the specific error; after two failures it gives up | The plan is the single point of failure ([[Orchestrator-Workers Workflow#^ow-reliability]]), so it gets a [[Gate Checks\|gate]] before any worker runs |
| **Run statuses** | `ok`, `partial` (some subtasks failed or were skipped), `plan_failed` (no worker or synthesis calls made), `all_workers_failed` (no synthesis) | Callers can tell a full answer from a partial one or a failure, instead of reading a report that hides gaps |
| **Dependency waves** | Each subtask may list `depends_on` ids. Subtasks are grouped into **waves**: each wave depends only on earlier ones. Waves run in order, subtasks within a wave run in parallel, and each worker gets its dependencies' outputs in its prompt | The basic version runs every subtask blind. Real plans often need order ("budget after venues and travel"), which makes the plan a [[Directed Acyclic Graph (DAG)]] |

^plan-gate-extension

```python
def validate_plan(raw, allowed_types, max_tasks=6):
    """Plan gate: pure code. Returns (tasks, None) or (None, error message)."""
    try:
        plan = json.loads(raw)
    except json.JSONDecodeError as exc:
        return None, f"Not valid JSON ({exc.msg}). Return JSON only, no prose."
    tasks = plan.get("tasks") if isinstance(plan, dict) else None
    if not tasks:
        return None, 'Missing or empty "tasks" list.'
    if len(tasks) > max_tasks:
        return None, f"{len(tasks)} subtasks; the maximum is {max_tasks}."
    ids = [t.get("id") for t in tasks]
    if len(set(ids)) != len(ids) or None in ids:
        return None, "Every subtask needs a unique id."
    for t in tasks:
        if t.get("type", "").strip().lower() not in allowed_types:
            return None, f"Subtask {t['id']}: unknown type {t.get('type')!r}. Allowed: {sorted(allowed_types)}."
        if not t.get("description", "").strip():
            return None, f"Subtask {t['id']}: empty description."
        missing = set(t.get("depends_on", [])) - set(ids)
        if missing:
            return None, f"Subtask {t['id']}: depends_on unknown ids {sorted(missing)}."
    if waves(tasks) is None:
        return None, "depends_on contains a cycle."
    return tasks, None

def waves(tasks):
    """Group subtasks into waves: each wave depends only on earlier waves. None if there's a cycle."""
    remaining = {t["id"]: set(t.get("depends_on", [])) for t in tasks}
    done, result = set(), []
    while remaining:
        ready = [i for i, deps in remaining.items() if deps <= done]
        if not ready:
            return None                                   # nothing can run: cycle
        result.append(ready)
        done.update(ready)
        for i in ready:
            del remaining[i]
    return result
```

`plan()` asks for `{"analysis": str, "tasks": [{"id", "type", "description", "depends_on"}]}` and retries once:

```python
def plan(self, task, max_attempts=2):
    prompt = build_plan_prompt(task, self.workers, self.max_tasks)   # registry + JSON schema, as in 7
    for attempt in range(1, max_attempts + 1):
        raw = llm_call(prompt, system="You are an orchestrator. You plan and delegate.", json_mode=True)
        tasks, error = validate_plan(raw, set(self.workers), self.max_tasks)
        if tasks:
            return json.loads(raw).get("analysis", ""), tasks
        prompt += f"\n\nYour previous plan was rejected: {error}\nReturn a corrected plan."
    return None, None                                               # → status "plan_failed"
```

`process()` then runs wave by wave:

```python
def process(self, task):
    analysis, tasks = self.plan(task)
    if tasks is None:
        return {"status": "plan_failed", "results": {}, "problems": {}, "report": None}
    by_id = {t["id"]: t for t in tasks}
    results, problems = {}, {}
    for wave in waves(tasks):                                    # waves run in order...
        with ThreadPoolExecutor(max_workers=len(wave)) as pool:  # ...a wave's subtasks run in parallel
            jobs = {}
            for i in wave:
                t = by_id[i]
                failed_deps = [d for d in t.get("depends_on", []) if d not in results]
                if failed_deps:
                    problems[i] = f"skipped: depends on failed {failed_deps}"
                    continue
                context = "".join(f"OUTPUT OF {d}:\n{results[d]}\n\n" for d in t.get("depends_on", []))
                worker = self.workers[t["type"].strip().lower()]
                jobs[i] = pool.submit(worker.run, task, t["description"], context)
            for i, job in jobs.items():
                try:
                    results[i] = job.result(timeout=120)
                except Exception as exc:
                    problems[i] = repr(exc)                      # one failure marks one subtask
    if not results:
        return {"status": "all_workers_failed", "results": {}, "problems": problems, "report": None}
    report = self.synthesize(task, analysis, results, problems)  # told what's missing, as in 7
    return {"status": "partial" if problems else "ok", "results": results,
            "problems": problems, "report": report}
```

(`Worker.run` gains a `context` argument that is inserted before the worker's focus instructions.)

#### Test run with a fake LLM

Team: `venues`, `travel`, `budget`. Each worker call sleeps 0.2 s.

| Scenario | Status | LLM calls | Time | Notes |
|---|---|---|---|---|
| Valid plan: venues, travel, then budget `depends_on` both | `ok` | 5 | 0.4 s | Two waves; the budget prompt contained both `OUTPUT OF v` and `OUTPUT OF t` |
| First plan is chatty prose around the JSON ("Sure! Here is the plan: …"), second is valid | `ok` | 6 | 0.4 s | ==Gate rejected it; one retry fixed it== |
| Plan uses unknown type `catering`, twice | `plan_failed` | 2 | 0.0 s | No worker or synthesis calls made |
| Plan with `a → b → a` | rejected | – | – | Gate message: "depends_on contains a cycle." |
| Travel worker raises an error | `partial` | 4 | 0.2 s | Budget ==skipped: depends on failed `t`==; synthesis told both |
| Both workers fail | `all_workers_failed` | 3 | 0.2 s | No synthesis call |

^plan-gate-test

Latency with waves: $T = t_{\text{plan}} + \sum_{w} \max_{i \in w} t_i + t_{\text{synth}}$, so each wave adds only its slowest subtask. With no dependencies there is one wave, and latency is roughly independent of the number of subtasks while cost still grows linearly with it.

> [!note] What these tests can't show
> A fake LLM checks the control flow, not the **plan quality**: whether the orchestrator picks sensible, complete, non-overlapping subtasks. That needs a labeled set of requests with expected subtasks, run against a live model ([[LLM Evaluation]]).

---

## 8. Deterministic Checks for the Lab Exercise

*Beyond the lecture; a study aid, not medical advice.* Whether a value is outside its reference range is **arithmetic**, not interpretation. It can be computed in code and handed to the workers, so the LLM only explains significance.

```python
import re

LINE = re.compile(r"-\s*(?P<name>[^:]+):\s*(?P<value>[\d.]+)\s*(?P<unit>\S+)\s*"
                  r"\(Normal:\s*(?P<lo>[\d.]+)-(?P<hi>[\d.]+)\)")

def flag_out_of_range(text):
    flags = []
    for m in LINE.finditer(text):
        v, lo, hi = float(m["value"]), float(m["lo"]), float(m["hi"])
        status = "LOW" if v < lo else "HIGH" if v > hi else "normal"
        flags.append((m["name"].strip(), v, m["unit"], status))
    return flags
```

Output on the exercise's lab data (tested):

| Panel | Test | Value | Range | Flag |
|---|---|---|---|---|
| CBC | WBC | 11.5 ×10⁹/L | 4.5–11.0 | **HIGH** |
| CBC | RBC | 4.6 ×10¹²/L | 4.2–5.4 | normal |
| CBC | Platelets | 140 ×10⁹/L | 150–450 | **LOW** |
| Renal | Creatinine | 1.4 mg/dL | 0.6–1.2 | **HIGH** |
| Renal | BUN | 25 mg/dL | 7–20 | **HIGH** |
| Liver | ALT | 55 U/L | 7–56 | normal (near the upper limit) |
| Liver | AST | 60 U/L | 10–40 | **HIGH** |

^lab-flags

This table doubles as an **evaluation checklist**: a correct report must mention all five abnormal values and must *not* call ALT abnormal. It's a precise, automatic test of the orchestrator plus workers ([[LLM Evaluation]]).

---

## 9. Cost and Latency

| Version | LLM calls | Latency |
|---|---|---|
| Original (demo, 2–4 tasks) | $1 + n$ (3–5) | $t_{\text{plan}} + \sum_i t_i$ (sequential) |
| Improved | $1 + n + 1$ | $t_{\text{plan}} + \max_i t_i + t_{\text{synth}}$ |

Example with 3 workers at 10 s, planning 8 s, synthesis 12 s: original $8 + 30 = 38$ s (no synthesis); improved $8 + 10 + 12 = 30$ s, *with* a synthesized report. Adding the synthesis step costs one call; running the workers in parallel more than pays for it.

---

## 10. Pitfalls and Failure Modes

| Failure | Symptom | Mitigation |
|---|---|---|
| Hand-written line parser for the plan | Mangled descriptions; tasks silently missing | JSON plan + `json.loads` + schema validation |
| Invalid plan passed to workers | Unknown types, duplicate ids, or chatty prose break dispatch | Code-only plan gate; one retry with the specific error; `plan_failed` status |
| Dependent subtasks run blind | "Budget" written without the venue or travel results | `depends_on` + dependency waves; pass dependency outputs into the prompt |
| Cyclic dependencies | Nothing can start, or the run hangs | Cycle check in the plan gate |
| Orchestrator doesn't know the team | Plans use types no worker handles | Registry in the planning prompt; closed set of types |
| Substring delegation | "website" → site plan worker | Exact match after normalization |
| Unmatched tasks dropped | Report missing a whole section | Fallback worker, or report the gap to the synthesizer and the user |
| Missing `<response>` tag → empty result | Blank findings | Fall back to the raw reply, or re-prompt; never return `""` silently |
| No synthesis | Output reads as separate memos | Explicit synthesis call |
| Sequential workers | Latency grows with the number of tasks | `ThreadPoolExecutor` |
| LLM does arithmetic | Wrong high/low flags on lab values | Compute flags in code; the LLM interprets |
| Medical or legal output treated as advice | Users act on unreviewed interpretations | Clear framing; professional review |
| Task text steering the plan | Injected instructions create unexpected subtasks | Delimit the task as data; closed worker set; least-privilege workers |

---

## 11. Key Takeaways

- [ ] I can map the `Orchestrator`, `get_worker`, and worker classes to the general-contractor analogy.
- [ ] I can explain the four-step flow: plan, delegate, execute, final report.
- [ ] I can compare the demo and the solution (domain, fallback, missing-tag behavior).
- [ ] I can explain the off-by-one bug in `parse_tasks` and why JSON is a better plan format.
- [ ] I can explain why the orchestrator should see the worker registry.
- [ ] I can show that neither script synthesizes, and write a synthesis step that reports gaps.
- [ ] I can run independent workers in parallel and collect failures.
- [ ] I can move deterministic parts (range flags) out of the LLM.
- [ ] I can write a code-only plan gate and retry the plan once with its error message.
- [ ] I can name the four run statuses and when each is returned.
- [ ] I can group subtasks into dependency waves and detect cycles.

---

## 12. Critical Analysis

- **The skeleton is the right one.** Plan → delegate → execute → assemble, with a common worker interface and prompt-defined specialists, is the standard shape of this pattern. The exercise teaches it clearly, and the generic fallback in the demo is good design.
- **The weak points are all at the contracts between LLM and code**: the plan format, the type names, and the response tags. This is the same lesson found in every implementation in this section ([[Implementing Routing Workflow]], [[Implementing Evaluator-Optimizer Workflow]]): ==wherever code acts on LLM text, use structured output, a closed vocabulary, and explicit failure handling==.
- **How dynamic is it really?** The lab solution's plan is essentially "one task per panel". A regex could find the panels, and a fixed set of workers could handle them. That is parallelization with routing, not open-ended orchestration. It's still a useful exercise, but the pattern earns its cost only when the subtasks can't be predicted, as in the permit demo, where different projects need different permits.
- **Domain risk:** permit rules are local and change. An LLM without access to municipal codes will produce plausible but possibly outdated requirements, so the output should point users to the official permit office. Lab interpretation is clinical territory: flags can be computed, but significance and next steps belong to a clinician.
- **How to evaluate it:** for the lab exercise, the flag table in [[#^lab-flags]] gives exact checks. For the permit demo, check the plan's coverage against a human-written list of required permits for a few sample projects, and check that the final answer cites the responsible office.
- **Security:** the task text (a user's request, or lab data from another system) is inserted directly into the orchestrator prompt, so it can try to steer the plan. With a closed worker registry, the worst an injected plan can do is misuse existing workers. That's why each worker should hold only the tools and data it needs ([[Prompt Injection]]).

> [!question] Discussion questions
> 1. Should the lab orchestrator be an LLM at all, given that panels can be found with code? Where would an LLM planner genuinely help in that domain?
> 2. How would you let a worker ask the orchestrator for clarification or report that its subtask was badly specified?
> 3. What should the synthesizer do if two workers' findings contradict each other?

---

## 13. Self-Test

> [!question]- Q1. In the general-contractor analogy, what do `Orchestrator`, `get_worker`, the specialist agents, and `GenericAgent` correspond to?
> The general contractor; the contact list; the specialist subcontractors; the reliable handyman who handles anything else.

> [!question]- Q2. What are the four steps of the workflow in the code walkthrough?
> The plan is made (LLM creates the to-do list), the work is delegated (`get_worker` picks a specialist per task), the jobs get done (each worker runs its task), and the final report is assembled from all the workers' outputs.

> [!question]- Q3. Why does every parsed description start with `>` and end with `<`?
> `parse_tasks` slices `line[12:-13]`, but `<description>` is 13 characters and `</description>` is 14. The slice starts one character too early and ends one character too late.

> [!question]- Q4. How do the demo and the solution handle a task type with no matching specialist?
> The demo sends it to `GenericAgent`. The solution raises `ValueError`, catches it, prints an error, and drops the task, so that section is missing from the report.

> [!question]- Q5. What part of the theory do both scripts leave out, and how would you add it?
> Synthesis. Both just list the worker outputs. Add a final LLM call that receives the original task, the plan summary, all worker findings, and any failed subtasks, and writes one coherent answer that connects findings and states what couldn't be covered.

> [!question]- Q6. (Quantitative) Planning takes 6 s, four workers take 9, 12, 7, and 10 s, and synthesis takes 11 s. Compare the original's latency (no synthesis) with the improved version's.
> Original: $6 + 9 + 12 + 7 + 10 = 44$ s. Improved: $6 + \max(9, 12, 7, 10) + 11 = 29$ s, and it includes a synthesized report.

> [!question]- Q7. (Design) Adapt the improved orchestrator for the lab exercise so abnormal values can never be missed.
> Run `flag_out_of_range` in code first and pass each panel's flags to its worker. Register workers for `hematology`, `renal`, and `liver`, with aliases such as `cbc` mapping to hematology. Use a generic fallback for unknown panels. After synthesis, check automatically that every HIGH/LOW flag appears in the report, and re-prompt the synthesizer if one is missing. Frame the output as information for a clinician, not advice.

> [!question]- Q8. (Design) A plan has subtasks A and B with no dependencies, C depending on A, and D depending on B and C. What are the waves, and what happens if B fails?
> Waves: [A, B] → [C] → [D]. If B fails, C still runs (it needs only A), but D is skipped because one of its dependencies failed. The run ends as `partial`, and the synthesizer is told that B failed and D was skipped.

### Flashcards

> [!tip] Flashcards
> Review cards for this note are in [[Implementing Orchestrator-Workers Workflow - Flashcards]].

---

## 14. Glossary

| Term | Meaning |
|---|---|
| `Orchestrator` | Class that plans with an LLM, delegates tasks, and collects results |
| `parse_tasks` | Line-based parser turning `<task>` XML into dicts |
| `extract_xml` | Regex helper returning the first `<tag>…</tag>` block |
| `WorkerAgent` | Base class defining `run(original_task, task_description)` |
| `get_worker` | The "contact list": maps a task type to a worker instance |
| `GenericAgent` | Fallback worker for task types without a specialist |
| Worker registry | The set of available worker types, shown to the orchestrator |
| Synthesis step | Final LLM call that combines worker findings into one answer |
| Off-by-one error | An index or slice that is one position too early or too late |
| Plan gate | Pure-code check that accepts or rejects the orchestrator's plan before dispatch |
| Run status | `ok`, `partial`, `plan_failed`, or `all_workers_failed` |
| `depends_on` | List of subtask ids whose outputs a subtask needs |
| Dependency wave | A group of subtasks whose dependencies are all complete; waves run in order |

---

## Further Reading

- [Building Effective Agents (Anthropic)](https://www.anthropic.com/research/building-effective-agents) – orchestrator-workers workflow
- [Python `concurrent.futures`](https://docs.python.org/3/library/concurrent.futures.html)
- [OpenAI – Structured outputs / JSON mode](https://platform.openai.com/docs/guides/structured-outputs)

%% Study hint: the contractor analogy covers plan → delegate → do → package. The review adds the missing steps: tell the contractor who's on the team, and have them actually write the final report instead of stapling the subcontractors' notes together. %%
