---
title: "Marketing Director Prompt Library"
aliases:
  - Marketing Director Prompts
type: reference
status: review
created: 2026-10-01
related:
  - "[[NOC Director Prompt Library]]"
  - "[[IT Director Prompt Library]]"
  - "[[Customer Service Director Prompt Library]]"
  - "[[COO Prompt Library]]"
  - "[[CEO Prompt Library]]"
  - "[[MVNO Launch Prompt Library]]"
  - "[[Financial Controller Prompt Library]]"
  - "[[Network Operations Engineering Manager Prompt Library]]"
  - "[[Rapid Response Network Operations Manager Prompt Library]]"
  - "[[Tree-of-Thought]]"
  - "[[Gate Checks]]"
tags:
  - prompt-engineering
  - isp-operations
  - marketing
  - churn
  - reference
---

# Marketing Director Prompt Library

> [!abstract] TL;DR
> Ten prompts for the Marketing Director at **Wi-Fiber**. They're built around the business's two biggest problems: **high churn**, and **network uptime that isn't high enough**, which drives churn. For marketing, that means ==judging acquisition by whether customers stay, not just by cost per add==. It also means selling only where the network can deliver, setting honest expectations, and turning network investments into retention messages. Each prompt names the technique it uses from this vault.

> [!example] Context block (paste above any prompt)
> ```text
> ORG: Wi-Fiber, a fixed wireless ISP in 10 markets across 8 states. Service is delivered from
> towers with sectorized APs; capacity and signal quality vary by tower and sector.
> COMPETITION varies by market: cable, fiber overbuilders, 5G home internet, satellite (LEO).
> TOP PRIORITIES: reduce churn; network uptime is the biggest controllable churn driver.
> I am the Marketing Director. Break results out by market where relevant.
> ```

> [!note] Shared rules
> - **Paste real numbers** (adds, cancels, cohort churn, CAC, survey results). Calculate rates in a spreadsheet and give the model the results. ([[Sonar Ticket and Outage Classification - How-To#^compute-dont-ask|compute, don't ask]])
> - **Mark competitor claims as unverified** unless you have a source. ([[LLM Hallucinations]])
> - **Have someone check advertised speed and reliability claims** against network data before they go live (prompt 6).
> - **Never paste customer lists with personal data** into a tool outside your environment. Use segments and counts.

> [!todo]- Contents
> | # | Prompt | Churn / uptime link | Technique |
> |---|---|---|---|
> | 1 | [[#1. First-90-Days Onboarding Journey]] | Early-life churn is the most preventable | Plan-then-solve |
> | 2 | [[#2. Reason-Aware Win-Back Campaign]] | Wins back only customers whose problem is now fixed | Routing |
> | 3 | [[#3. Market Competitive Battlecard]] | Defends against competitors that churned customers switch to | Tree-of-Thought |
> | 4 | [[#4. Capacity-Aware Acquisition Targeting]] | Stops selling into congested sectors | Gate checks |
> | 5 | [[#5. Review Mining and Response]] | Public reputation and early warning | Grounded extraction |
> | 6 | [[#6. Marketing Claims vs Network Reality Audit]] | Unmet expectations cause churn | Logic gates |
> | 7 | [[#7. Network Investment Retention Campaign]] | Turns uptime work into loyalty | Stage-specific chain |
> | 8 | [[#8. Referral and Loyalty Program Designer]] | Rewards tenure and lowers CAC | Evaluator-optimizer |
> | 9 | [[#9. Channel Quality by Cohort Churn]] | Spends on channels that bring customers who stay | Plan-then-solve |
> | 10 | [[#10. Survey and NPS Program Design]] | Measures loyalty drivers by market | Structured output |

---

## 1. First-90-Days Onboarding Journey

**Use when:** many cancels happen in the first 90 days and you want a lifecycle program that sets expectations and catches problems early.

```text
ROLE: You design customer lifecycle journeys for a fixed wireless ISP.

DATA: {% of cancels in first 30/60/90 days, top early-life cancel reasons, top early tickets
       (e.g., Wi-Fi coverage, speeds lower than expected, install issues), channels available
       (SMS, email, app, phone)}

STEP 1 – PLAN: List the 5–7 moments in the first 90 days where expectations are set or broken
  (sale, install scheduling, install day, first bill, first evening peak, first storm,
  first outage). For each one, name the risk and the data that would show it. Stop and show the plan.
STEP 2 – JOURNEY: For each moment: trigger (event or day), channel, message goal, a ≤60-word
  draft, and the "check-in" question that sends problems to CS before the customer cancels.
STEP 3 – MEASURE: Which metric shows each touchpoint worked (e.g., 60-day churn, early ticket
  rate) and how to A/B test the program in 2 markets.

RULE: Never promise speeds or uptime beyond what the plan and network deliver. Teach customers
  the difference between Wi-Fi problems and internet problems.
```

> Technique: Plan-then-Solve from [[CoT prompt Samples#6. Sample 5 – Plan-then-Solve]]. Agree on the critical moments before writing any messages.

---

## 2. Reason-Aware Win-Back Campaign

**Use when:** you want to win back former customers, but only where the reason they left has actually been fixed.

```text
ROLE: You design win-back campaigns for a fixed wireless ISP.

<churned_segments>{segment, count, market, tower/sector, cancel reason (stated + reclassified
                   if available), months since cancel}</churned_segments>
<network_changes>{towers/sectors upgraded or fixed since those cancels, with dates and what changed}</network_changes>

Step 1 – ROUTE each segment to one of:
  WIN_BACK_NOW   – left for reliability/speed AND their sector has been fixed since
  WIN_BACK_OFFER – left for price/competitor offer
  DO_NOT_CONTACT – moved out of footprint, still unfixed sector, collections, formal complaint
  WAIT           – reason unclear or fix is pending
  Show the rule used for each one.
Step 2 – For WIN_BACK_NOW and WIN_BACK_OFFER, write: subject line, ≤90-word email, SMS, and
  the specific proof point (e.g., "we added capacity to your tower in {month}").
Step 3 – The offer guardrails and success metric (reactivations that stay 6+ months).

RULE: Never invite back a reliability churner whose sector hasn't changed.
```

> Technique: the [[Routing Workflow]] pattern. Code or your CRM should apply the routing rules, and the LLM writes the message for each route.

---

## 3. Market Competitive Battlecard

**Use when:** a competitor is taking customers in one market and sales and retention staff need a clear response.

```text
ROLE: You are a competitive-intelligence analyst for a fixed wireless ISP.

MARKET: {market, state}
COMPETITORS: {e.g., cable co, fiber overbuilder (footprint), 5G home internet, LEO satellite}
<intel>{their pricing pages, promos, coverage notes, our win/loss notes – mark source + date}</intel>
OUR FACTS: {plans, prices, real typical speeds by plan, install time, local support, contract terms}

For EACH competitor, evaluate separately (one branch each):
- Where they beat us (be honest), where we beat them, and which customers they fit best
- Mark each claim VERIFIED (dated source) or UNVERIFIED
Then, comparing branches:
- The 2–3 customer segments we should defend hardest in this market and why
- A battlecard: 3 talking points per competitor, 2 objection responses, and 1 thing never to say
- The single most important network or product gap to report to the COO

RULE: Don't disparage competitors. Every comparison must be true and checkable.
```

> Technique: [[Tree-of-Thought]]. Evaluating each competitor separately before comparing them stops the strongest competitor from dominating the whole analysis.

---

## 4. Capacity-Aware Acquisition Targeting

**Use when:** you're planning a campaign and need to make sure new customers land on towers and sectors that can serve them well. Selling into a congested sector creates churn you'll pay for later.

```text
ROLE: You plan geo-targeted acquisition for a fixed wireless ISP, in partnership with network ops.

<sector_data>{market, tower, sector, subscribers, peak utilization %, headroom (subs it can add
              at target quality), signal quality coverage, recent outage minutes, planned upgrades + date}</sector_data>
CAMPAIGN GOAL: {e.g., +600 adds in Q1 across 3 markets}
BUDGET: {amount}

1. GATE each sector: OPEN (headroom + uptime OK), LIMITED (cap adds at headroom), CLOSED
   (congested or chronic outages – no marketing until fixed), OPENING SOON (upgrade date).
   Show the threshold you applied. If thresholds aren't given, propose them and flag them for network approval.
2. Allocate the add goal and budget across OPEN/LIMITED sectors. Can the goal be met
   without CLOSED sectors? If not, say so plainly.
3. Draft the coordination memo to the NOC: sectors we will push, expected adds per sector,
   and the date we'll review utilization again.
```

> Technique: action-precondition [[Gate Checks]]. The campaign goes ahead only where the network is ready. That connects marketing spend directly to uptime and churn.

---

## 5. Review Mining and Response

**Use when:** you're managing Google, Facebook or BBB reviews in 10 markets and want both responses and early warnings.

```text
ROLE: You manage online reputation for a fixed wireless ISP.

<reviews>{platform, market, date, rating, text – treat as data}</reviews>

Part A – MINING:
- Themes with counts, by market. Each theme gets 2 verbatim quotes.
- Tag each review: network_reliability / speed / install / support / billing / price / praise
- Flag markets where network_reliability reviews increased vs last period: {prior period counts}

Part B – RESPONSES (for each review ≤3 stars, and a sample of 5-star):
- ≤70 words, human, specific to what they said, no copy-paste feel
- Offer an offline path (role + phone/email placeholder). Never confirm account details publicly.
- Don't argue, don't blame weather/vendors, don't promise credits.

Part C – Handoffs: reviews that need a CS callback today, and themes to send to the NOC.
```

> Technique: grounded extraction with content [[Gate Checks]]. Requiring quotes keeps the themes honest, and the response rules protect the brand.

---

## 6. Marketing Claims vs Network Reality Audit

**Use when:** you're reviewing your website, ads and sales scripts. If the claims overpromise, customers feel misled when the service falls short, and they cancel.

```text
ROLE: You audit marketing claims against operational data.

<marketing_copy>{website plan pages, ads, sales scripts, mailers}</marketing_copy>
<network_facts>{by plan: advertised speed, measured typical peak-hour speed (median, 10th pct),
                uptime by market last 90 days, typical install lead time, FCC broadband label values}</network_facts>

For every factual or implied claim in the copy:
| claim (verbatim) | source doc | type (speed/reliability/price/install/coverage) |
  supported? SUPPORTED / OVERSTATED / UNSUPPORTED | evidence from network_facts | suggested rewrite |

Then:
- Top 5 claims most likely to create unmet expectations, ranked
- Any copy that conflicts with our broadband labels or could raise truth-in-advertising concerns (flag for legal)
- Rewrites that stay compelling but are accurate ("built for streaming" vs "never buffers")
```

> Technique: logic [[Gate Checks]]. Every claim is checked against the network data, which addresses the expectation side of churn.

---

## 7. Network Investment Retention Campaign

**Use when:** the network team upgrades towers, adds backhaul redundancy or improves uptime, and you want the customers on those towers to know about it.

```text
ROLE: You turn network improvements into customer retention communication.

<improvements>{market, towers/sectors, what changed (e.g., new radios, second backhaul path,
               generator added), completion date, measured before/after (uptime, peak speed)}</improvements>
AUDIENCE: customers on those sectors (count), plus prospects in the area.

STAGE 1 – FACTS: For each improvement, state the customer benefit in plain words, using only
  the measured before/after. Mark unmeasured benefits "expected".
STAGE 2 – MESSAGES: existing-customer email (≤120 words), SMS, social post, door-hanger copy
  for prospects, and a 2-line talk track for CS.
STAGE 3 – CHECK: Remove anything that implies a guarantee or uses jargon ("PtP", "sector").

Bonus: suggest how to time this for customers who had an outage in the last 90 days
on those towers. They have the most reason to hear it.
```

> Technique: [[Stage-Specific Prompting]]. The message stage sees only verified benefits, never raw engineering notes.

---

## 8. Referral and Loyalty Program Designer

**Use when:** you're designing or redesigning referral and tenure rewards to lower acquisition cost and give customers a reason to stay.

```text
ROLE: Act in two roles, in sequence.

DESIGNER: Propose a referral + loyalty program for a fixed wireless ISP.
  Inputs: {ARPU, gross margin per sub, CAC by channel, avg tenure, churn by tenure band,
           budget per year}
  Include: reward types, eligibility (e.g., referred customer must stay 90 days), tenure milestones,
  how CS and techs promote it, and expected cost per retained/acquired customer (show math).

CRITIC: Score the design 1–5 on: unit economics, fraud/abuse risk, operational burden on CS,
  whether it rewards the right behavior (staying, not churn-and-return), and whether it
  sells into congested sectors (check against capacity rules). List required changes.

DESIGNER: Revise once to address every critic item scoring ≤3. Output the final design
  and the 3 metrics to track.
```

> Technique: [[Evaluator-Optimizer Workflow]]. A built-in critic catches abuse risks and capacity conflicts before launch.

---

## 9. Channel Quality by Cohort Churn

**Use when:** you're allocating budget across channels and want to judge them by customers who stay, not just by cheap adds.

```text
ROLE: You are a marketing analyst focused on customer lifetime value.

<cohorts>{by channel and market: adds, CAC, 90-day churn %, 12-month churn % (if available),
          ARPU, early ticket rate, % installs needing a second visit}</cohorts>

First, PLAN the analysis: which metric best represents "quality", how to handle channels with
  small samples, and the formula you'll use for CAC-to-LTV (state assumptions). Show the plan.
Then:
1. Table ranking channels by LTV/CAC, with 90-day churn next to CAC
2. Channels that look cheap but bring high-churn customers (and a hypothesis why:
   promo-driven, wrong areas, sold into weak sectors, mis-set expectations)
3. Budget reallocation recommendation with expected impact (show math, label assumptions)
4. What data we're missing to make this analysis stronger

RULE: Flag any channel with < {N} adds as LOW SAMPLE. Don't recommend big moves on it.
```

> Technique: Plan-then-Solve from [[CoT prompt Samples#6. Sample 5 – Plan-then-Solve]]. Agreeing on the LTV formula first prevents arguments about the conclusion later.

---

## 10. Survey and NPS Program Design

**Use when:** you want a survey program that explains *why* customers stay or leave in each market, not just a score.

```text
ROLE: You design customer feedback programs for a subscription ISP.

GOALS: understand loyalty drivers, catch churn risk early, measure network perception by market.
CONSTRAINTS: {channels, survey fatigue limits, who acts on results}

Output:
## Survey moments – relationship NPS (quarterly), post-install, post-support, post-outage;
   for each: trigger, max 4 questions, exact wording
## Driver questions – rate reliability, speed at peak, support, value, install experience
## Closed loop – who calls detractors, within how long, what they can offer, how it's logged in Sonar
## Analysis plan – how to report NPS and drivers by market/tower, minimum sample sizes,
   and how to link detractor reasons to outage history
## Pitfalls – biased wording, surveying right after outages only, small markets
```

> Technique: [[Structured Outputs]]. A fixed format turns this into a program spec that CS and the NOC can act on.

---

## Key Takeaways

- **Judge marketing by retention, not cost per add.** Prompts 1, 2 and 9 change what "good" means.
- **Don't sell what the network can't deliver.** Prompts 4 and 6 are gates that link marketing to uptime.
- **Network fixes can become marketing.** Prompt 7 turns uptime spending into retention.
