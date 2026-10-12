---
title: "CEO Prompt Library"
aliases:
  - CEO Prompts
  - Chief Executive Officer Prompt Library
type: reference
status: review
created: 2026-10-01
related:
  - "[[COO Prompt Library]]"
  - "[[NOC Director Prompt Library]]"
  - "[[IT Director Prompt Library]]"
  - "[[Customer Service Director Prompt Library]]"
  - "[[Marketing Director Prompt Library]]"
  - "[[MVNO Launch Prompt Library]]"
  - "[[Financial Controller Prompt Library]]"
  - "[[Network Operations Engineering Manager Prompt Library]]"
  - "[[Rapid Response Network Operations Manager Prompt Library]]"
  - "[[Tree-of-Thought]]"
  - "[[Gate Checks]]"
tags:
  - prompt-engineering
  - isp-operations
  - executive
  - churn
  - ebitda
  - reference
---

# CEO Prompt Library

> [!abstract] TL;DR
> Thirty prompts for the CEO of **Wi-Fiber**, built around four priorities: **lower churn, higher EBITDA, better customer sentiment, and long-term stability**. The four are connected. ==Churn is the main thing linking them==: every point of churn removed adds recurring EBITDA, lowers acquisition spend, improves sentiment and makes the company more durable. These prompts are for the CEO's own work: setting direction, making trade-offs, allocating capital, holding the leadership team accountable and managing the board. The day-to-day operational prompts are in the [[COO Prompt Library|COO]] and director libraries.

> [!example] Context block (paste above any prompt)
> ```text
> ORG: Wi-Fiber, a fixed wireless ISP in 10 markets across 8 states. Towers with sectorized APs,
> PtP backhaul, customer CPE; Sonar for billing and operations.
> LEADERSHIP: COO (Network Ops, Customer Service, Field Ops), CFO, Marketing Director, IT Director.
> CEO PRIORITIES: (1) lower churn, (2) increase EBITDA, (3) improve customer sentiment,
> (4) long-term stability of the company.
> I am the CEO. Be direct, quantify where my data allows, and flag trade-offs between priorities.
> ```

> [!note] Shared rules
> - **Financial numbers come from the CFO's models**, not the LLM. Paste the results and use the model for structure, scenarios, interpretation and writing. ([[Sonar Ticket and Outage Classification - How-To#^compute-dont-ask|compute, don't ask]])
> - **Label every number** as *actual*, *calc* (derived from your inputs) or *assumption*. ([[LLM Hallucinations]])
> - **Check competitor, regulatory and funding-program details** against current sources before acting. The model's knowledge may be out of date.
> - **Keep board materials, financials, deal discussions and personnel matters** in tools your company has approved for confidential data.

> [!todo]- Contents
> | # | Prompt | Priority | Technique |
> |---|---|---|---|
> | 1 | [[#1. CEO Monthly Business Review]] | All four | Structured output |
> | 2 | [[#2. Three-Year Strategic Plan]] | Stability | Tree-of-Thought |
> | 3 | [[#3. Priority Trade-Off Decision Memo]] | All four | Self-consistency |
> | 4 | [[#4. Board Meeting Narrative]] | All four | Content gates |
> | 5 | [[#5. Executive Scorecard Cascade]] | All four | Stage-specific chain |
> | 6 | [[#6. CEO Time and Attention Audit]] | All four | Structured output |
> | 7 | [[#7. The Value of One Point of Churn]] | Churn / EBITDA | Plan-then-solve |
> | 8 | [[#8. Leadership Team Churn Interrogation]] | Churn | Orchestrator-workers |
> | 9 | [[#9. Price Increase Churn Risk]] | Churn / EBITDA | Tree-of-Thought |
> | 10 | [[#10. Customer Value Segmentation]] | Churn / EBITDA | Task decomposition |
> | 11 | [[#11. Retention Initiative Portfolio Review]] | Churn | Evaluator-optimizer |
> | 12 | [[#12. Competitive Threat Assessment by Market]] | Churn / Stability | Parallelization |
> | 13 | [[#13. Unified Customer Sentiment Index]] | Sentiment | Structured output |
> | 14 | [[#14. CEO Customer Listening Session]] | Sentiment | Grounded extraction |
> | 15 | [[#15. CEO Letter to Customers]] | Sentiment | Content gates |
> | 16 | [[#16. Customer Promise and Experience Principles]] | Sentiment | Stage-specific chain |
> | 17 | [[#17. Local Reputation and Community Standing]] | Sentiment / Stability | Parallelization |
> | 18 | [[#18. Employee Sentiment to Customer Sentiment]] | Sentiment | Grounded extraction |
> | 19 | [[#19. EBITDA Bridge]] | EBITDA | Task decomposition |
> | 20 | [[#20. Cost-to-Serve and Market Profitability]] | EBITDA | Plan-then-solve |
> | 21 | [[#21. Churn-Safe Cost Reduction]] | EBITDA / Churn | Logic gates |
> | 22 | [[#22. Capital Allocation Framework]] | EBITDA / Stability | Tree-of-Thought |
> | 23 | [[#23. Revenue Growth Levers]] | EBITDA | Plan-then-solve |
> | 24 | [[#24. Vendor and Contract Portfolio Review]] | EBITDA / Stability | Few-shot |
> | 25 | [[#25. Enterprise Risk Register]] | Stability | Checklist gate |
> | 26 | [[#26. Liquidity and Downside Stress Test]] | Stability | Plan-then-solve |
> | 27 | [[#27. Technology Durability Roadmap]] | Stability | Tree-of-Thought |
> | 28 | [[#28. Funding, Grants and Subsidy Screening]] | Stability / EBITDA | Gate checks |
> | 29 | [[#29. Succession and Leadership Bench]] | Stability | Structured output |
> | 30 | [[#30. Strategic Options and M&A Screen]] | Stability | Self-consistency |

---

# A. Strategy and Executive Cadence

## 1. CEO Monthly Business Review

**Use when:** you prepare your monthly review with the leadership team, and you want all four priorities on one page.

```text
ROLE: You prepare a CEO's monthly business review.

<data>{this month vs last month vs plan vs same month last year, total and by market:
  CHURN: churn %, cancels by reason bucket (network / service / commercial / uncontrollable), saves
  EBITDA: revenue, ARPU, gross margin, opex by function, EBITDA, EBITDA margin, capex, FCF
  SENTIMENT: NPS, CSAT, review rating, complaints (FCC/PUC/BBB)
  STABILITY: cash, liquidity runway, covenant headroom, uptime, key risks status, key hires/departures}</data>
<exec_updates>{one paragraph from each leader}</exec_updates>

Respond ONLY in this format:
## The one thing (the most important development and what I should do about it)
## Four-priority scorecard (table: priority | key metric | actual | plan | trend | status R/Y/G)
## Connections (where one priority moved another this month, e.g., outage → churn → EBITDA)
## Market outliers (best and worst 2 markets and why, from the data)
## Leadership asks (decisions each leader needs from me)
## Questions I should ask in the meeting (5, pointed, evidence-based)
Use only numbers from <data>. Mark anything derived "(calc)".
```

> Technique: [[Structured Outputs]]. The "Connections" section makes the review show how the four priorities affect each other.

## 2. Three-Year Strategic Plan

**Use when:** you're setting long-term direction: which markets, which technologies, and grow vs. optimize.

```text
ROLE: You are a strategy advisor to the CEO of a regional fixed wireless ISP.

<inputs>{market-level: subs, penetration of serviceable homes, churn, EBITDA margin,
  competitive landscape (cable, fiber builds incl. subsidized, 5G home internet, LEO satellite),
  network condition; company: balance sheet, capex capacity, team strengths}</inputs>

1. Generate 3–4 distinct strategic paths (e.g., "deepen and harden existing 10 markets",
   "selective fiber overlay in dense pockets", "expand to adjacent rural markets",
   "optimize for cash and strategic sale").
2. Evaluate each path separately against the four priorities (churn, EBITDA, sentiment,
   stability), plus capital required and execution risk. State the assumptions.
3. Prune paths that the balance sheet can't fund or that leave us exposed to the
   most likely competitive threat.
4. Recommend a path (or sequence). Give 3-year milestones, the 3 bets we're making, the
   signposts that would make us change course, and what we will NOT do.
```

> Technique: [[Tree-of-Thought]]. Comparing complete strategies keeps the plan from just continuing what the company already does.

## 3. Priority Trade-Off Decision Memo

**Use when:** a decision pits your priorities against each other, for example cutting opex for EBITDA when it could hurt churn and sentiment.

```text
ROLE: Act as four independent advisors. Each answers separately without seeing the others.

DECISION: {e.g., reduce CS headcount 15% / delay tower power upgrades 1 year / raise prices $5}
DATA: {relevant financials, churn data, sentiment data, risk factors}

ADVISOR 1 – CFO lens: EBITDA and cash impact over 12 and 36 months.
ADVISOR 2 – Customer lens: churn and sentiment impact; who feels it first.
ADVISOR 3 – Operator lens: what breaks operationally; second-order effects.
ADVISOR 4 – Board/lender lens: long-term stability, covenant and valuation impact.

Each: recommendation (do / don't / modify), the 2 strongest reasons, confidence 0–100%.

SYNTHESIS: Where they agree, where they conflict and why, a modified option that
  captures most of the upside with less downside, and the metric and threshold that would
  trigger a reversal.
```

> Technique: [[CoT prompt Samples#5. Sample 4 – Self-Consistency|Self-Consistency]] using personas. If the advisors disagree, the decision really does involve a trade-off. Run each advisor in a separate chat for real independence.

## 4. Board Meeting Narrative

**Use when:** you're preparing the quarterly board meeting and need a clear story, not a stack of slides.

```text
ROLE: You help an ISP CEO prepare board meetings.

<facts>{quarter results vs plan, four-priority scorecard, major events, initiatives,
  risks, asks}</facts>

Produce:
1. NARRATIVE ARC (≤1 page): Where we are, what we learned, where we're going, what we need.
   Lead with the bad news if there is any.
2. DECK OUTLINE: ≤12 slides, each with a headline that states the conclusion
   (e.g., "Outage-driven churn fell 30%; reliability capex is paying back")
   and the chart or table that proves it.
3. LIKELY BOARD QUESTIONS (8), each with a direct answer and the backup data needed.
4. ASKS: approvals needed, written as resolutions.

MUST: give every metric with its comparison (plan or prior); separate facts from forecasts.
MUST NOT: bury misses, use operational jargon, or claim causation without evidence.
Then self-check each rule PASS/FAIL.
```

> Technique: content [[Gate Checks]]. The rules require candor, and the self-check catches spin.

## 5. Executive Scorecard Cascade

**Use when:** you're setting annual goals and need every leader's targets to add up to your four priorities without conflicting.

```text
ROLE: You help a CEO cascade company goals to the executive team.

COMPANY TARGETS: {churn X%→Y%, EBITDA $A→$B, NPS N→M, stability: liquidity/uptime/risk targets}
LEADERS: COO (NOC, CS, Field), CFO, Marketing Director, IT Director. Current baselines: {…}

STAGE 1 – For each company target, list the leaders who influence it and how.
STAGE 2 – Draft 3–4 measurable goals per leader, each mapped to a company target.
STAGE 3 – CONFLICT CHECK: find goals that push against each other (e.g., Marketing adds vs
  COO uptime in congested sectors; CFO opex cuts vs CS save rate). For each conflict, propose a
  shared goal or guardrail.
STAGE 4 – Incentive check: what behavior each goal rewards, and whether any could be gamed
  (e.g., reclassifying cancel reasons, excluding outages from uptime).
```

> Technique: [[Stage-Specific Prompting]]. The conflict and gaming checks are what make the cascade hold up during the year.

## 6. CEO Time and Attention Audit

**Use when:** you suspect your calendar doesn't match your four priorities.

```text
ROLE: You are an executive coach analyzing how a CEO spends time.

<calendar>{last 4–6 weeks of meetings: title, duration, attendees (roles), recurring Y/N}</calendar>
PRIORITIES: churn, EBITDA, customer sentiment, long-term stability (+ external: board, lenders, community)

Output:
## Time allocation (table: priority/category | hours | % | what it should be, with reasoning)
## Meetings to cut, delegate or shorten (with who should own them instead)
## Missing time (e.g., no direct customer contact, no frontline time, no long-term strategy block)
## Proposed weekly template (blocks by priority)
## One habit to start (e.g., listen to 5 cancel calls per week)
Classify each meeting from its title and attendees. Mark ambiguous ones "UNSURE" and don't guess.
```

> Technique: [[Structured Outputs]]. Comparing your actual calendar with your stated priorities shows the gaps.

---

# B. Churn

## 7. The Value of One Point of Churn

**Use when:** you want everyone, including the board, to understand churn reduction in dollars.

```text
ROLE: You are a subscription-business financial analyst.

DATA: {subscribers, ARPU, gross margin %, monthly churn %, CAC, avg install cost,
  EBITDA, valuation multiple range used by our board/lenders}

PLAN first: define formulas for (a) LTV, (b) annual revenue retained per 0.1 pt monthly churn
  reduction, (c) acquisition spend avoided to maintain the same subscriber base, (d) EBITDA impact,
  (e) implied enterprise value impact. Show formulas and stop.
Then compute with my numbers:
1. Table: churn reduced by 0.1 / 0.25 / 0.5 pt → revenue, EBITDA, avoided CAC, EV impact
2. Break-even: how much per year we could spend on retention or reliability per 0.1 pt and
   still increase EBITDA
3. A 3-sentence version for all-hands and a 3-sentence version for the board
Label each figure (calc) or (assumption).
```

> Technique: Plan-then-Solve from [[CoT prompt Samples#6. Sample 5 – Plan-then-Solve]]. This gives the company one shared number for comparing every churn and reliability investment.

## 8. Leadership Team Churn Interrogation

**Use when:** churn isn't improving and you want to question each leader's view with evidence before the next exec meeting.

```text
ROLE: You orchestrate a cross-functional churn investigation for a CEO.

Step 1 (orchestrator): From <churn_summary>{churn by reason, market, tenure, outage exposure}</churn_summary>,
  write 3 sharp questions for each leader that their data should answer.
Step 2 (workers – analyze each separately, using only that leader's data):
  COO <coo_data>{uptime, outage minutes by market, CS metrics, field metrics}</coo_data>
  Marketing <mktg_data>{acquisition by channel/market, 90-day churn by cohort, promos}</mktg_data>
  CFO <cfo_data>{pricing changes, billing issues, collections, credits}</cfo_data>
  For each: answers, evidence, and what the data CAN'T answer.
Step 3 (orchestrator): A synthesis for the CEO:
  - Root causes ranked by churn impact, with the leader who owns each
  - Contradictions between leaders' explanations
  - Gaps no one owns
  - 5 commitments to ask for at the meeting (owner, metric, date)
```

> Technique: [[Orchestrator-Workers Workflow]]. Each leader's data is analyzed separately, and the orchestrator brings out contradictions and gaps nobody owns.

## 9. Price Increase Churn Risk

**Use when:** a rate increase is the fastest way to raise EBITDA, but you're worried about churn and sentiment.

```text
ROLE: You advise a CEO on pricing decisions for a subscription ISP.

DATA: {plans + prices, subs per plan by market, historical churn response to past increases
  (if any), competitor prices by market, uptime by market, NPS by market, cost inflation}

1. Generate 3–4 pricing options (e.g., across-the-board $X, tiered by plan, increase paired with
   a speed upgrade, grandfather long-tenure, exempt markets with poor uptime).
2. Evaluate each separately: incremental revenue (gross), expected extra churn (state the
   elasticity assumption and its range), net EBITDA at 12 months, sentiment risk, regulatory/
   notice requirements by state to verify.
3. Prune options with negative net EBITDA under the pessimistic churn assumption.
4. Recommend one, with: which markets to exclude (low uptime = high risk), the customer
   communication approach, CS save-desk preparation, and the churn tripwire that triggers a rollback.
```

> Technique: [[Tree-of-Thought]] with optimistic and pessimistic branches. Testing against the pessimistic case protects you from too-optimistic elasticity estimates.

## 10. Customer Value Segmentation

**Use when:** you want to know which customers are worth fighting for, and where you're keeping customers at a loss.

```text
ROLE: You are a customer-profitability analyst.

<segments>{segment definitions + per segment: subs, ARPU, gross margin, cost to serve (support
  contacts, truck rolls, credits), churn %, tenure, NPS, sector congestion exposure}</segments>

Decompose:
1. Profitability per segment = revenue − direct cost − cost to serve (use my numbers; show math)
2. LTV per segment using churn
3. Classify each segment: PROTECT (high value, at risk), GROW (high value, stable),
   FIX (low value due to fixable cost-to-serve, e.g., poor signal installs), REPRICE, or
   ACCEPT (low value, low cost, stable)
4. For each class: the strategy, owner, and what not to do (e.g., don't discount PROTECT
   customers whose real problem is reliability)
```

> Technique: [[Task Decomposition]]. Splitting profitability into its parts shows which segments can be fixed and which need repricing.

## 11. Retention Initiative Portfolio Review

**Use when:** several churn initiatives are underway and you need to decide which to scale, fix or stop.

```text
ROLE: Act in two roles.

ANALYST: For each initiative {name, owner, cost to date, monthly cost, target, measured
  result, how it was measured, start date}, assess: churn impact (measured vs claimed),
  cost per retained subscriber, comparison to the value of a saved subscriber {from prompt 7},
  and strength of evidence (controlled test / before-after / anecdotal).

SKEPTIC: Challenge each assessment. Was there a control group? Did something else change
  (season, price, outage-free month)? Is the metric gameable? Downgrade the evidence rating where warranted.

ANALYST (final): Classify each initiative SCALE / FIX / STOP / TEST PROPERLY. Give the
  reallocation of budget, and the 2 initiatives to run as controlled tests next quarter.
```

> Technique: [[Evaluator-Optimizer Workflow]]. The skeptic stops initiatives from getting credit for churn changes they didn't cause.

## 12. Competitive Threat Assessment by Market

**Use when:** you're judging which markets face a serious competitive threat in the next 1–3 years (subsidized fiber builds, cable upgrades, 5G home internet, LEO satellite).

```text
ROLE: You are a competitive strategist for a fixed wireless ISP.

<market_intel>{per market: known/announced competitor builds and dates, subsidy awards in our
  footprint, competitor pricing, our share, our uptime, our NPS, our churn to each competitor –
  each item with source + date}</market_intel>

Assess EACH market separately (don't blend):
  - Threat level 1–5 with timeline, citing dated intel; mark undated items UNVERIFIED
  - Our defensibility: reliability, price, local service, coverage where others won't build
  - Strategic posture: DEFEND (invest), DIFFERENTIATE, HARVEST (maximize cash), or EXIT/PARTNER
Then aggregate:
  - Portfolio view: subscribers and EBITDA at high threat
  - The 3 moves that most improve company-wide defensibility
  - Intel gaps to close (who should research what, by when)
```

> Technique: [[Parallelization Workflow]]. Assessing each market separately avoids blurring them into a single national view.

---

# C. Customer Sentiment

## 13. Unified Customer Sentiment Index

**Use when:** NPS, CSAT, reviews and complaints each tell a different story and you want one trusted measure.

```text
ROLE: You design customer sentiment measurement for executive reporting.

SOURCES: {NPS (relationship), CSAT (post-contact), online review ratings + volume, formal
  complaints, social mentions, cancel-reason data}, with volume, frequency and known biases for each.

Design:
1. A composite Sentiment Index: components, weights, normalization, minimum samples, and
   rationale. Weight toward sources that predict churn (validate with our data; mark untested weights).
2. Reporting: company, by market, by customer segment. Monthly trend with confidence bands.
3. Driver attribution: how to show which experiences (outages, support, install, billing,
   price) move the index.
4. Guardrails against gaming (surveying only happy customers, review gating).
5. What a "real" improvement looks like vs noise.
```

> Technique: [[Structured Outputs]] for a measurement spec. Weighting by how well each source predicts churn connects sentiment back to the money.

## 14. CEO Customer Listening Session

**Use when:** you want to read the voice of the customer yourself, unfiltered, once a month.

```text
ROLE: You prepare raw customer voice for a CEO, with minimal filtering.

<verbatims>{100–300 items: survey comments, reviews, cancel notes, complaint excerpts,
  each with market, tenure, source – personal details removed}</verbatims>

Output:
## 10 quotes I must read (verbatim, chosen for representativeness, not shock value;
   include 3 positive)
## Themes (≤7) with counts, markets, and 2 quotes each
## What customers say we promised vs what they got
## Surprises (themes that don't appear in management reports)
## 3 customers I should personally call (by record id + why)
Every claim needs a quote. Never paraphrase a quote.
```

> Technique: grounded extraction from [[Output Validation]]. You read the customers' own words, not someone else's summary.

## 15. CEO Letter to Customers

**Use when:** after a rough period (outages, a price change) or a major investment, a direct message from the CEO can restore trust.

```text
ROLE: You ghostwrite customer letters for a regional ISP CEO. Voice: plain, accountable, local.

SITUATION: {what happened or what's changing, who's affected, facts with numbers}
WHAT WE'RE DOING: {specific investments/changes with dates}
WHAT CUSTOMERS GET: {credits, upgrades, commitments – exactly as approved}

Write: email (≤250 words), a shorter SMS/app version, and a social version.
MUST: take responsibility in the first 3 sentences, give one specific commitment with a date,
  provide a direct way to reach a real person.
MUST NOT: blame weather/vendors/customers, use "we apologize for any inconvenience",
  promise "this will never happen again", or include anything not in the inputs.
Self-check every rule PASS/FAIL, then provide a version for each of 2 hardest-hit markets
  with a local detail.
```

> Technique: content [[Gate Checks]]. The rules ban the corporate phrases that hurt trust.

## 16. Customer Promise and Experience Principles

**Use when:** you want a short set of service commitments that every department uses to make decisions.

```text
ROLE: You help a CEO define a customer promise and experience principles.

INPUTS: {top cancel reasons, top sentiment themes, what customers praise us for, competitor
  promises, what we can actually deliver operationally today and in 12 months}

STAGE 1 – Find the 3 things customers value most that we can credibly own (cite inputs).
STAGE 2 – Draft a one-sentence customer promise and 4–5 experience principles
  (e.g., "We tell you before you tell us" for outages).
STAGE 3 – For each principle: what it means for NOC, CS, Field, Marketing and Billing; the
  metric that proves we keep it; and the current gap.
STAGE 4 – Reality check: flag any principle we can't deliver within 12 months and rewrite it
  or add the investment needed.
```

> Technique: [[Stage-Specific Prompting]]. The final reality-check stage keeps the promise from becoming a slogan.

## 17. Local Reputation and Community Standing

**Use when:** you want to strengthen Wi-Fiber's standing in each of the 10 communities. For a local ISP, community standing affects sentiment, permits, tower access and resilience against competitors.

```text
ROLE: You advise on community relations for a multi-market regional ISP.

PER MARKET: {local presence (office, staff, techs who live there), sponsorships, municipal/
  county relationships, school/library partnerships, local press coverage, review rating,
  pending permits/tower issues, competitor community activity}

For EACH market separately:
  - Reputation strengths and weaknesses (cite inputs)
  - 3 low-cost, high-trust actions (e.g., free service for a community center, storm-response
    visibility, local hiring stories)
  - Key relationships to build (roles, not names) and why
Then company-wide: a 12-month community calendar, a budget split by market weighted by
  competitive threat (prompt 12), and how to measure impact on sentiment.
```

> Technique: [[Parallelization Workflow]]. Planning each community separately keeps the plan local rather than corporate.

## 18. Employee Sentiment to Customer Sentiment

**Use when:** you want to test whether frontline engagement (CS agents, techs) is affecting customer experience.

```text
ROLE: You analyze the link between employee and customer experience.

<employee_data>{engagement survey results by team and market (anonymized), turnover by role and
  market, open comments}</employee_data>
<customer_data>{CSAT, NPS, repeat dispatch, FCR, churn by market}</customer_data>

1. Employee themes from the comments (≤6), with counts and quotes, by role (CS vs field vs NOC)
2. Markets where low engagement or high turnover lines up with weak customer metrics (label as
   CORRELATION, with the numbers)
3. Root causes employees cite that also hurt customers (tools, staffing, unclear ownership, pay)
4. 3 CEO-level actions and the employee and customer metric each one should move
Keep groups at least {N} people so no individual can be identified.
```

> Technique: grounded extraction with correlation labeling. This keeps employee issues from being dismissed as anecdotes.

---

# D. EBITDA

## 19. EBITDA Bridge

**Use when:** EBITDA moved and you need to explain exactly why.

```text
ROLE: You explain EBITDA variances for a subscription ISP.

<financials>{EBITDA prior period and current period; revenue split into subscriber volume,
  ARPU/price, mix, other; costs split into network (backhaul, tower leases, power), CS, field,
  marketing/CAC, G&A, credits/bad debt}</financials>

1. Build an EBITDA bridge (prior → current) with each driver's contribution (show math).
   Split volume into adds vs churn.
2. Classify each driver: STRUCTURAL (will persist) vs ONE-TIME vs TIMING.
3. Show the churn component explicitly: revenue lost to churn and the CAC spent replacing it.
4. Recurring EBITDA run-rate excluding one-time items.
5. The 3 drivers most worth managing next quarter, with owner.
Use only numbers provided. Flag anything that doesn't add up.
```

> Technique: [[Task Decomposition]]. Every dollar of change is assigned to a driver, and showing churn separately makes its cost visible.

## 20. Cost-to-Serve and Market Profitability

**Use when:** you want to know which of the 10 markets actually create value after fully loaded costs.

```text
ROLE: You are an FP&A analyst for a multi-market ISP.

<market_pl>{per market: revenue, subs, direct network cost (tower leases, backhaul, power),
  field cost, CS cost (allocated by contacts), marketing, credits, allocated G&A (method stated),
  maintenance capex}</market_pl>

PLAN first: allocation method choices and their bias. Stop and show.
Then:
1. Market contribution margin and EBITDA-minus-maintenance-capex per sub (table, ranked)
2. Cost-to-serve per sub by component; the outlier component in each weak market
3. Link to churn and uptime: are high cost-to-serve markets also high-churn/low-uptime? (correlation)
4. For each bottom-3 market: FIX (specific cost or churn lever), REPRICE, or STRATEGIC REVIEW
Mark every allocation-sensitive conclusion.
```

> Technique: Plan-then-Solve. Agreeing on the allocation method first stops the result from depending on how G&A happens to be spread.

## 21. Churn-Safe Cost Reduction

**Use when:** you need to cut opex for EBITDA without causing churn that costs more than the savings.

```text
ROLE: You evaluate cost-reduction proposals for churn and sentiment risk.

<proposals>{each: description, annual savings, function, what changes for customers or frontline}</proposals>
CHURN VALUE: {$ per 0.1 pt churn from prompt 7}

For each proposal, apply the CHURN GATE:
1. Customer-touching? (Y/N + how)
2. Plausible churn/sentiment impact mechanism (e.g., longer hold times → saves drop;
   fewer spares → longer MTTR → outage churn)
3. Break-even: how much churn increase would wipe out the savings? (calc)
4. Verdict: SAFE (no customer touch), SAFE WITH GUARDRAIL (name the metric + tripwire),
   or BLOCK (break-even churn is implausibly small)
Then: total SAFE + GUARDRAILED savings, and 3 cost ideas that IMPROVE churn
  (e.g., avoidable truck roll reduction, self-service deflection).
```

> Technique: logic [[Gate Checks]] applied to cost decisions. A cut goes ahead only if its churn break-even is credible.

## 22. Capital Allocation Framework

**Use when:** you're splitting capex between growth, maintenance, reliability and technology refresh with limited capital.

```text
ROLE: You are a capital allocation advisor to an ISP CEO and board.

<projects>{each: category (growth / reliability / maintenance / refresh / IT), cost, timing,
  expected subs added or churn reduced or outage minutes avoided, payback assumptions, risk}</projects>
CAPITAL AVAILABLE: {amount}, HURDLE RATE: {x%}, CONSTRAINTS: {covenants, crew capacity}

1. Put every project in common units: NPV and EBITDA impact, using churn value {prompt 7}
   for reliability projects (show assumptions).
2. Build 3 portfolios (growth-heavy, reliability-heavy, balanced) within budget and crew capacity.
3. Evaluate each against the four priorities and stability (cash buffer remaining).
4. Recommend a portfolio, the projects just below the cut line, and the triggers to fund them.
```

> Technique: [[Tree-of-Thought]] across portfolios. Converting reliability projects into churn dollars lets them compete fairly with growth projects.

## 23. Revenue Growth Levers

**Use when:** you're looking for EBITDA growth beyond cost cuts: penetration, ARPU, new products.

```text
ROLE: You are a growth strategist for a regional ISP.

DATA: {serviceable homes/businesses per market and sector headroom, penetration, plan mix,
  ARPU, upsell rates, business/enterprise customers, managed Wi-Fi or other add-ons offered,
  churn by plan}

PLAN: list candidate levers (penetration in sectors with headroom, plan mix upgrades,
  business services, managed Wi-Fi/add-ons, MDU/community deals, rural expansion) and the
  data needed for each. Stop and show.
Then, for each lever: revenue and EBITDA potential over 24 months (calc with stated assumptions),
  capex needed, churn effect (some levers reduce churn, e.g., managed Wi-Fi), execution risk.
Rank by EBITDA per dollar invested and recommend the top 3 with first-90-day actions.
RULE: Penetration growth only in sectors with network headroom.
```

> Technique: Plan-then-Solve. Limiting growth to sectors with headroom keeps it from creating churn.

## 24. Vendor and Contract Portfolio Review

**Use when:** you're looking for EBITDA in your largest contracts (tower leases, backhaul and transit, equipment, software).

```text
ROLE: You review vendor contracts for savings and risk.

<contracts>{vendor, category, annual spend, term/renewal date, escalators, termination terms,
  SLA, performance history, alternatives}</contracts>

Examples of how I want each one classified:
- Tower lease, 3% annual escalator, renews in 8 months, few alternative structures →
  NEGOTIATE (escalator cap, term extension for rate), leverage: portfolio of sites with landlord
- Transit provider, 2 major outages this year, renewal in 14 months →
  RE-BID + add redundant provider; stability risk outweighs savings
- Software tool, 40% of licenses unused → RIGHT-SIZE now

For each contract: action (NEGOTIATE / RE-BID / RIGHT-SIZE / CONSOLIDATE / KEEP), estimated
  savings range, stability risk, deadline to act. Then a 12-month negotiation calendar.
```

> Technique: [[Few-Shot Prompting]]. The examples show that stability can matter more than price.

---

# E. Long-Term Stability

## 25. Enterprise Risk Register

**Use when:** you're keeping the company's top risks visible to you and the board.

```text
ROLE: You build enterprise risk registers for regional ISPs.

CONTEXT: {financial position, debt and covenants, key vendors, tower lease portfolio, spectrum
  holdings/licenses, technology age, key people, cyber posture, insurance, regulatory exposure by state}

Cover at least: competitive displacement, technology obsolescence, spectrum/licensing, tower
  lease concentration, upstream/backhaul concentration, cyber/ransomware, severe weather,
  key-person, liquidity/covenants, regulatory/subsidy changes, supply chain, labor availability.

For each risk: description, likelihood 1–5, impact 1–5 (in EBITDA/subs where possible),
  current controls, residual risk, owner role, leading indicator, next action.
Output a ranked table, a heat map summary, and the top 5 with mitigation plans.
Only rate controls described in CONTEXT. Mark others "UNKNOWN – verify".
```

> Technique: a checklist gate. A minimum list of risks keeps important ones from being left out.

## 26. Liquidity and Downside Stress Test

**Use when:** you want to confirm the company survives a bad year.

```text
ROLE: You are a CFO-level advisor running downside scenarios.

BASE CASE: {12–24 month forecast: subs, churn, ARPU, EBITDA, capex, debt service, cash}
COVENANTS: {terms}

PLAN the scenarios first and stop:
  - Churn shock (+0.5 pt for 6 months, e.g., competitor fiber launch in top 2 markets)
  - Major weather event (2 markets, capex + credits + churn)
  - Price pressure (−5% ARPU to defend share)
  - Combined plausible downside
Then, with results from our model {results}:
1. Cash low point, covenant headroom, months of runway for each scenario
2. Which scenario breaks first and why
3. A pre-agreed action ladder (levers in order, $ impact, decision trigger) that protects
   churn-critical spending (reliability, CS) for as long as possible
4. Financing moves to make now while things are good
```

> Technique: Plan-then-Solve. You approve the scenarios before running them, and the action ladder is agreed before it's needed.

## 27. Technology Durability Roadmap

**Use when:** you're judging whether today's network will still compete in 5–7 years against fiber, better 5G home internet and LEO satellite.

```text
ROLE: You are a wireless technology strategist.

CURRENT NETWORK: {radio platforms and ages, spectrum used (licensed/CBRS/unlicensed bands),
  backhaul, typical delivered speeds vs plans, capacity headroom}
CUSTOMER DEMAND TRENDS: {usage growth/yr, plan mix shift}

1. Project when current network capacity and speeds fall behind customer expectations and
   competitors (show assumptions).
2. Generate 3 technology paths (e.g., next-gen fixed wireless radios + more spectrum,
   selective fiber-to-the-home in dense pockets + wireless elsewhere, partnership/wholesale).
3. Evaluate each separately: capex, timeline, churn defense, EBITDA impact, execution risk,
   dependence on spectrum or subsidy outcomes.
4. Recommend a roadmap with decision points (dates) and the signposts that trigger each.
Mark technology claims that need vendor or engineering validation.
```

> Technique: [[Tree-of-Thought]]. Comparing several technology paths avoids betting the company on one roadmap.

## 28. Funding, Grants and Subsidy Screening

**Use when:** federal and state broadband programs could fund expansion or fortify your footprint, or could fund a competitor in your markets.

```text
ROLE: You screen broadband funding opportunities for a fixed wireless ISP.

<programs>{program name, administering agency/state, eligible technologies, eligible areas,
  match requirements, obligations (buildout deadlines, pricing/affordability rules, reporting),
  application deadline – each with a source link and date}</programs>
OUR FOOTPRINT: {markets, states, unserved/underserved areas we could reach}

For each program:
1. ELIGIBILITY GATE – Pass / Fail / Unclear on technology, geography, entity, match capacity.
   Quote the requirement. Never assume eligibility.
2. If pass: value, obligations, long-term cost (e.g., price caps, 10-year service commitments),
   and effect on EBITDA and stability.
3. DEFENSIVE VIEW: awards to competitors in our footprint, and challenge processes or deadlines
   to watch.
4. GO / NO-GO / MONITOR with the next step and owner.
Flag anything to verify with counsel or a grant specialist.
```

> Technique: an eligibility gate from [[Gate Checks]], with quoted program rules. Program details change often, so always check current sources.

## 29. Succession and Leadership Bench

**Use when:** you want the company to keep running well if a key leader leaves, including you.

```text
ROLE: You advise CEOs on succession and leadership bench strength.

<roles>{critical roles (CEO, COO, CFO, NOC Director, CS Director, network engineering lead,
  market managers…): incumbent tenure, flight risk (H/M/L), internal candidates (initials) with
  readiness (now / 1–2 yrs / 3+ yrs), undocumented knowledge they hold}</roles>

Output:
## Bench strength table (role | risk | ready-now successor? | gap)
## Key-person exposure (roles where one departure would hurt churn, uptime or lender confidence)
## Knowledge capture priorities (undocumented systems, vendor relationships, network design)
## Development plans for top 5 internal candidates (stretch assignment, mentor, timeline)
## Emergency succession plan (who acts in each critical role tomorrow)
## Retention actions for high-risk/high-impact people
```

> Technique: [[Structured Outputs]]. A standard format makes bench strength something the board can review every year.

## 30. Strategic Options and M&A Screen

**Use when:** you're evaluating acquisitions (neighboring wireless ISPs), divesting a market, partnerships, or a sale. These are decisions that permanently shape the company.

```text
ROLE: Act as three independent reviewers of a strategic option. Answer separately.

OPTION: {e.g., acquire WISP X (subs, markets, network condition, price), sell market Y,
  partner with fiber builder in market Z}
OUR POSITION: {financials, strategy from prompt 2, capital capacity}

REVIEWER 1 – STRATEGIST: Fit with the 3-year plan; churn, EBITDA, sentiment, and stability effects.
REVIEWER 2 – INTEGRATION OPERATOR: Network, systems (Sonar migration), CS and field integration
  risks; what typically goes wrong; realistic synergy timing.
REVIEWER 3 – PRE-MORTEM: "It's 2 years later and this deal destroyed value. Why?" (3 reasons)

SYNTHESIS: valuation drivers to diligence first, deal-breakers, a diligence checklist (network
  audit, churn by cohort, uptime history, customer sentiment, tower lease terms), and a
  recommendation: PURSUE / PURSUE WITH CONDITIONS / PASS.
```

> Technique: [[CoT prompt Samples#5. Sample 4 – Self-Consistency|Self-Consistency]] using personas, plus a pre-mortem. A pre-mortem brings up integration risks that deal enthusiasm tends to hide.

---

## Key Takeaways

- **Start with prompt 7.** Once one point of churn has a dollar value, churn, EBITDA, sentiment and stability can be compared in the same unit (used in 11, 20, 21, 22).
- **Check every EBITDA move against churn.** Prompts 9, 21 and 23 make sure EBITDA gains aren't paid for with future cancellations.
- **Sentiment is measurable and has an owner.** Prompts 13, 14 and 16 turn it into a metric, a habit and a set of principles.
- **Long-term stability is built in advance.** The stress test (26), risk register (25), succession plan (29) and technology roadmap (27) all assume a bad year is coming.
- **The CEO prompts set the agenda for the other libraries.** Prompt 8 questions the leaders using the analyses their own [[COO Prompt Library|COO]], [[Marketing Director Prompt Library|Marketing]] and [[Customer Service Director Prompt Library|CS]] prompts produce.
