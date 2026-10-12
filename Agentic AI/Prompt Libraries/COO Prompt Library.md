---
title: "COO Prompt Library"
aliases:
  - COO Prompts
  - Chief Operating Officer Prompt Library
type: reference
status: review
created: 2026-10-01
related:
  - "[[NOC Director Prompt Library]]"
  - "[[IT Director Prompt Library]]"
  - "[[Customer Service Director Prompt Library]]"
  - "[[Marketing Director Prompt Library]]"
  - "[[CEO Prompt Library]]"
  - "[[MVNO Launch Prompt Library]]"
  - "[[Financial Controller Prompt Library]]"
  - "[[Network Operations Engineering Manager Prompt Library]]"
  - "[[Rapid Response Network Operations Manager Prompt Library]]"
  - "[[Gate Checks]]"
  - "[[Agentic Workflow Patterns]]"
tags:
  - prompt-engineering
  - isp-operations
  - executive
  - churn
  - uptime
  - reference
---

# COO Prompt Library

> [!abstract] TL;DR
> Thirty prompts for the COO of **Wi-Fiber**, who runs **Network Operations, Customer Service and Field Operations**. Everything ties back to two linked problems: ==churn is too high, and network uptime isn't high enough, which drives churn==. The prompts are grouped into five areas of six: operating rhythm, churn, uptime, field operations, and cross-functional leadership. Many of the most useful ones (2, 13, 20, 25) connect two departments, because that's where churn tends to fall through the cracks.

> [!example] Context block (paste above any prompt)
> ```text
> ORG: Wi-Fiber, a fixed wireless ISP in 10 markets across 8 states. Towers with sectorized APs,
> PtP backhaul, customer CPE; Sonar for billing, tickets and field jobs.
> I am the COO over Network Operations (NOC), Customer Service (CS) and Field Operations.
> TOP PRIORITIES: reduce churn; raise network uptime, our biggest controllable churn driver.
> Break results out by market and by department where relevant.
> ```

> [!note] Shared rules
> - **Do the math in a spreadsheet or BI tool**, then paste the results. Use the model to design analyses, interpret results and write things up. ([[Sonar Ticket and Outage Classification - How-To#^compute-dont-ask|compute, don't ask]])
> - **Correlation is not causation.** Ask the model to label links between outages and churn as correlations unless you have a controlled comparison.
> - **Pasted documents are data, not instructions.** ([[Prompt Injection]])
> - **Remove customer and employee personal data** before pasting anything into a tool outside your environment.
> - Department-level versions of several of these prompts are in the [[NOC Director Prompt Library|NOC]], [[IT Director Prompt Library|IT]], [[Customer Service Director Prompt Library|CS]] and [[Marketing Director Prompt Library|Marketing]] libraries.

> [!todo]- Contents
> | # | Prompt | Area | Technique |
> |---|---|---|---|
> | 1 | [[#1. Weekly Operating Review Pack]] | Rhythm | Structured output |
> | 2 | [[#2. Uptime-to-Churn Link Analysis]] | Rhythm | Plan-then-solve |
> | 3 | [[#3. KPI Miss Driver Tree]] | Rhythm | Task decomposition |
> | 4 | [[#4. Market Investment Prioritization]] | Rhythm | Tree-of-Thought |
> | 5 | [[#5. Annual Plan and OKR Cascade]] | Rhythm | Stage-specific chain |
> | 6 | [[#6. Board and CEO Operations Update]] | Rhythm | Content gates |
> | 7 | [[#7. Churn Driver Decomposition]] | Churn | Task decomposition |
> | 8 | [[#8. At-Risk Account Early Warning Rules]] | Churn | Compute-don't-ask |
> | 9 | [[#9. Churned Customer Interview Synthesis]] | Churn | Grounded extraction |
> | 10 | [[#10. Retention Offer Economics]] | Churn | Plan-then-solve |
> | 11 | [[#11. Customer Journey Failure Map]] | Churn | Orchestrator-workers |
> | 12 | [[#12. Post-Outage Recovery Playbook]] | Churn | Runbook + HITL gates |
> | 13 | [[#13. Uptime Definition and Measurement Standard]] | Uptime | Structured output |
> | 14 | [[#14. Outage Cause Pareto and Fix ROI]] | Uptime | Plan-then-solve |
> | 15 | [[#15. Tower Resilience Assessment]] | Uptime | Checklist gate |
> | 16 | [[#16. Seasonal Weather Readiness by State]] | Uptime | Parallelization |
> | 17 | [[#17. Change-Induced Outage Review]] | Uptime | Grounded extraction |
> | 18 | [[#18. Upstream Vendor and Landlord Accountability]] | Uptime | Content gates |
> | 19 | [[#19. Avoidable Truck Roll Analysis]] | Field | Few-shot |
> | 20 | [[#20. Install Quality Standard and Early Churn]] | Field | Logic gates |
> | 21 | [[#21. Dispatch and Schedule Review]] | Field | Structured output |
> | 22 | [[#22. Repeat Dispatch Root Cause]] | Field | Task decomposition |
> | 23 | [[#23. Tower Work Safety and Job Hazard Review]] | Field | Evaluator-optimizer |
> | 24 | [[#24. Spares and Inventory Readiness for MTTR]] | Field | Plan-then-solve |
> | 25 | [[#25. Major Incident Command Roles]] | Cross | Structured output |
> | 26 | [[#26. Ticket Handoff Friction Analysis]] | Cross | Grounded extraction |
> | 27 | [[#27. Leader 1:1 and Skip-Level Prep]] | Cross | Structured output |
> | 28 | [[#28. Org Design for 10 Markets]] | Cross | Tree-of-Thought |
> | 29 | [[#29. Operations AI and Automation Roadmap]] | Cross | Workflow pattern routing |
> | 30 | [[#30. Operations Change Communication]] | Cross | Multi-audience generation |

---

# A. Operating Rhythm and Strategy

## 1. Weekly Operating Review Pack

**Use when:** you prepare the weekly ops review across NOC, CS and Field.

```text
ROLE: You prepare a weekly operating review for an ISP COO.

<kpis>{by market, this week vs last week vs 4-wk avg vs target:
  NOC: subscriber-minutes of outage, uptime %, # incidents Sev1/2, MTTR
  CS: contacts/1k subs, FCR, CSAT, cancels, saves, save rate
  Field: installs, repairs, truck rolls/1k subs, repeat dispatch %, on-time %
  Business: gross adds, net adds, churn %}</kpis>
<notes>{each director's 3-line update}</notes>

Respond ONLY in this format:
## Headline (2 sentences: the most important change this week and what we're doing about it)
## Red / Yellow / Green by market × department (table; red = worse than target AND trend down)
## Uptime → churn watch (markets where outage minutes rose AND cancels rose)
## Wins (max 3)
## Decisions needed from me (each with options + director's recommendation)
## Follow-ups from last week (done / not done)
Every number must come from kpis. Don't calculate new metrics.
```

> Technique: [[Structured Outputs]]. Using the same format every week makes trends easy to see and hard to hide.

## 2. Uptime-to-Churn Link Analysis

**Use when:** you want to put a number on how much uptime drives churn, so you can justify reliability spending in churn dollars.

```text
ROLE: You are an operations analyst designing and interpreting an analysis.

AVAILABLE DATA: {Sonar accounts w/ tower/sector + cancel date + reason; outage events with
  start/end + affected sectors; tickets; truck rolls; ARPU}

STEP 1 – PLAN (stop after this and show me):
  - Unit of analysis (subscriber or sector-month), exposure window (e.g., outage minutes
    in prior 60/90 days), outcome (churn in next 30/60 days)
  - Exposure bands (e.g., 0, <60 min, 60–240, 240+, repeat outages)
  - Confounders to control for (market, tenure, plan, price changes, competitor entry)
  - The exact table I should build in SQL/Excel
STEP 2 – INTERPRET (after I paste the results): {results table}
  - Churn rate by exposure band and the lift vs zero-outage subscribers
  - Estimated churn and revenue attributable to outages (label it as an estimate)
  - The uptime threshold where churn noticeably increases, if there is one
  - Caveats, and what a controlled comparison would need
```

> Technique: Plan-then-Solve from [[CoT prompt Samples#6. Sample 5 – Plan-then-Solve]]. The model designs the analysis and you run it. This is the number the other 29 prompts depend on.

## 3. KPI Miss Driver Tree

**Use when:** a headline metric misses (churn, uptime, CSAT) and you need the real cause, not just the first explanation offered.

```text
ROLE: You build driver trees to explain KPI misses.

KPI MISSED: {e.g., churn 2.4% vs 1.8% target in October}
<data>{the KPI broken down by every dimension available: market, tenure band, plan,
       cancel reason, sector outage exposure, channel acquired}</data>

1. Build a driver tree: KPI → 3–5 first-level drivers → sub-drivers. Show it as an indented list.
2. For each node, give the variance vs target using only the data provided. Mark nodes without
   data "NO DATA".
3. Identify the 1–2 nodes that explain most of the variance (show the math).
4. Separate CONTROLLABLE (uptime, support, install quality, pricing decisions) from
   EXTERNAL (competitor entry, seasonality, moves).
5. Recommend actions only for the controllable drivers, plus the data needed to fill NO DATA nodes.
```

> Technique: [[Task Decomposition]]. The tree keeps the explanation honest because every part of the variance has to be accounted for.

## 4. Market Investment Prioritization

**Use when:** you have limited capital and crews and need to decide which of the 10 markets gets reliability investment first.

```text
ROLE: You are a strategy advisor to an ISP COO.

<markets>{for each of 10 markets: subs, ARPU, churn %, uptime %, outage minutes/sub,
  sector congestion %, competitor pressure (low/med/high + who), growth potential,
  known capex needs + cost}</markets>
BUDGET: {capex + crew-months available}

1. Propose 3 different prioritization strategies (e.g., "defend largest revenue",
   "fix worst churn", "highest churn-dollars saved per capex dollar").
2. Evaluate each strategy as its own branch: which markets it funds, expected churn
   reduction (show assumptions), risks.
3. Prune strategies that break the budget or leave a market in crisis untouched.
4. Recommend one strategy (or a blend) with a ranked market list and the trigger that would
   make you re-rank (e.g., competitor fiber build announced).
```

> Technique: [[Tree-of-Thought]]. Comparing whole strategies shows the trade-offs that a single ranked list would hide.

## 5. Annual Plan and OKR Cascade

**Use when:** you're setting next year's goals and need NOC, CS and Field targets that all add up to the churn and uptime goals.

```text
ROLE: You help a COO build an annual operating plan.

COMPANY GOALS: {e.g., churn from X% to Y%, uptime from A% to B%, net adds N}
BASELINES: {current KPIs by department and market}
CONSTRAINTS: {headcount, capex, opex}

STAGE 1 – Translate company goals into 3–4 operations objectives.
STAGE 2 – For each department (NOC, CS, Field), write 2 objectives with 2–3 measurable key results
  each, and show which company goal each one moves.
STAGE 3 – Consistency check: flag any key result that conflicts with another (e.g., CS AHT target vs
  save-desk time; field productivity vs install quality) and propose how to resolve it.
STAGE 4 – Quarterly milestones and the leading indicator to watch monthly for each objective.
```

> Technique: [[Stage-Specific Prompting]]. Stage 3 checks the cascade for conflicting targets, which are a common reason department goals work against each other.

## 6. Board and CEO Operations Update

**Use when:** you report operations results upward and need to be candid and brief.

```text
ROLE: You write operations updates for an ISP's CEO/board.

<facts>{quarter KPIs vs plan, major incidents, initiatives status, spend vs budget, risks}</facts>

Write ≤1 page:
- Bottom line (3 sentences): are churn and uptime getting better, by how much, and why
- Scorecard table: metric | plan | actual | trend | comment
- What worked / what didn't (2 each, with evidence)
- Biggest risk next quarter and the mitigation
- Ask of the board (if any)

MUST: lead with the bad news if there is any; give every number with its comparison.
MUST NOT: use department jargon (MTTR, sector, PtP) without a plain gloss; claim causation
  without evidence.
Then self-check each MUST/MUST NOT with PASS/FAIL.
```

> Technique: content [[Gate Checks]] with a self-check. The rules make the model lead with bad news and use plain language.

---

# B. Churn

## 7. Churn Driver Decomposition

**Use when:** you want to know what share of churn each department can actually influence.

```text
ROLE: You are a churn strategist.

<churn_data>{monthly cancels by reclassified reason (see CS library prompt 3), market,
  tenure band, outage exposure band, install-quality flag, acquisition channel}</churn_data>

1. Split churn into: NETWORK-DRIVEN (reliability, speed), SERVICE-DRIVEN (support, billing,
   install experience), COMMERCIAL (price, competitor), UNCONTROLLABLE (moves, death, business closed).
   Show % of total and by market.
2. For each controllable bucket, name the owning department(s) and the 2 most effective levers.
3. Estimate the churn reduction if each lever achieved a realistic improvement (state assumptions).
4. Rank levers by churn reduction per dollar/effort and recommend the top 5 for this year.
```

> Technique: [[Task Decomposition]]. Assigning each type of churn to an owner turns "reduce churn" into specific jobs for specific teams.

## 8. At-Risk Account Early Warning Rules

**Use when:** you want a churn-risk score computed in Sonar or BI from operational signals, with clear actions for each risk level.

```text
ROLE: You design rule-based churn early-warning systems. You design the rules; code computes them.

AVAILABLE SIGNALS per account: {outage minutes last 30/90 days, # outages, tickets last 30 days,
  repeat contacts, truck rolls, signal quality (RSL/SNR) trend, speed-test results vs plan,
  plan downgrades, late payments, tenure, sector congestion}
HISTORICAL CHURN RATES by signal (if available): {table}

Output:
1. A point-based score (each signal → points, with thresholds) that a SQL query can implement.
   Justify each weight using the historical data, or mark it "initial guess – validate".
2. Risk tiers (e.g., 0–3 low, 4–6 watch, 7+ high) and the ACTION per tier with owner:
   CS outreach, NOC sector review, field proactive realign, retention offer.
3. How to validate: backtest on the last 6 months, and the precision/recall to target.
4. Which signals we should start collecting that we don't have.
```

> Technique: "compute, don't ask" from the [[Sonar Ticket and Outage Classification - How-To|Sonar how-to]]. The LLM writes the rules, and the scoring runs as code every night.

## 9. Churned Customer Interview Synthesis

**Use when:** you've done (or recorded) exit calls with former customers and want findings you can trust.

```text
ROLE: You synthesize customer interviews into evidence-backed findings.

<transcripts>{10–40 exit-call transcripts or notes with market + tenure}</transcripts>

1. For each interview: the moment they decided to leave, what tipped it, what would have
   kept them, competitor chosen. Every field gets a verbatim quote or "not stated".
2. Cross-interview themes (≤7), each with count, markets and the 2 strongest quotes.
3. "Last straw" analysis: which events most often came right before the decision
   (outage, slow evenings, billing surprise, bad support call, missed appointment).
4. 3 recommendations, each tied to a theme and an owning department.
Don't generalize beyond the sample. Note the sample size on every finding.
```

> Technique: grounded extraction from [[Output Validation]]. Requiring quotes keeps the synthesis from turning into assumptions.

## 10. Retention Offer Economics

**Use when:** you're setting what the save desk can offer and need to know whether saves are actually profitable.

```text
ROLE: You are a finance-minded retention analyst.

DATA: {ARPU, gross margin, avg remaining tenure of saved vs never-at-risk customers,
  save rate by offer type, offer cost, % of saved customers who churn within 6 months,
  cost of a truck roll}

PLAN first: define LTV of a saved customer, the cost of each offer, and the break-even save rate.
  Show the formulas. Then compute using my numbers only:
1. Net value per offer type (table)
2. Offers that lose money, and offers we should use more
3. A recommended offer ladder by cancel reason (reliability cancels get a fix plus a credit,
   not just a discount)
4. Guardrails: max credit per account per year, approval levels
Label every assumption.
```

> Technique: Plan-then-Solve from [[CoT prompt Samples#6. Sample 5 – Plan-then-Solve]]. You can check the formulas before trusting the conclusions.

## 11. Customer Journey Failure Map

**Use when:** you want to see where in the customer lifecycle each department is losing customers.

```text
ROLE: You are an orchestrator coordinating three specialist analysts.

JOURNEY STAGES: sale → install scheduling → install → first 90 days → steady state →
  outage experience → support contact → billing → cancel/save

Step 1 (orchestrator): For each stage, write a focused question for each relevant specialist.
Step 2 (workers – answer each separately using only its data):
  NOC analyst <noc_data>{outages, uptime by sector, congestion}</noc_data>
  CS analyst <cs_data>{contacts by stage, FCR, CSAT, cancels by tenure}</cs_data>
  Field analyst <field_data>{install metrics, missed appointments, repeat dispatch}</field_data>
Step 3 (orchestrator): Combine into a map: stage | failure points | evidence | churn impact
  estimate (H/M/L) | owner | handoff gaps between departments.
Highlight the 3 stages where failures span departments and nobody clearly owns them.
```

> Technique: [[Orchestrator-Workers Workflow]]. Each department analyst sees only its own data, and the orchestrator finds the gaps between departments.

## 12. Post-Outage Recovery Playbook

**Use when:** you want a standard, cross-department playbook that runs after every significant outage so it doesn't cause churn.

```text
ROLE: You write operational runbooks.

INPUTS: {outage severity definitions, credit policy, CS and field capacity, comms channels,
  approval roles}

Write a runbook with phases and owners:
PHASE 0 – Trigger: which outage sizes/durations activate it (and repeat-outage triggers)
PHASE 1 – During: customer notices (NOC → CS), CS talk track, status page cadence
PHASE 2 – Within 24h after restore: verify every affected CPE re-registered (NOC), list
  non-recovered CPE for field, segment customers (once / repeat / ticketed)
PHASE 3 – Within 72h: recovery outreach by segment (CS), credits per policy (billing),
  proactive calls to repeat-affected customers
PHASE 4 – Within 7 days: post-incident review, prevention action, "we fixed it" message (Marketing)
For each step: owner role, SLA, system (Sonar etc.), and an APPROVAL GATE where a human must
sign off (customer-facing messages, credits above threshold).
```

> Technique: action and human-approval [[Gate Checks#^other-gate-types|gates]] built into a runbook. Each step has an owner and a sign-off point.

---

# C. Network Uptime

## 13. Uptime Definition and Measurement Standard

**Use when:** each department reports "uptime" differently and you need one company-wide definition that matches what customers actually experience.

```text
ROLE: You are a network reliability architect writing an internal measurement standard.

CURRENT STATE: {how uptime is calculated today, by whom, data sources (monitoring, CPE
  registration, Sonar outages), known gaps}

Write the standard:
1. Primary metric: customer-experienced availability = 1 − (subscriber-minutes impacted ÷
   total subscriber-minutes). Define "impacted" (down, degraded below X% of plan speed?).
2. Secondary metrics: tower/sector availability, backhaul availability, MTTD, MTTR,
   repeat-outage subscribers (2+ in 90 days).
3. What counts and what's excluded (planned maintenance with notice? customer-side faults?)
   with a rationale for each decision. Recommend NOT excluding anything customers feel.
4. Data sources and calculation steps (precise enough for a SQL query)
5. Reporting cadence, by market/tower, and targets for each tier.
List decisions I need to make, with your recommendation.
```

> Technique: [[Structured Outputs]] applied to a policy. Uptime and churn can't be linked until everyone measures uptime the same way.

## 14. Outage Cause Pareto and Fix ROI

**Use when:** you want to spend reliability money where it removes the most subscriber-minutes of outage.

```text
ROLE: You are a reliability engineer and business analyst.

<outages>{12 months: date, market, tower, affected subs, duration, cause category
  (power, backhaul, equipment failure, config/change, weather, upstream, fiber cut, unknown)}</outages>
FIX OPTIONS + COSTS: {generators/batteries, redundant backhaul, spares, monitoring, change process}

PLAN the analysis first. Then, with the numbers I supply:
1. Pareto: cause categories ranked by subscriber-minutes (not count). Show cumulative %.
2. Top 10 towers by subscriber-minutes and their main cause.
3. Map each fix option to the outage minutes it would plausibly prevent (state assumptions)
   → cost per subscriber-minute avoided, and churn dollars avoided using {churn per outage minute
   from prompt 2}.
4. Ranked investment list, and how many "unknown" causes we need to resolve before trusting this.
```

> Technique: Plan-then-Solve. Ranking by subscriber-minutes rather than incident count matches how customers experience outages.

## 15. Tower Resilience Assessment

**Use when:** you're auditing towers for single points of failure before they cause an outage.

```text
ROLE: You assess tower-site resilience for a fixed wireless ISP.

<sites>{per tower: market, subs served, power (utility, battery runtime, generator Y/N,
  auto-transfer Y/N), backhaul paths (count, licensed/unlicensed, shared hops), downstream
  towers fed through this one, remote management (OOB access Y/N), environmental monitoring,
  equipment age, last site visit, landlord access restrictions}</sites>

For each tower, check: N+1 power ≥ {target hours}, redundant backhaul, OOB access,
  monitoring for power/temperature/door, equipment within support life, 24/7 access.
Output:
| tower | subs (incl. downstream) | failed checks | risk score (subs × failed checks weight) | top fix | est. cost |
Then: top 15 towers by risk, "hub" towers whose failure takes down others, and a
  phased remediation plan by quarter within {budget}.
Only score checks that have data. Mark others UNKNOWN and list them for a site visit.
```

> Technique: a checklist gate from [[Gate Checks]]. Weighting by subscribers, including downstream towers, ties each risk to churn exposure.

## 16. Seasonal Weather Readiness by State

**Use when:** before each season, you want a readiness plan for each of the 8 states' weather risks.

```text
ROLE: You coordinate seasonal readiness planning for a multi-state ISP.

STATES/MARKETS: {list with typical seasonal threats: ice, snow, thunderstorms/lightning,
  hurricanes, heat, wildfire/PSPS power shutoffs, flooding}
ASSETS PER MARKET: {towers, generator coverage, fuel contracts, crews, spares}

Analyze each state as a separate parallel task (don't let states blend):
  - Top 2 threats this season and their failure modes on our network (power loss, RF fade,
    ice on dishes, tower access, heat on cabinets)
  - Readiness checklist (pre-season tasks with owner and due date)
  - Gaps vs current assets
Then aggregate:
  - Cross-market shared needs (fuel contracts, spare pool, mutual aid between markets)
  - Customer pre-season messaging (with Marketing/CS)
  - The top 5 readiness actions company-wide by subscribers protected
```

> Technique: [[Parallelization Workflow]]. Analyzing states separately and combining at the end keeps one state's threats from crowding out another's.

## 17. Change-Induced Outage Review

**Use when:** you suspect your own changes (firmware, config, maintenance) cause a meaningful share of outages.

```text
ROLE: You audit the link between network changes and outages.

<outages>{12 months with cause notes}</outages>
<changes>{change records: date, device/tower, type, approved Y/N, MOP Y/N, rollback used Y/N}</changes>

1. Match each outage to changes on the same device/tower within {N hours} before. Label MATCH
   (cited), POSSIBLE, or NONE. Quote the evidence.
2. % of outages and subscriber-minutes that were change-induced.
3. Among change-induced: approved vs unapproved, MOP vs no MOP, rollback used vs not.
4. Patterns (firmware rollouts, Friday changes, specific engineers' shifts—use roles only).
5. Process changes: staged rollouts, canary sectors, change freeze windows, pre/post checks.
Only label MATCH with explicit evidence. Never assign blame to individuals.
```

> Technique: grounded extraction with evidence labels. Self-inflicted outages are often the cheapest uptime gains to fix. Pair this with NOC library prompts 3 (MOP review) and 9 (staged firmware rollouts).

## 18. Upstream Vendor and Landlord Accountability

**Use when:** transit providers, backhaul lessors, tower landlords or power utilities keep causing outages and you need to escalate.

```text
ROLE: You prepare vendor accountability packages.

VENDOR: {name/type}
<contract>{SLA terms, credits, escalation path, notice requirements – relevant clauses}</contract>
<incidents>{dates, durations, affected subs, their tickets/RFOs, our ticket numbers}</incidents>

Produce:
1. SLA performance table vs contract terms, with credits owed (show calculation per clause)
2. Escalation letter: factual, cites clauses and incidents, requests credits + a corrective
   action plan by a date. Firm and professional.
3. Internal brief: our leverage, alternatives (redundant provider/path), recommended next step
   if they don't respond, and whether to involve legal.
MUST NOT: threaten, speculate about their internal causes, or misstate contract terms (quote them).
```

> Technique: content [[Gate Checks]] with quoted contract clauses as the source of truth. A person reviews before sending, and legal reviews where flagged.

---

# D. Field Operations

## 19. Avoidable Truck Roll Analysis

**Use when:** truck rolls per 1,000 subscribers are high and you suspect many could have been fixed remotely or with better triage.

```text
ROLE: You classify truck rolls as avoidable or necessary.

<truck_rolls>{job id, market, reason, pre-dispatch CS/NOC notes, tech findings, resolution}</truck_rolls>

Examples of my classification standard:
- Findings: "Customer router unplugged" → AVOIDABLE – remote triage miss. Evidence: "router unplugged"
- Findings: "CPE realigned, RSL -72 → -58" → NECESSARY – physical fix. Evidence: "realigned"
- Findings: "Sector down at tower, nothing wrong at home" → AVOIDABLE – NOC/outage check miss
- Findings: "Replaced failed PoE" → NECESSARY (but check: could the customer swap it with a shipped part?)

For each job: label, sub-type, verbatim evidence.
Then: % avoidable by market and sub-type, cost (× {cost per roll}), and the top 3 triage/
  remote-diagnostic changes (e.g., mandatory outage check, remote CPE signal check before dispatch).
```

> Technique: [[Few-Shot Prompting]]. Four examples set a consistent standard for what counts as avoidable.

## 20. Install Quality Standard and Early Churn

**Use when:** customers whose installs had marginal signal tend to churn early, and you want an install acceptance gate.

```text
ROLE: You design install quality standards for fixed wireless.

DATA: {early churn (90-day) and early tickets by install signal bands (RSL/SNR/modulation at
  completion), by tech, by market; current install checklist}

1. Show 90-day churn and ticket rate by signal band (from my data) and identify the threshold
   where problems rise.
2. Write an INSTALL ACCEPTANCE GATE: minimum RSL/SNR/modulation, speed test at completion vs plan,
   photo of mount, customer Wi-Fi walkthrough, Sonar fields required. Define what happens if
   the gate fails (try another AP/sector, higher mount, don't install + refer, supervisor override with reason).
3. A 30-day post-install proactive check (remote signal check, auto-ticket if degraded).
4. How to report gate compliance by tech without creating perverse incentives.
```

> Technique: logic [[Gate Checks]] applied to physical work. A bad install shouldn't be allowed to "pass", just as bad LLM output shouldn't.

## 21. Dispatch and Schedule Review

**Use when:** you're reviewing a market's daily or weekly field schedule for efficiency and churn risk.

```text
ROLE: You review field dispatch schedules for an ISP.

<jobs>{Sonar jobs for the day/week: id, type (install/repair/tower), priority, customer
  churn-risk tier (from prompt 8), area, time window, assigned tech, est. duration}</jobs>
<techs>{tech (initials), skills (tower-certified?), start location, hours}</techs>

Respond ONLY in this format:
## Risks (jobs likely to miss window, high-churn-risk customers scheduled late or unassigned)
## Inefficiencies (backtracking, skill mismatches, overloaded/underloaded techs)
## Suggested changes (specific swaps/reorders, with reasoning)
## Capacity outlook (backlog days by job type, by market)
Every suggestion must reference job ids. Repairs for high-churn-risk or repeat-outage customers
take priority over routine installs unless I say otherwise.
```

> Technique: [[Structured Outputs]]. Including churn risk in dispatch decisions links field priorities to retention.

## 22. Repeat Dispatch Root Cause

**Use when:** the same customer needs a second truck roll within 30 days, which costs you twice and puts the customer at high churn risk.

```text
ROLE: You analyze repeat field dispatches.

<repeat_pairs>{for each: first job (type, tech, findings, resolution, signal at close), second job
  (same fields), days between, CS contacts in between, sector outages in between}</repeat_pairs>

Decompose each pair:
1. Was the second visit for the SAME issue? (yes/no/unclear + evidence)
2. If same: why the first fix failed – [misdiagnosis, temporary fix, part failure, network-side
   issue not caught, install standard not met, customer-side]
3. Could the first visit have prevented it? What step was missing?
Report: rates by cause, market and job type (techs as anonymized IDs), training needs vs
  process/tooling needs, and network-side issues to send to the NOC.
```

> Technique: [[Task Decomposition]]. Separating "same issue" from "new issue" stops the repeat-dispatch rate from overstating the problem.

## 23. Tower Work Safety and Job Hazard Review

**Use when:** you're reviewing climbs, RF exposure work or storm restoration plans. Safety matters more than uptime.

```text
ROLE: Act in two roles.

PLANNER: Given this tower job {task, tower type/height, equipment, crew, weather forecast,
  RF sources on structure, access}, draft a Job Hazard Analysis: steps, hazards per step,
  controls, PPE, rescue plan, stop-work triggers.

SAFETY REVIEWER: Review the JHA against {company safety policy / OSHA tower climbing practices /
  carrier RF safety requirements – pasted}. For each step: ADEQUATE / INSUFFICIENT + why.
  Flag missing items: competent climber designation, 100% tie-off, rescue plan specifics,
  RF power-down coordination with other tenants, weather limits.

PLANNER: Revise for every INSUFFICIENT item. Output the final JHA and a 5-line crew briefing.
This is a drafting aid. A qualified safety lead must approve it.
```

> Technique: [[Evaluator-Optimizer Workflow]]. A reviewer with authority, plus a required human approval, because the cost of a mistake here is a person, not churn.

## 24. Spares and Inventory Readiness for MTTR

**Use when:** outages last longer because the right radio, backhaul unit or power gear isn't stocked in that market.

```text
ROLE: You plan spare-parts strategy to reduce outage repair time.

DATA: {installed base by market and model (APs, PtP radios, switches, routers, power gear),
  failure rates/12 mo, current spares by warehouse, vendor lead times, drive time between
  markets, cost per unit, outages where "waiting on part" extended MTTR}

PLAN the method first (e.g., spares per installed base by failure rate, lead time and criticality).
Then:
1. Per market: recommended min spares by model, with gaps vs current stock
2. Critical spares (failure takes down many subs or hub towers) that must be in every market
3. Shared regional pool options to cut cost
4. Hours of MTTR saved (estimate, from "waiting on part" history) and cost
5. End-of-life models that need a replacement plan rather than more spares
```

> Technique: Plan-then-Solve. Linking spares to "waiting on part" outage hours turns inventory spending into uptime gained.

---

# E. Cross-Functional Leadership

## 25. Major Incident Command Roles

**Use when:** during big outages, NOC, CS and Field step on each other, or nobody owns customer communication.

```text
ROLE: You design incident command structures for ISPs.

CONTEXT: {team sizes per dept, on-call structure, tools (Sonar, chat, bridge), markets, after-hours coverage}

Output:
## Severity levels (with objective triggers: subs affected, duration, hub tower down)
## Roles per severity: Incident Commander, Tech Lead (NOC), Comms Lead (CS), Field Lead,
   Exec liaison – who fills each, backups, and who does NOT join the bridge
## RACI table for key tasks (diagnosis, dispatch, customer notice, status page, credits,
   exec updates, closure, post-incident review)
## Cadence (update intervals per severity, to whom)
## Handoffs (shift change, escalation, closure criteria including "all CPE re-registered")
## One-page checklist for the Incident Commander
```

> Technique: [[Structured Outputs]]. One shared structure prevents the "everyone's on the bridge, nobody's talking to customers" problem.

## 26. Ticket Handoff Friction Analysis

**Use when:** tickets bounce between CS, NOC and Field, adding days that customers notice.

```text
ROLE: You analyze cross-department handoffs.

<ticket_histories>{tickets with 2+ group changes: each assignment (group, timestamp, note),
  final resolution, total age}</ticket_histories>

1. For each ticket: number of handoffs, time spent waiting in each group, and whether each
   handoff note contained what the next team needed (quote it). Label each handoff
   CLEAN / MISSING_INFO / WRONG_GROUP / BOUNCED_BACK.
2. Most common bad handoff paths (e.g., CS→Field→NOC→Field) with avg added days.
3. The minimum required fields per handoff type (e.g., CS→NOC: tower/sector, CPE signal,
   outage check done Y/N) to turn into required Sonar fields.
4. Ownership rule proposal: who owns the customer while the ticket is with another team.
```

> Technique: grounded extraction. Quoting real handoff notes shows exactly what information is missing.

## 27. Leader 1:1 and Skip-Level Prep

**Use when:** you meet with your three directors or their teams and want focused conversations.

```text
ROLE: You help an operations executive prepare for 1:1s.

PERSON: {role (e.g., NOC Director), their goals/OKRs, recent KPIs vs target, notes from last 1:1,
  open commitments, anything I've heard from their team or peers}
MEETING TYPE: {1:1 / skip-level with their team / quarterly review}

Output:
## Recognize (1–2 specific wins with evidence)
## Discuss (≤3 topics, each with an open question – not a leading one)
## Support (what they may need from me: decisions, budget, cover with peers)
## Accountability (open commitments; how to raise any slipped item respectfully)
## Cross-department (one place their work affects churn or uptime through another team)
## For skip-levels: 5 questions that surface ground truth without undermining the director
```

> Technique: [[Structured Outputs]]. A consistent agenda means churn and uptime come up in every leadership conversation.

## 28. Org Design for 10 Markets

**Use when:** you're deciding what to centralize (NOC, CS, dispatch) and what to keep local in each market (techs, market managers).

```text
ROLE: You are an organizational design advisor for multi-market field service businesses.

CURRENT ORG: {structure, headcount by dept and market, spans of control, pain points}
GOALS: lower churn, higher uptime, scalable to {N} more markets, within {budget}.

Generate 3 org models (e.g., fully centralized ops w/ local techs; regional hubs;
  market GMs owning CS+Field locally with central NOC).
Evaluate each separately on: speed of outage response, customer experience consistency,
  local accountability for churn, cost, management span, scalability, transition risk.
Prune any model that can't be staffed within budget.
Recommend one, with: transition phases, roles that change, risks to retention during the
  change, and the metrics that show it's working at 90/180 days.
```

> Technique: [[Tree-of-Thought]]. Comparing whole org models brings out trade-offs that small tweaks to the current org would hide.

## 29. Operations AI and Automation Roadmap

**Use when:** you're deciding where AI and automation should go across NOC, CS and Field. This connects your MS AI work to the business.

```text
ROLE: You are an AI solutions architect who avoids over-engineering.

CANDIDATE USE CASES: {e.g., ticket routing, churn-signal tagging, outage notices, alert
  correlation, truck-roll triage, install QA from photos, post-incident drafts, VoC reports}
For each: volume, time per item, error cost, data available, customer-facing Y/N.

For EACH use case:
1. What can be rules/code only (no LLM)
2. Best pattern: none / single prompt / prompt chain / routing / parallelization /
   orchestrator-workers / evaluator-optimizer / agent
3. Required gates (format, grounding, action preconditions, human approval)
4. Value: hours/month and churn/uptime impact (H/M/L, with reasoning)
5. Risk if wrong, and whether it's reversible
Then: a 3-phase roadmap (read-only/shadow → assisted → automated), prioritized by
  value ÷ risk, with go/no-go metrics for each phase.
```

> Technique: [[Agentic Workflow Patterns]] plus [[Gate Checks]]. This is the operations-wide version of IT library prompt 8.

## 30. Operations Change Communication

**Use when:** you're rolling out a change (new uptime standard, install gate, incident roles, reorg) and every team needs to understand why it matters.

```text
ROLE: You write internal change communications for an operations organization.

THE CHANGE: {what, when, who's affected, why (tie to churn/uptime data), what's NOT changing}
AUDIENCES: NOC engineers, CS agents, field techs, directors/managers.

For each audience write:
- A ≤150-word message in their language (techs: practical, what's different on Monday;
  CS: what to tell customers; NOC: process detail)
- "What this means for you" in 3 bullets
- The 3 questions they'll likely ask, with honest answers
Plus: a 5-minute talking-points script for team huddles, and a feedback channel.
MUST: connect the change to customer impact with one real number; acknowledge the effort it asks.
MUST NOT: blame a team for the problem being solved; use corporate filler.
```

> Technique: multi-audience generation with content [[Gate Checks]]. The same facts are written differently for each team.

---

## Key Takeaways

- **Start with prompts 2 and 13.** Define uptime the same way everywhere, then measure how much it drives churn. Every investment decision afterward can be justified in churn dollars.
- **Look at the handoffs between departments** (11, 12, 25, 26). That's where outages turn into cancellations, because no single director owns those gaps.
- **Field quality affects churn too.** Install gates (20), avoidable truck rolls (19) and repeat dispatches (22) are retention levers, not just cost levers.
- **Design in the prompt, compute in code.** The early-warning score (8), uptime metric (13) and Pareto (14) should run as queries. The LLM designs them and explains the results.
