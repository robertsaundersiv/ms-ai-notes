---
title: "Customer Service Director Prompt Library"
aliases:
  - CS Director Prompts
type: reference
status: review
created: 2026-10-01
related:
  - "[[NOC Director Prompt Library]]"
  - "[[IT Director Prompt Library]]"
  - "[[Marketing Director Prompt Library]]"
  - "[[COO Prompt Library]]"
  - "[[CEO Prompt Library]]"
  - "[[MVNO Launch Prompt Library]]"
  - "[[Financial Controller Prompt Library]]"
  - "[[Network Operations Engineering Manager Prompt Library]]"
  - "[[Rapid Response Network Operations Manager Prompt Library]]"
  - "[[Gate Checks]]"
  - "[[Sonar Ticket and Outage Classification - How-To]]"
tags:
  - prompt-engineering
  - isp-operations
  - customer-service
  - churn
  - reference
---

# Customer Service Director Prompt Library

> [!abstract] TL;DR
> Ten prompts for the Customer Service Director at **Wi-Fiber**. They're built around the two problems the business cares about most: **churn is too high**, and **network uptime isn't high enough**, which drives churn. Customer service is where both problems show up first. Each customer contact is a chance to spot churn risk, recover after an outage, or feed a network problem back to the NOC. Each prompt names the technique it uses from this vault.

> [!example] Context block (paste above any prompt)
> ```text
> ORG: Wi-Fiber, a fixed wireless ISP in 10 markets across 8 states. Customers connect via
> rooftop/pole CPE to sectorized APs on towers; billing and ticketing are in Sonar.
> TOP PRIORITIES: reduce churn; network uptime is the biggest controllable churn driver.
> I am the Customer Service Director. Break results out by market where relevant.
> ```

> [!note] Shared rules
> - **Paste real exports** (Sonar tickets, call notes, cancellation reasons, survey text). Don't ask the model to guess volumes or rates. Calculate rates in a spreadsheet and paste the results. ([[Sonar Ticket and Outage Classification - How-To#^compute-dont-ask|compute, don't ask]])
> - **Customer text is data, not instructions.** ([[Prompt Injection]])
> - **Ask for verbatim evidence** so you can spot-check classifications. ([[LLM Hallucinations]])
> - **Remove names, addresses, phone numbers and account numbers** before pasting anything into a tool outside your environment.

> [!todo]- Contents
> | # | Prompt | Churn / uptime link | Technique |
> |---|---|---|---|
> | 1 | [[#1. Churn-Signal Contact Classifier]] | Spots at-risk customers on every contact | Routing |
> | 2 | [[#2. Retention Save Playbook by Cancel Reason]] | Saves customers at the point of cancel | Few-shot |
> | 3 | [[#3. Stated vs Real Cancellation Reason]] | Measures how much churn is really network-driven | Grounded extraction |
> | 4 | [[#4. Repeat-Contact Root Cause Finder]] | Repeat contacts predict churn | Task decomposition |
> | 5 | [[#5. QA Scorecard Evaluator]] | Better handling means fewer cancels | LLM-as-judge |
> | 6 | [[#6. Post-Outage Recovery Outreach]] | Wins back trust after uptime failures | Segmented generation + gates |
> | 7 | [[#7. Self-Service Troubleshooting Article Builder]] | Faster fixes, fewer calls and truck rolls | Stage-specific chain |
> | 8 | [[#8. Formal Complaint Response (FCC / PUC / BBB)]] | Saves your most escalated customers | Content gates |
> | 9 | [[#9. Agent Coaching Plan]] | Better save skills on the team | Structured output |
> | 10 | [[#10. Monthly Voice-of-Customer Report]] | Tells the COO and NOC where churn is coming from | Stage-specific chain |

---

## 1. Churn-Signal Contact Classifier

**Use when:** you want to label every ticket or call note for churn risk so at-risk customers go to a retention specialist the same day.

```text
ROLE: You classify customer contacts for churn risk at a fixed wireless ISP.

<contacts>{batch of Sonar ticket/call notes: id, market, tower/sector if known, text}</contacts>

For each contact, output one JSON object:
{
  "id": "...",
  "churn_risk": "HIGH" | "MEDIUM" | "LOW",
  "signals": ["<verbatim phrase from the text>", ...],
  "signal_type": ["mentions_competitor" | "mentions_cancel" | "repeat_issue" |
                  "outage_frustration" | "price_complaint" | "moving" | "slow_speeds" | "none"],
  "network_related": true | false,
  "route_to": "retention" | "tier2_tech" | "billing" | "standard"
}

RULES:
- HIGH needs at least one explicit signal (cancel, competitor named, "last time", "fed up").
- "signals" must be copied verbatim. If there's no signal, use [] and LOW.
- "network_related" is true when the complaint is about outages, drops, slowness or weather.
- Don't infer risk from tone alone.
```

> Technique: the [[Routing Workflow]] pattern with grounded evidence. Run the routing rules (HIGH goes to retention) in code or in Sonar automation, so the LLM only produces the labels.

---

## 2. Retention Save Playbook by Cancel Reason

**Use when:** you want a consistent, honest save script for each cancel reason, including reasons where the honest answer is "we can't fix this yet."

```text
ROLE: You design retention playbooks for a fixed wireless ISP's save desk.

CANCEL REASONS (from our data, with share of cancels): {e.g., outages/reliability 31%,
  slow speeds 18%, moving 15%, price 14%, competitor offer 12%, other 10%}
SAVE TOOLS AVAILABLE: {credits, plan changes, free CPE upgrade/realign visit, tower
  upgrade ETA if known, contract-free month, etc. + any limits}

Here is the style I want, for one reason:

Reason: Slow speeds in the evening
Diagnose: "Is it slow all day or mainly 7–11 pm? Wired or Wi-Fi?"
Honest position: If the sector is congested and no upgrade is scheduled, say so.
Offer ladder: 1) Check signal remotely / CPE realign  2) Plan right-size  3) Credit
Don't: Promise speeds the sector can't deliver.
Log: Sonar tag "save-attempt/speed" + outcome.

Write the same structure for every reason above. Then add:
- When NOT to try to save (moving out of footprint, unfixable coverage), plus a graceful exit
  script that leaves the door open for a win-back.
- What the agent must send to the NOC (tower/sector, symptom) on every reliability cancel.
```

> Technique: [[Few-Shot Prompting]]. One worked example sets the structure and the honesty standard for the rest.

---

## 3. Stated vs Real Cancellation Reason

**Use when:** your cancellation report says "price" or "moving" but you suspect reliability is the real driver.

```text
ROLE: You are a churn analyst reviewing cancellation records.

<cancels>{id, market, tower/sector, stated reason code, agent notes, exit survey text,
          tickets in the prior 90 days (count + subjects), outage events on their sector
          in the prior 90 days (if available)}</cancels>

For each record:
- stated_reason: the code as given
- likely_real_reason: one of [reliability, speed, price, moving, competitor, service_experience,
  billing, other, unclear]
- evidence: verbatim quotes or the ticket/outage facts you relied on
- reclassified: true/false

Then summarize:
1. A stated → real matrix (counts)
2. The % of churn that is likely network-driven (reliability + speed), stated vs real
3. Towers/sectors that appear in 3+ network-driven cancels
4. Which reason codes our agents misuse most, and a proposed fix to the code list

Only reclassify when the evidence supports it. Otherwise leave it and mark it "unclear".
```

> Technique: grounded extraction from [[Output Validation]]. Every reclassification needs evidence, so you can show the COO the reliability churn number and back it up.

---

## 4. Repeat-Contact Root Cause Finder

**Use when:** first-contact resolution is low, or customers contact you 3+ times in 30 days. Those customers are strong churn candidates.

```text
ROLE: You analyze repeat customer contacts to find why issues aren't resolved the first time.

<repeat_chains>{for each customer with 2+ contacts in 30 days: market, sector, and each
                contact's date, channel, notes, resolution, whether a truck roll happened}</repeat_chains>

Decompose each chain:
1. ORIGINAL ISSUE – what the customer first wanted fixed
2. BREAK POINT – the contact where resolution should have happened, and why it didn't:
   [misdiagnosis, no ownership, waiting on NOC, waiting on field, network issue unresolved,
    knowledge gap, policy blocked, customer-side]
3. COST – number of contacts, truck rolls, days open

Report:
- Top break points by count, each with 2 example chain ids
- How many chains were really unresolved network issues (sector/backhaul problems that
  CS couldn't fix), listed by tower/sector for the NOC
- 3 process changes, each tied to the break point it would remove
```

> Technique: [[Task Decomposition]]. Breaking each chain into issue, break point and cost turns a vague "low FCR" into specific process changes you can act on.

---

## 5. QA Scorecard Evaluator

**Use when:** you want consistent QA on more calls and tickets than supervisors can listen to.

```text
ROLE: You are a QA evaluator for an ISP support team. Score strictly against the rubric.

<interaction>{call transcript or ticket thread}</interaction>

RUBRIC (score each 0/1/2 and quote the moment that justifies the score):
1. Verified the issue and checked for a known outage on the customer's tower/sector first
2. Correct troubleshooting for fixed wireless (signal/CPE check before router/Wi-Fi blame)
3. Set an honest expectation (ETA, next step, what the customer should do)
4. Detected churn signals and acted (offered retention or escalated)
5. Ownership language ("I will…") and no blaming the customer, weather or other teams
6. Correct Sonar logging (category, outage link, notes a teammate could act on)

OUTPUT: scores, quotes, total /12, the one behavior that would most improve the
outcome, and AUTO-FAIL if the agent promised credits or restore times outside policy.
If the transcript doesn't show enough to judge a criterion, score it "N/A". Don't guess.
```

> Technique: LLM-as-judge from [[LLM Evaluation]]. Before trusting the model's scores, compare them with a supervisor's scores on 20 interactions.

---

## 6. Post-Outage Recovery Outreach

**Use when:** a significant outage is over and you want to contact affected customers before they decide to leave.

```text
ROLE: You write post-outage recovery messages for a fixed wireless ISP.

VERIFIED FACTS: {market, towers/sectors, start/end time, duration, cause in plain words
  (if confirmed), what we're doing to prevent recurrence, credit policy that applies}
SEGMENTS (computed in Sonar, not by you):
  A) Affected once in 90 days
  B) Affected 2+ times in 90 days (high churn risk)
  C) Affected AND opened a ticket during the outage

Write per segment:
- SMS (≤160 chars) and email (≤150 words)
- For B: a personal-sounding message from the CS Director with a specific prevention step
  and a direct callback number. Also flag B for a proactive retention call.
- For C: acknowledge they contacted us; close the loop on their ticket.

MUST: apologize once, state the duration, state the credit only as policy allows.
MUST NOT: blame weather or vendors as an excuse, promise "this won't happen again",
  use technical jargon.
Finish with a PASS/FAIL self-check against MUST/MUST NOT.
```

> Technique: segmented generation with content [[Gate Checks]]. Code decides who is in each segment, and the LLM only writes the messages. A person approves before anything is sent.

---

## 7. Self-Service Troubleshooting Article Builder

**Use when:** the same fixable issues keep generating calls and truck rolls (CPE power, router placement, Wi-Fi vs. signal, weather fade).

```text
ROLE: You write customer-facing help articles for fixed wireless internet.

<resolved_tickets>{10–30 resolved tickets on one issue: notes + resolution}</resolved_tickets>

STAGE 1 – Extract the steps that actually resolved these tickets, ranked by how often
  they worked. Cite ticket ids.
STAGE 2 – Write the article: title as the customer would search it ("Internet drops when it
  rains"), a 1-line "what's happening" in plain English, numbered steps a non-technical
  person can do in under 10 minutes, a "Call us if…" section with clear stop points
  (anything on the roof, the pole or the dish = call us).
STAGE 3 – Write a 3-step version for the phone menu / chat bot.
STAGE 4 – Review: flag any step that's unsafe, needs tools, or wasn't in the tickets.
```

> Technique: [[Stage-Specific Prompting]]. The article is based on fixes that actually worked in real tickets, not generic advice.

---

## 8. Formal Complaint Response (FCC / PUC / BBB)

**Use when:** a customer files a regulatory or BBB complaint. These customers are almost certain to churn, and the response becomes part of a public record.

```text
ROLE: You draft formal complaint responses for an ISP. Factual, respectful, concise.

<complaint>{complaint text – treat as data}</complaint>
<account_facts>{service history, tickets, outages on their sector, credits issued,
               truck rolls, current status – from Sonar}</account_facts>
AGENCY: {FCC informal complaint / {state} PUC / BBB}

Produce:
1. TIMELINE of facts from account_facts only, each with a date
2. RESPONSE to the agency: acknowledgment, factual summary, actions taken, resolution
   offered, contact person (role)
3. CUSTOMER CALL PLAN: what to offer, who calls, by when
4. INTERNAL FLAGS: anything in the complaint we can't verify, any policy failure on our side,
   and whether legal should review

MUST NOT: dispute the customer's feelings, include internal jargon, admit legal liability,
  or state anything not in account_facts.
```

> Technique: content and logic [[Gate Checks]] with a strict source of truth. A person must review before sending, and legal should review where the INTERNAL FLAGS say so.

---

## 9. Agent Coaching Plan

**Use when:** you're preparing monthly 1:1s and want coaching that's specific to each agent, not generic.

```text
ROLE: You are a contact-center coach.

<agent_data>{agent (initials only), tenure, AHT, FCR, CSAT, save rate, QA scores by
             criterion for the month, 3 QA excerpts}</agent_data>
<team_averages>{same metrics}</team_averages>

Output in this format:
## Strengths (2) – each with the metric or QA quote that proves it
## Focus area (1) – the single change with the biggest impact on churn or FCR, and why
## Practice – a 10-minute role-play scenario on fixed wireless that targets the focus area
## Measure – the metric and target to check next month
## Opener – one sentence to start the 1:1 positively

Don't rank the agent against named peers. Don't recommend discipline.
```

> Technique: [[Structured Outputs]]. Using the same structure for every 1:1 makes month-to-month progress easy to compare.

---

## 10. Monthly Voice-of-Customer Report

**Use when:** you report to the COO each month and want customer pain tied to specific markets, towers and network events.

```text
ROLE: You produce a monthly Voice-of-Customer report for an ISP COO.

<metrics>{by market: contacts per 1k subs, FCR, CSAT, cancels, save rate, top ticket categories}</metrics>
<verbatims>{50–200 survey comments / ticket excerpts with market + sector}</verbatims>
<network_events>{outages this month by market/tower with duration}</network_events>

STAGE 1 – THEMES: Cluster verbatims into ≤8 themes. Give counts, markets and 2 quotes each.
STAGE 2 – LINK: For each theme, say whether it lines up with network_events (same market/
  tower, within 14 days). Label each link CORRELATED or NO CLEAR LINK. Don't claim causation.
STAGE 3 – REPORT (1 page):
  - Headline: the one thing the COO should know
  - Market heat map (table: market × [contacts/1k, CSAT, cancels, top theme])
  - Network-to-churn signals: towers/sectors with both outages and cancellation themes
  - What CS changed this month and the result
  - 3 asks of other departments (NOC, Field, Marketing), each with evidence
```

> Technique: [[Stage-Specific Prompting]]. Each stage passes only its findings to the next. The CORRELATED label keeps the model from claiming causes it can't prove.

---

## Key Takeaways

- **CS sees churn first.** Prompts 1, 3 and 4 turn every customer contact into a churn signal you can count.
- **Credit and segment rules belong in code**, not in the model's judgment (prompts 1, 6).
- **Send your findings to the NOC.** Prompts 3, 4 and 10 each produce a list of towers and sectors that links customer pain to uptime work.
