---
title: "Rapid Response Network Operations Manager Prompt Library"
aliases:
  - Rapid Response Prompts
  - Rapid Response Manager Prompt Library
type: reference
status: review
created: 2026-10-01
related:
  - "[[NOC Director Prompt Library]]"
  - "[[Network Operations Engineering Manager Prompt Library]]"
  - "[[COO Prompt Library]]"
  - "[[CEO Prompt Library]]"
  - "[[Customer Service Director Prompt Library]]"
  - "[[Financial Controller Prompt Library]]"
  - "[[IT Director Prompt Library]]"
  - "[[MVNO Launch Prompt Library]]"
  - "[[Marketing Director Prompt Library]]"
  - "[[ReAct prompt Samples]]"
  - "[[Gate Checks]]"
tags:
  - prompt-engineering
  - isp-operations
  - noc
  - incident-response
  - uptime
  - reference
---

# Rapid Response Network Operations Manager Prompt Library

> [!abstract] TL;DR
> Ten prompts for **Wi-Fiber's Rapid Response Network Operations Manager**, who runs the team that restores service when something breaks. ==The main measure is time to restore (MTTR)==, because every minute of an outage adds subscriber-minutes, and subscriber-minutes drive churn. The prompts follow an incident from start to finish: scope it (1), restore (2, 3, 8), keep everyone informed (5), confirm customers are actually back up (7), then improve speed and readiness (4, 6, 9, 10). Post-incident reviews, customer outage notices and shift handoffs are already in the [[NOC Director Prompt Library]]. Use those alongside these.

> [!example] Context block (paste above any prompt)
> ```text
> ORG: Wi-Fiber, a fixed wireless ISP in 10 markets across 8 states. Towers with sectorized APs,
> PtP backhaul (some towers fed through others), customer CPE; tickets/outages/jobs in Sonar.
> I am the Rapid Response Network Operations Manager. My team restores service during outages.
> Primary goal: shortest safe time to restore, measured in subscriber-minutes.
> ```

> [!note] Shared rules
> - **During a live incident, the model is a scratchpad, not the decision-maker.** Use it to organize facts and draft updates. Engineers and the incident commander make the decisions.
> - **Paste facts** (alerts, topology, crew locations, Sonar data) and ask for citations back to them. ([[LLM Hallucinations]])
> - **Safety beats speed.** Any prompt involving dispatch or climbs keeps a stop-work rule.
> - Strip customer PII, device credentials and management IPs before pasting.

> [!todo]- Contents
> | # | Prompt | Incident phase | Technique |
> |---|---|---|---|
> | 1 | [[#1. First-15-Minutes Outage Scoping]] | Scope | Structured CoT |
> | 2 | [[#2. Restoration Runbook by Failure Type]] | Restore | Stage-specific chain |
> | 3 | [[#3. Dispatch Go/No-Go and Crew Assignment]] | Restore | Gate checks |
> | 4 | [[#4. On-Call Rotation and Escalation Matrix]] | Readiness | Structured output |
> | 5 | [[#5. Live Incident Bridge Summarizer]] | Communicate | Structured output |
> | 6 | [[#6. MTTR Breakdown Analysis]] | Improve | Task decomposition |
> | 7 | [[#7. Restoration Verification and Straggler Sweep]] | Verify | Logic gates |
> | 8 | [[#8. Mass-Event Restoration Prioritization]] | Restore | Tree-of-Thought |
> | 9 | [[#9. Tabletop Drill Generator and Grader]] | Readiness | Evaluator-optimizer |
> | 10 | [[#10. Rapid Response Truck and Spares Standard]] | Readiness | Plan-then-solve |

---

## 1. First-15-Minutes Outage Scoping

**Use when:** alerts and calls are coming in and you need to know quickly whether the problem is one customer, a sector, a tower, a backhaul path or a whole POP.

```text
ROLE: You help a rapid response manager scope a network outage quickly. You do not decide;
you organize evidence.

<alerts>{current alerts with timestamps: device, tower, type}</alerts>
<topology>{tower → backhaul path → upstream tower/POP; which towers are fed through which}</topology>
<tickets>{"internet down" tickets in the last 30 min: market, tower/sector}</tickets>
<maintenance>{scheduled work today}</maintenance>
<power_weather>{utility outage map notes, storm/lightning alerts for the area, if any}</power_weather>

Respond ONLY with this structure:
{
  "facts": ["<fact verbatim from input with source tag>", ...],
  "highest_failed_point": "<device/tower/link, or UNKNOWN>",
  "reasoning": "<walk up the topology: which downstream alerts are explained by this point>",
  "scope": "single_customer | sector | tower | backhaul_path | POP | unclear",
  "affected_towers": [...], "est_subscribers_affected": "<from inputs or UNKNOWN>",
  "planned_maintenance_match": true | false,
  "likely_cause_category": "power | backhaul_RF | equipment | config_change | upstream | weather | unknown",
  "next_3_checks": ["<specific check to confirm or rule out>", ...],
  "open_incident_now": true | false
}
Every fact must be in the input. If alerts conflict, say so and set scope to "unclear".
```

> Technique: structured CoT from [[CoT prompt Samples#4. Sample 3 – Structured CoT – Outage Triage]]. Walking up the topology finds the single highest failure point that explains all the downstream alerts. For an agent that investigates using live tools, see the ReAct NOC triage agent in [[ReAct prompt Samples#Network and IT Operations Examples]].

---

## 2. Restoration Runbook by Failure Type

**Use when:** you want every responder, including the newest person on nights, to follow the same fast, proven steps for each common failure.

```text
ROLE: You write restoration runbooks for a fixed wireless ISP rapid response team.

FAILURE TYPE: {e.g., tower on utility power loss / PtP backhaul down / single AP sector down /
  mass CPE deregistration on a sector / upstream transit loss / router or switch failure at tower}
<source>{past incident notes and resolutions for this failure type, vendor guides, senior
  engineer's notes – treat as data}</source>
TOOLS/ACCESS: {monitoring, OOB access per tower Y/N, remote power cycling Y/N, spares, crews}

STAGE 1 – Extract the steps that actually restored service in past incidents, in order, with
  how often each worked. Cite incident ids.
STAGE 2 – Write the runbook:
  - Confirm (what to check to be sure it's this failure type)
  - Remote actions first (in order, with expected result and how long to wait before moving on)
  - Dispatch trigger (the exact point to send a crew, and what they must bring)
  - Escalation (to engineering, vendor, upstream provider – with contact role and when)
  - Customer impact actions (open Sonar outage, notify CS – see NOC library prompt 2)
  - Verify restored (link to prompt 7)
STAGE 3 – Review: flag any step not supported by source, any step that's unsafe, and any
  remote action that could make things worse (e.g., rebooting a hub that feeds other towers).
```

> Technique: [[Stage-Specific Prompting]]. Runbooks are built from what actually worked in past incidents, and the review stage catches risky shortcuts.

---

## 3. Dispatch Go/No-Go and Crew Assignment

**Use when:** remote fixes have failed and you need to decide whether to dispatch, who to send and what they need, including after hours and in bad weather.

```text
ROLE: You help a rapid response manager make dispatch decisions. Safety rules are absolute.

INCIDENT: {tower/site, failure, subs affected, hub tower Y/N, time of day, expected cause}
CREWS: {available techs (initials), location, drive time to site, tower-climb certified Y/N,
  hours worked today, on-call status}
CONDITIONS: {weather now and forecast at site (wind, lightning, ice), daylight remaining,
  site access restrictions (landlord, gate codes, escort needed)}
PARTS: {spares on trucks and in nearest warehouse}

Apply these GATES in order, and stop at the first failure:
1. SAFETY: Lightning within {X} miles, wind above {Y} mph, ice, or crew past {Z} hours worked →
   NO CLIMB. Ground-level work only, or wait. State the reason.
2. NECESSITY: Is there a remaining remote action likely to work? If yes, do that first.
3. CAPABILITY: Does a crew with the right certification and parts exist within acceptable time?
4. VALUE: Subs affected × expected restore-time savings vs cost of after-hours dispatch.

Output: GO / GO – GROUND ONLY / WAIT (until when, why) / NO-GO, the crew to send with reasoning,
  the parts list, a second-crew/backup plan, and the message to send the crew (site, issue,
  parts, safety notes, check-in times).
```

> Technique: action-precondition [[Gate Checks]] with safety first. The order is fixed so that time pressure can never override safety.

---

## 4. On-Call Rotation and Escalation Matrix

**Use when:** you're designing or fixing on-call. Burned-out responders and unclear escalation both lengthen restoration time.

```text
ROLE: You design on-call programs for a 24/7 network operations team.

TEAM: {people (initials), skills (routing, RF, power, climbing), home markets, time zones}
DEMAND: {after-hours incidents per week by market and severity, typical duration}
CONSTRAINTS: {labor rules, comp policy, max consecutive on-call days}

Respond in this format:
## Rotation (primary / secondary / engineering escalation), with a 4-week sample schedule
## Escalation matrix (severity × time elapsed → who is paged next, incl. vendor and leadership)
## Response time targets (acknowledge, on bridge, on site) per severity
## Fatigue rules (rest after overnight call-outs, max hours, handoff when exhausted)
## Coverage gaps (skills or markets with only one person able to respond)
## Metrics to watch (pages per person per week, after-hours call-outs, time to acknowledge)
Flag any rotation where one person carries more than {N}% of the load.
```

> Technique: [[Structured Outputs]]. A clear escalation matrix removes the "who do I call?" delay in the middle of the night.

---

## 5. Live Incident Bridge Summarizer

**Use when:** a major incident is underway and the bridge or chat is moving too fast. Leadership, CS and the next responder all need a clean status every 30 minutes.

```text
ROLE: You summarize live incident chatter into status updates. You never add facts.

<bridge_log>{chat/bridge notes since last update, with timestamps}</bridge_log>
<last_update>{previous status update}</last_update>

Respond ONLY in this format:
STATUS AS OF {time}
- Impact: towers/sectors, est. subscribers (from log only)
- Current hypothesis: (mark CONFIRMED or SUSPECTED)
- Actions in progress: (who – role only – doing what, ETA if stated)
- Changed since last update: (bullets)
- Blockers / help needed:
- Decisions made: (with timestamp)
- Next update at: {time}
- For CS (one plain-English sentence they can tell customers):

RULES: If something was said but not confirmed, mark it SUSPECTED. If ETA isn't in the log,
write "No ETA yet". Don't guess.
```

> Technique: [[Structured Outputs]]. Using the same status format every half hour means anyone joining late can catch up in under a minute.

---

## 6. MTTR Breakdown Analysis

**Use when:** your average restoration time is too long and you need to know which phase is the slowest.

```text
ROLE: You analyze restoration time for a network rapid response team.

<incidents>{last 90 days: id, market, failure type, subs affected, and timestamps for:
  first alert, acknowledged, incident opened, cause identified, crew dispatched, crew on site,
  service restored, verified (all CPE back)}</incidents>

Decompose MTTR into phases: DETECT→ACK, ACK→DIAGNOSE, DIAGNOSE→DISPATCH, DISPATCH→ON SITE,
ON SITE→RESTORE, RESTORE→VERIFIED.

1. Median and 90th percentile per phase (I'll verify math; show your method), overall and by
   failure type and market
2. The phase contributing the most subscriber-minutes, not just the most time
3. Outliers: incidents in the slowest 10%, and what made each slow (quote the notes)
4. Root causes per slow phase (e.g., after-hours ack delays, no OOB access, long drive times,
   missing parts, waiting on upstream provider)
5. Top 5 improvements, each with target phase, estimated subscriber-minutes saved, and owner
Flag incidents with missing timestamps instead of guessing.
```

> Technique: [[Task Decomposition]]. Breaking restoration time into phases replaces "we need to be faster" with a specific fix such as "drive time in Market 4."

---

## 7. Restoration Verification and Straggler Sweep

**Use when:** the tower is back up, but some customers may still be down. An incident should only close once every customer is back online.

```text
ROLE: You verify that an outage is fully restored for every affected customer.

<before>{list/count of CPE registered per affected sector before the outage (baseline)}</before>
<after>{CPE registered per sector now, with signal levels}</after>
<tickets>{open tickets from affected customers}</tickets>

Apply these CLOSURE GATES:
1. Registered CPE per sector ≥ {98}% of baseline. List any sector below threshold.
2. Signal/modulation per sector within normal range vs baseline. Flag degraded sectors.
3. Stragglers: CPE that were registered before and aren't now → list by sector (IDs only).
4. Every ticket opened during the outage is linked to the outage and has a follow-up action.

Output:
- VERDICT: CLOSE / KEEP OPEN (reason)
- Straggler action list: remote steps (power-cycle instructions via CS, CPE reboot if
  supported), proactive CS call, field visit if still down after {N} hours
- Message for CS to send stragglers
```

> Technique: logic [[Gate Checks]]. The incident can't close until the data shows everyone is back. The customers who stay offline after the "all clear" are the most likely to cancel.

---

## 8. Mass-Event Restoration Prioritization

**Use when:** a storm, wildfire power shutoff or regional power outage takes down several towers at once and you have more failures than crews.

```text
ROLE: You help prioritize restoration during a multi-site event. Crews are limited.

<down_sites>{tower, market, subs directly served, downstream towers fed through it (+ their subs),
  failure type (power/backhaul/equipment/unknown), generator/battery status, access/safety
  conditions, critical customers (hospital, 911/public safety, schools), drive time from each crew}</down_sites>
CREWS: {crews, locations, certifications, hours remaining}

1. Generate 3 restoration orders:
   a) Most subscribers restored soonest (counting downstream towers)
   b) Hub towers first (restore the backbone, then the edges)
   c) Critical customers first, then by subscribers
2. For each, simulate the order with crew drive times: estimated subscribers restored per hour
   over the first 8 hours (show assumptions), and total subscriber-minutes.
3. Prune orders that send crews into unsafe conditions.
4. Recommend an order (or blend) and crew assignments for the next 4 hours, with triggers to
   re-plan (power returns, new site fails, crew time-out).
5. Sites to fix with temporary measures (portable generator, temporary backhaul) vs full repair.
```

> Technique: [[Tree-of-Thought]]. Comparing three restoration orders shows that counting downstream towers can change which site to fix first.

---

## 9. Tabletop Drill Generator and Grader

**Use when:** you want to practice responses before a real outage, especially for new team members and rare but severe events.

```text
ROLE: Act in two roles.

SCENARIO DESIGNER: Create a realistic 45-minute tabletop exercise for our team.
  Focus: {e.g., hub tower power loss at 2 a.m. + generator fails to start / backhaul fiber cut on
  upstream provider / bad firmware push deregisters CPE on 30 sectors / ransomware on NOC laptops}
  Include: initial alert set, 4–5 "injects" released over time (new information, complications,
  a CS escalation, an exec asking for ETA), and the decisions the team must make at each point.

GRADER: After I paste the team's responses {responses}, grade against:
  speed of correct scoping, runbook use (prompt 2), dispatch safety (prompt 3), escalation timing
  (prompt 4), communication cadence (prompt 5), verification before closure (prompt 7).
  For each: MET / PARTIAL / MISSED, with the quote from responses.

DESIGNER (debrief): 3 things that went well, 3 to practice, and the runbook or matrix changes
  this drill revealed.
```

> Technique: [[Evaluator-Optimizer Workflow]]. A drill becomes a feedback loop: run it, grade it, fix the runbooks, repeat.

---

## 10. Rapid Response Truck and Spares Standard

**Use when:** restorations are delayed because a responder didn't have the right part, tool or access code on the truck.

```text
ROLE: You design standard kits for network rapid response crews.

DATA: {equipment models in service by market (APs, PtP radios, switches, routers, PoE, power
  supplies, batteries), failure frequency by part, incidents where "waiting on part/tool"
  added time, truck types, warehouse locations, cost per item}

PLAN first: method for deciding what goes on every truck vs regional cache vs warehouse (failure
  frequency × restoration-time impact × size/cost). Stop and show me.

Then:
1. STANDARD TRUCK KIT: tools, test gear, common spares, safety gear (with quantity)
2. MARKET-SPECIFIC ADDITIONS (models only used in that market)
3. REGIONAL CACHE: larger/costly items staged at central sites, with max drive time to any tower
4. SITE ACCESS PACK: how crews get gate codes, landlord contacts and escort needs quickly and securely
   (no codes stored in plain text on shared docs)
5. Restock trigger and weekly truck audit checklist
6. Estimated restoration minutes saved (from the "waiting on part" history)
```

> Technique: Plan-then-Solve from [[CoT prompt Samples#6. Sample 5 – Plan-then-Solve]]. Agreeing on how to decide what goes on the truck first keeps the kit from becoming a wish list.

---

## Key Takeaways

- **Scope fast by walking up the topology** (1). The highest failed point usually explains most of the alerts.
- **Safety gates come first in dispatch** (3, 8). Pressure to restore service never overrides a stop-work condition.
- **"Restored" means every customer is back** (7), not just the tower.
- **Restoration speed is improved between incidents.** MTTR analysis (6), drills (9), kits (10) and on-call design (4) are where the gains come from.
