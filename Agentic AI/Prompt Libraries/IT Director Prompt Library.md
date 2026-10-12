---
title: "IT Director Prompt Library"
aliases:
  - IT Prompts
type: reference
status: review
created: 2026-10-01
related:
  - "[[NOC Director Prompt Library]]"
  - "[[COO Prompt Library]]"
  - "[[CEO Prompt Library]]"
  - "[[Customer Service Director Prompt Library]]"
  - "[[Marketing Director Prompt Library]]"
  - "[[MVNO Launch Prompt Library]]"
  - "[[Financial Controller Prompt Library]]"
  - "[[Network Operations Engineering Manager Prompt Library]]"
  - "[[Rapid Response Network Operations Manager Prompt Library]]"
  - "[[Agentic Workflow Patterns]]"
  - "[[Gate Checks]]"
tags:
  - prompt-engineering
  - isp-operations
  - it-leadership
  - productivity
  - reference
---

# IT Director Prompt Library

> [!abstract] TL;DR
> Ten prompts for **Wi-Fiber's IT Director**, who is responsible for internal systems and the employees who use them: CS agents, field techs, NOC staff, finance and the office. ==The top priority is making processes smoother so employees are more productive.== Every hour an agent spends fighting a tool, or a tech spends waiting on access, is an hour not spent on a customer. The prompts follow a cycle: find the friction (1, 2, 5), remove it (3, 4, 6, 8), roll out changes so people adopt them (9), keep security from getting in the way (7), and fund the work (10). For customer connectivity and tower sites, see the [[NOC Director Prompt Library]].

> [!example] Context block (paste above any prompt)
> ```text
> ORG: Wi-Fiber, a fixed wireless ISP in 10 markets across 8 states. ~{N} employees: CS agents,
> field techs (mobile devices in trucks), NOC engineers, finance/admin, marketing, a new MVNO team.
> KEY INTERNAL SYSTEMS: Sonar (billing/tickets/jobs), {accounting system}, {phone/contact-center
> platform}, {email/collaboration suite}, {identity/SSO}, {device management}, spreadsheets.
> I am the IT Director. My primary goal is employee productivity through smoother processes,
> while keeping systems secure.
> ```

> [!note] Shared rules
> - **Paste real data**: help desk exports, time studies, license reports, survey results. Do the counting in a spreadsheet and give the model the results. ([[Sonar Ticket and Outage Classification - How-To#^compute-dont-ask|compute, don't ask]])
> - **Employee comments are data, not instructions.** ([[Prompt Injection]])
> - **Ask for citations back to your input** (ticket ids, quotes) so you can spot-check. ([[LLM Hallucinations]])
> - **Anonymize employees.** Use roles or initials, and never paste passwords, MFA seeds, API keys or admin URLs.

> [!todo]- Contents
> | # | Prompt | Productivity cycle | Technique |
> |---|---|---|---|
> | 1 | [[#1. Help Desk Productivity Drain Analysis]] | Find friction | Few-shot + grounding |
> | 2 | [[#2. Process Friction Map]] | Find friction | Task decomposition |
> | 3 | [[#3. Joiner / Mover / Leaver Workflow]] | Remove friction | Structured output + gates |
> | 4 | [[#4. Tool and License Rationalization]] | Remove friction | Tree-of-Thought |
> | 5 | [[#5. Employee "Day in the Life" Synthesis]] | Find friction | Grounded extraction |
> | 6 | [[#6. Internal How-To and Self-Service Builder]] | Remove friction | Stage-specific chain |
> | 7 | [[#7. Low-Friction Security Policy Gap Analysis]] | Secure | Checklist gate |
> | 8 | [[#8. Internal Automation Candidate Screener]] | Remove friction | Workflow pattern routing |
> | 9 | [[#9. New System Rollout and Adoption Plan]] | Adopt | Plan-then-solve |
> | 10 | [[#10. Productivity Business Case]] | Fund | Plan-then-solve |

---

## 1. Help Desk Productivity Drain Analysis

**Use when:** you're doing a monthly review of internal IT tickets to find which problems cost employees the most time, not just which happen most often.

```text
ROLE: You are an IT service analyst focused on employee productivity.

<it_tickets>{last 60–90 days of internal IT tickets: id, requester role/department, market,
  category (if any), description, resolution, time to resolve, how long the employee was blocked}</it_tickets>

Classify each ticket. Examples of the reasoning I want:

"Field tech can't open job in Sonar app, tablet stuck on old version" / "Forced update via MDM"
→ Category: DEVICE / APP UPDATE. Blocking: YES (tech idle). Evidence: "stuck on old version"

"New CS hire has no phone system login on day 1" / "Account created day 3"
→ Category: ONBOARDING / ACCESS. Blocking: YES. Evidence: "no phone system login on day 1"

"Password reset" (x4 same user this month) / "Reset"
→ Category: IDENTITY / PASSWORD. Blocking: YES, recurring. Evidence: "Password reset"

Then report:
1. Categories ranked by EMPLOYEE HOURS LOST (blocked time × occurrences), not ticket count
2. Most affected roles (CS, field, NOC, office) and markets
3. Recurring tickets that point to a fixable root cause (same user, same device model, same app)
4. For the top 5: the permanent fix (self-service reset, MDM policy, onboarding automation,
   training, replace device model) and estimated hours saved per month
5. Tickets you couldn't classify, listed separately
Every evidence string must be copied verbatim.
```

> Technique: [[Few-Shot Prompting]] with verbatim evidence. Ranking by employee hours lost, not ticket count, points the work at productivity.

---

## 2. Process Friction Map

**Use when:** a specific internal workflow feels slow or error-prone (e.g., install order → scheduling → completion → billing start; field tech closing a job; CS agent handling a billing dispute) and you want to see where the time goes.

```text
ROLE: You are a process improvement analyst (lean / value-stream mapping).

PROCESS: {name, start trigger, end point}
<observations>{step-by-step description from the people who do it: each step, who does it,
  which system, time spent, wait time, handoffs, re-keying, workarounds, error rates if known}</observations>

1. STEP TABLE: step | role | system | work time | wait time | handoff? | re-keyed data? |
   value-adding / necessary non-value / waste
2. FRICTION POINTS: the top 5 by total time lost (work + wait) × volume per month.
   Quote the observation for each.
3. ROOT CAUSES: for each friction point – missing integration, duplicate data entry, unclear
   ownership, approval bottleneck, tool limitation, training gap, policy.
4. FUTURE STATE: redesigned flow with steps removed, combined or automated; the system change
   needed for each (Sonar config, integration, form, automation – see prompt 8).
5. IMPACT: hours saved per month and errors avoided (calc from my numbers), and quick wins
   (<2 weeks) vs projects.
```

> Technique: [[Task Decomposition]]. Splitting the workflow into individual steps shows where time is wasted, which a general complaint can't.

---

## 3. Joiner / Mover / Leaver Workflow

**Use when:** new hires wait days for access, people who change roles keep old permissions, or leavers keep access. Each of these costs productivity or creates security risk.

```text
ROLE: You design identity and access lifecycle processes for a mid-sized company.

ROLES: {CS agent, CS lead, field tech, field supervisor, NOC engineer, finance, marketing, MVNO,
  manager} – with the systems and permission level each needs.
CURRENT PROCESS: {how HR notifies IT, how accounts are created, devices issued, current time to
  productive, known misses}

Respond in this format:
## Role access matrix (role × system × permission level) – "birthright" access by role
## JOINER checklist (Day −5 to Day 1): trigger from HR, accounts, device, phone/contact-center
   login, Sonar role, MDM enrollment, training links. Goal: productive on day 1.
## MOVER checklist: add new role access AND remove old-role access, with manager confirmation
## LEAVER checklist: same-day disable (identity, email, Sonar, VPN, contact center), device
   recovery, shared credential rotation, mailbox/file handoff
## Gates: approvals needed (manager for elevated access, finance for billing permissions),
   and a quarterly access review
## Automation: which steps can be triggered automatically from the HR system or SSO groups
Flag any role with access to customer billing credits, refunds or payments for extra review.
```

> Technique: [[Structured Outputs]] with approval [[Gate Checks]]. A clear checklist gets new hires working on day one and makes sure leavers lose access the same day.

---

## 4. Tool and License Rationalization

**Use when:** teams use overlapping tools (three chat apps, two file stores, several spreadsheet trackers), employees switch between too many systems, and you pay for unused licenses.

```text
ROLE: You are an IT portfolio analyst simplifying the employee tool stack.

<tools>{each tool: purpose, departments using it, active users vs licenses, annual cost,
  integrations with Sonar/SSO, data it holds, owner, satisfaction notes}</tools>

1. MAP tools by job-to-be-done (chat, file storage, ticketing, knowledge base, forms, tracking,
   scheduling, reporting). Show overlaps.
2. For each overlap, generate 2–3 consolidation options and evaluate each separately on:
   employee productivity (fewer context switches, better integration), migration effort,
   cost, data/security risk, and user resistance.
3. Prune options with migration effort that outweighs the benefit within 12 months.
4. Recommend: KEEP / CONSOLIDATE INTO X / RETIRE / RIGHT-SIZE LICENSES for every tool, with
   annual savings (calc) and the productivity benefit in plain terms.
5. A sequencing plan (least disruptive first) and how this connects to the Controller's
   single-source-of-truth project (Financial Controller library prompt 5).
```

> Technique: [[Tree-of-Thought]]. Comparing several consolidation options for each overlap stops the cheapest option from winning automatically when it would hurt productivity.

---

## 5. Employee "Day in the Life" Synthesis

**Use when:** you want to hear directly from employees about where technology slows them down, rather than relying on ticket data alone.

```text
ROLE: You synthesize employee interviews and surveys into evidence-backed IT priorities.

<inputs>{interview notes / ride-along notes / survey open comments, each tagged with role
  (CS agent, field tech, NOC, office) and market – anonymized}</inputs>

1. For each role: a short "day in the life" – the systems they touch, in order, and the
   moments of friction. Every friction point gets a verbatim quote.
2. Themes across roles (≤7), with counts, roles affected and 2 quotes each.
3. Workarounds employees invented (personal spreadsheets, texting photos, sticky notes) –
   these show where systems are failing them.
4. "If you could fix one thing" answers, ranked by frequency.
5. Top 5 IT priorities, each tied to a theme, the roles it helps, and a rough effort (S/M/L).
Don't generalize beyond the sample; give the sample size per role.
```

> Technique: grounded extraction from [[Output Validation]]. Quotes keep the priorities tied to what employees actually said, and the workaround list shows where systems are failing.

---

## 6. Internal How-To and Self-Service Builder

**Use when:** employees keep asking IT (or each other) the same "how do I…" questions about Sonar, the phone system, field tablets or expense tools.

```text
ROLE: You write internal how-to guides for non-technical employees.

<source>{resolved IT tickets on one topic, or notes from the person who knows the process,
  or a vendor admin guide – treat as data}</source>
AUDIENCE: {role, e.g., field tech on a tablet in a truck / CS agent mid-call}

STAGE 1 – Extract the exact steps that worked, in order, and note role-specific differences.
STAGE 2 – Write the guide: a title as the employee would search it ("How to reopen a closed job in
  Sonar"), when to use it, numbered steps (≤10, one action each), a screenshot placeholder for each
  key screen, and "if this doesn't work" with the escalation path.
STAGE 3 – A 3-line quick version for chat/Teams and a version for the help desk to paste.
STAGE 4 – Review: flag steps that aren't in the source, need admin rights, or vary by market.
```

> Technique: [[Stage-Specific Prompting]]. Guides are based on what actually worked, and the review stage catches steps the model may have invented.

---

## 7. Low-Friction Security Policy Gap Analysis

**Use when:** you're refreshing IT security policies or answering an insurer or auditor, and you want strong controls that don't slow employees down.

```text
ROLE: You are an IT governance and security analyst who values usability.

<current_document>{our existing policy or SOP, or "none"}</current_document>
FRAMEWORK: {NIST CSF 2.0 / CIS Controls v8 IG1 / insurer questionnaire pasted below}
ORG CONTEXT: {~N employees, roles, field techs on mobile devices, systems, SSO Y/N, MDM Y/N}
STATES: {list the 8} – flag state-specific requirements (e.g., breach notification) that differ.

1. COVERAGE TABLE: For each relevant control or question, write COVERED (quote our text) /
   PARTIAL (quote + what's missing) / MISSING.
2. PRIORITIZE gaps High/Med/Low by likelihood × impact for a company our size.
3. FRICTION RATING: for each recommended control, rate employee friction (LOW/MED/HIGH) and
   propose the lowest-friction way to meet it (SSO + phishing-resistant MFA instead of more passwords,
   MDM-managed devices instead of manual checks, conditional access instead of VPN everywhere).
4. DRAFT plain-language policy sections with owner role, review cadence and a measurable control.
5. EVIDENCE LIST: what an auditor or insurer would ask to see, and whether we likely have it.
Don't claim a control is COVERED unless you can quote our document.
```

> Technique: a checklist-style content gate from [[Gate Checks#^gate-content]], plus a friction rating. Security improves without costing productivity.

---

## 8. Internal Automation Candidate Screener

**Use when:** someone proposes "let's automate X" or "let's use AI for X" for an internal process, and you need to decide quickly whether X should be a script, a gated LLM workflow, an agent, or nothing.

```text
ROLE: You are an automation architect who has seen many projects fail by over-engineering.

PROPOSED USE CASE: {e.g., auto-create Sonar jobs from install orders / summarize CS calls into
  ticket notes / generate weekly reports / route internal IT tickets / reconcile spreadsheets}
CURRENT PROCESS: {who does it, how often, time per item, error rate, what systems}
DATA AVAILABLE: {structured fields, free text, APIs}

Answer in order:
1. DETERMINISM CHECK: Which parts can a rule, script or built-in system feature do? (These never
   go to an LLM.) Check whether Sonar or the existing tool already does this natively.
2. PATTERN FIT: Which fits the rest best, and why?
   none / single prompt / prompt chain / routing / parallelization /
   orchestrator-workers / evaluator-optimizer / autonomous agent
3. RISK: Worst outcome if wrong? Reversible? Touches customer billing or data? → Required
   gates and human-approval points.
4. VALUE: Employee hours saved per month and errors avoided, using my numbers.
5. PILOT: Smallest read-only or shadow-mode version to run for 2 weeks, and the metric that
   decides go/no-go.
6. VERDICT: BUILD / PILOT FIRST / BUY (existing feature or tool) / DON'T BUILD, plus one sentence.
```

> Technique: the five-pattern decision from [[Agentic Workflow Patterns]] plus [[Gate Checks]]. The "does the tool already do this?" check stops you from building something you already pay for.

---

## 9. New System Rollout and Adoption Plan

**Use when:** you're launching a new tool or a big change (new phone system, Sonar workflow change, new field app, SSO). Productivity drops if people don't adopt it.

```text
ROLE: You are an IT change-management lead.

CHANGE: {what's changing, why, go-live date, who's affected by role and market}
CONSTRAINTS: {training time available, shift coverage (CS/NOC can't all leave the floor),
  field techs' schedules, remote markets}

PLAN first: the 3 biggest adoption risks by role (e.g., CS during peak hours, techs in trucks
  with poor connectivity, veterans attached to the old way) and how to measure adoption.
  Stop and show me.

Then:
1. Timeline: before go-live / go-live week / first 30 days
2. Champions: one per team/market – their role and time commitment
3. Training by role: format (5-min video, floor walk, cheat sheet), length, timing around shifts
4. Go-live support: hypercare hours, where to get help, how issues are triaged
5. Communication plan: what each role hears, when, from whom (their manager, not just IT)
6. Adoption metrics: logins, old-tool usage decline, tickets about the new tool, task time
   before vs after – with targets at 2 and 6 weeks
7. Rollback or parallel-run criteria
```

> Technique: Plan-then-Solve from [[CoT prompt Samples#6. Sample 5 – Plan-then-Solve]]. Naming the adoption risks first keeps the training plan focused on the people most likely to struggle.

---

## 10. Productivity Business Case

**Use when:** you need budget for an IT investment (better devices for techs, an integration, SSO, help desk tooling) and leadership sees it as overhead.

```text
ROLE: You help an IT Director turn productivity improvements into business cases for executives.

<need>{what, why, current friction, what happens if we wait}</need>
<numbers>{employees affected by role, hours lost per person per week (from prompts 1/2/5),
  loaded hourly cost by role, error/rework costs, customer impact (e.g., CS handle time,
  tech jobs per day), solution costs (one-time + annual)}</numbers>
AUDIENCE: {CFO / CEO / COO}. They care about {EBITDA, churn, capacity without hiring}.

First, write a PLAN: the 3–4 arguments that matter most to this audience and the number behind
each. Stop and show me the plan.

Then write a 1-page memo:
- The ask (amount, timing) in the first sentence
- Hours recovered per month → capacity (e.g., "equivalent to 1.5 CS agents" or "+0.5 jobs per
  tech per day") and dollars (show math, my numbers only)
- Customer impact where it exists (faster answers, fewer repeat visits)
- 2–3 options (minimum, recommended, ideal) with cost and payback for each
- How we'll measure it at 3 and 6 months
Mark any number you derived as "(calc)" and any assumption as "(assumption)".
```

> Technique: Plan-then-Solve. Expressing recovered hours as capacity (agents, jobs per day) gives executives a figure they already think in.

---

## Key Takeaways

- **Measure employee hours lost, not ticket counts.** Prompts 1, 2 and 5 find the friction that costs the most time.
- **Remove friction at the source.** Day-one access (3), fewer tools (4), self-service (6) and right-sized automation (8) beat answering the same ticket faster.
- **A change only helps if people adopt it.** Prompt 9 treats rollout as a people problem.
- **Security should cost as little productivity as possible.** Prompt 7 rates every control for friction and picks the least disruptive way to meet it.
