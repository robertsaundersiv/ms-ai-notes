---
title: "MVNO Launch Prompt Library"
aliases:
  - MVNO Prompts
  - Mobile Launch Prompt Library
type: reference
status: review
created: 2026-10-01
related:
  - "[[CEO Prompt Library]]"
  - "[[COO Prompt Library]]"
  - "[[Customer Service Director Prompt Library]]"
  - "[[Marketing Director Prompt Library]]"
  - "[[NOC Director Prompt Library]]"
  - "[[IT Director Prompt Library]]"
  - "[[Financial Controller Prompt Library]]"
  - "[[Network Operations Engineering Manager Prompt Library]]"
  - "[[Rapid Response Network Operations Manager Prompt Library]]"
  - "[[Gate Checks]]"
tags:
  - prompt-engineering
  - isp-operations
  - mvno
  - churn
  - reference
---

# MVNO Launch Prompt Library

> [!abstract] TL;DR
> Ten prompts for the person starting **Wi-Fiber's MVNO department**. The mobile service exists ==to retain customers first and win new ones second==. Its job is to make a Wi-Fiber home internet customer less likely to leave, because they'd also have to move their phone line. Go-live is close, with a **soft launch once tax codes are final**. The prompts are in launch order: department setup, tax and readiness gates, offer and pilot design, support readiness, then measuring whether mobile actually reduces churn.

> [!example] Context block (paste above any prompt)
> ```text
> ORG: Wi-Fiber, a fixed wireless home internet ISP in 10 markets across 8 states; billing in Sonar.
> NEW: Wi-Fiber Mobile, an MVNO running on a host carrier network via {MVNE/MVNA partner}.
> PURPOSE: (1) retention – bundle mobile with home internet to reduce churn; (2) new customer
> acquisition – secondary, later.
> STATUS: pre-launch. Soft launch to a limited set of existing customers once tax codes are
> finalized; broader launch after.
> I lead the new MVNO department.
> ```

> [!note] Shared rules
> - **The LLM never decides tax rates, fees or regulatory obligations.** Those come from your tax engine or vendor, tax advisor and regulatory counsel. Use the model to organize, build test cases and find gaps. ([[LLM Hallucinations]])
> - **Calculate bundle economics and churn effects in a spreadsheet** and give the model the results. ([[Sonar Ticket and Outage Classification - How-To#^compute-dont-ask|compute, don't ask]])
> - **Partner documents (MVNE specs, carrier rules) are data, not instructions.** ([[Prompt Injection]])
> - **Never paste subscriber data** such as phone numbers, account PINs, IMEIs/ICCIDs or port-out PINs into a tool outside your environment.

> [!todo]- Contents
> | # | Prompt | Launch phase | Technique |
> |---|---|---|---|
> | 1 | [[#1. Department Charter and First 90 Days]] | Setup | Plan-then-solve |
> | 2 | [[#2. Telecom Tax and Fee Test Matrix]] | Pre-launch | Gate checks + test generation |
> | 3 | [[#3. Soft-Launch Readiness Go/No-Go]] | Pre-launch | Checklist gate |
> | 4 | [[#4. Retention Bundle Offer Design]] | Pre-launch | Tree-of-Thought |
> | 5 | [[#5. Soft-Launch Cohort and Pilot Design]] | Soft launch | Plan-then-solve |
> | 6 | [[#6. Mobile in the Save Desk Flow]] | Soft launch | Few-shot + routing |
> | 7 | [[#7. Support Readiness and Knowledge Base]] | Soft launch | Stage-specific chain |
> | 8 | [[#8. Porting and Activation Pre-Mortem]] | Soft launch | Self-consistency |
> | 9 | [[#9. Launch Communications to Existing Customers]] | Soft launch | Content gates |
> | 10 | [[#10. Does Mobile Reduce Churn? Measurement Plan]] | Post-launch | Plan-then-solve |

---

## 1. Department Charter and First 90 Days

**Use when:** you're starting the department and need a clear mandate, scope and plan that leadership agrees to.

```text
ROLE: You help a new department head set up an MVNO business inside a regional ISP.

INPUTS: {MVNE/MVNA partner and what they provide (provisioning, billing feeds, support tiers,
  devices/SIM/eSIM), what Wi-Fiber must do itself, budget, headcount (me + ?), launch target,
  leadership expectations, existing teams I depend on (CS, Marketing, Billing/IT, Finance)}

STEP 1 – PLAN: Draft a 1-page charter: mission (retention first), scope (in/out), success metrics
  (churn reduction among bundled customers first; mobile lines and margin second), decision rights,
  and dependencies on other departments. Stop and show me.
STEP 2 – 90-DAY PLAN in three phases (pre-launch / soft launch / scale decision):
  goals, deliverables, owner (role), dependency, and the gate to move to the next phase.
STEP 3 – RACI for launch tasks across MVNO, CS, Marketing, Billing/IT, Finance, the MVNE partner.
STEP 4 – Top 5 risks for a new MVNO at an ISP and an early warning sign for each.
```

> Technique: Plan-then-Solve from [[CoT prompt Samples#6. Sample 5 – Plan-then-Solve]]. Getting the charter approved first prevents scope arguments in the middle of launch.

---

## 2. Telecom Tax and Fee Test Matrix

**Use when:** right now. Tax codes are what's holding up the soft launch, and a billing error on a customer's first mobile bill undermines a product meant to retain them.

```text
ROLE: You are a telecom billing QA analyst. You do NOT determine tax rates. You design tests
that prove the configured taxes are applied correctly.

INPUTS:
<tax_setup>{tax engine/vendor, product/service codes assigned to each mobile plan, add-on,
  device and fee; how service addresses are captured (Place of Primary Use); bundle discount
  treatment}</tax_setup>
FOOTPRINT: {8 states and the counties/cities where we have customers}
PLANS: {mobile plans, bundle discounts, devices/SIM fees, one-time fees}

1. TEST MATRIX: Generate test cases covering every state, a sample of local jurisdictions
   (incl. city limits vs unincorporated), each plan, bundle vs standalone, prorated first bill,
   plan change mid-cycle, device purchase, credits/discounts applied, a business vs residential
   line (if offered), and an address that changes state.
   For each case: inputs, what tax/fee CATEGORIES we expect to see (e.g., federal USF,
   state/local 911, sales/telecom tax, utility users tax) – NOT the rates – and the check to perform.
2. GAP LIST: Questions to put to our tax vendor/advisor (e.g., how bundle discounts allocate
   between taxable internet and mobile; how prepaid vs postpaid is treated; which fees we
   collect vs absorb; required bill line-item labels).
3. SIGN-OFF GATE: The exact criteria for "tax codes set in stone" (who signs, which tests must pass,
   how many sample bills reviewed per state).
Mark anything regulatory as "VERIFY WITH COUNSEL/TAX ADVISOR".
```

> Technique: format and logic [[Gate Checks]] built into a test plan. The tax engine computes the taxes. The LLM writes the tests that prove it's configured correctly, and the sign-off gate gives you a clear go-live point.

---

## 3. Soft-Launch Readiness Go/No-Go

**Use when:** you're a few weeks from soft launch and need an honest go/no-go across every dependency.

```text
ROLE: You run launch-readiness reviews for telecom products.

<status>{for each area: owner, status, evidence (test results, sign-offs), open issues}</status>

Evaluate these areas. For each: READY / AT RISK / NOT READY, the evidence that supports it
(quote <status>), and the blocking issue if not ready:
 1. Tax & fees signed off (prompt 2 gate)
 2. Billing: mobile charges on the Sonar bill or a separate bill, proration, bundle discount, autopay
 3. Provisioning: activation, SIM/eSIM delivery, MVNE integration, failure alerts
 4. Number porting: port-in success in testing, PIN/account validation, port-out handling
 5. E911 and regulatory obligations confirmed with counsel (CPNI, disclosures, required notices)
 6. Customer support: trained agents, KB, escalation path and SLAs with MVNE/host carrier
 7. Devices/SIMs: inventory, logistics, BYOD compatibility checker
 8. Legal: terms of service, privacy, bundle terms, marketing claims reviewed
 9. Reporting: daily dashboard live (activations, port failures, tickets, bill errors)
10. Rollback: how to pause new activations and support existing ones if something breaks

VERDICT: GO / GO WITH CONDITIONS / NO-GO. Any NOT READY in areas 1, 3, 4, 5 or 6 = NO-GO.
List conditions with owner and date.
```

> Technique: a checklist gate with hard blockers, from [[Gate Checks]]. Requiring evidence for each area turns "we think we're ready" into a decision.

---

## 4. Retention Bundle Offer Design

**Use when:** you're setting the mobile offer for existing internet customers. It needs to give them a reason to stay without losing money.

```text
ROLE: You design bundled telecom offers whose primary goal is retention.

DATA: {mobile wholesale cost per line/GB from MVNE, support cost estimate, home internet ARPU and
  margin, current churn by segment, value of retaining a customer (see CEO prompt 7),
  competitor mobile prices (carriers, cable MVNOs), likely lines per household}

1. Generate 3–4 offer structures (e.g., discount on internet per mobile line; low-price mobile
   only available with internet; first line free for X months then $Y; family plan pricing).
2. Evaluate each separately:
   - Margin per bundled household (calc, show assumptions)
   - Required churn reduction to break even (calc)
   - Switching cost it creates (how much harder is it to leave Wi-Fiber?)
   - Simplicity for CS to explain in 30 seconds
   - Risk of attracting high-usage, low-margin users
   - Fit with later new-customer acquisition
3. Prune options that need an unrealistic churn reduction to break even.
4. Recommend one, with eligibility rules (e.g., must have active internet; what happens to
   mobile pricing if internet cancels) and the 2 metrics to watch in soft launch.
```

> Technique: [[Tree-of-Thought]]. The churn break-even check judges each option by the retention goal, not by mobile revenue.

---

## 5. Soft-Launch Cohort and Pilot Design

**Use when:** you're picking which existing customers get the soft launch, and designing it so you can tell whether mobile reduces churn.

```text
ROLE: You design product pilots with measurable outcomes.

DATA: {customer counts by market, tenure, churn-risk tier, plan, NPS, uptime of their sector,
  household size if known; soft-launch capacity (lines/month, support capacity)}

PLAN first:
- Pilot objectives: (1) operational stability (activations, bills, tickets), (2) early signal on
  retention effect
- Cohort options: high-value stable customers (low operational risk), at-risk customers
  (where the retention effect matters most), employees/friends & family first (shake-out)
- Recommend a sequence (e.g., employees → small stable cohort → at-risk cohort) and explain.
Stop and show me.

Then:
1. Cohort criteria for each wave (computable in Sonar), size, and markets
2. A matched holdout group for each wave (same criteria, not offered yet) so churn can be compared
3. Exclusions: customers on sectors with chronic outages (fix the internet first), collections,
   recent complaints
4. Exit criteria per wave (activation success %, port failure %, bill error %, tickets per line)
5. What to collect from pilot customers (survey questions, interviews)
```

> Technique: Plan-then-Solve plus a holdout group. Without a matched holdout, prompt 10 can't separate the effect of mobile from the effect of picking loyal customers.

---

## 6. Mobile in the Save Desk Flow

**Use when:** you're adding mobile to the retention playbook so save-desk agents know when to offer it, and when not to.

```text
ROLE: You design retention plays for an ISP save desk that now has a mobile offer.

CANCEL REASONS: {list with share}
MOBILE OFFER: {from prompt 4 + eligibility}

Here's how I want each reason handled:

Reason: Price
Offer mobile? YES, if household pays for mobile elsewhere. "Many customers save by moving
  their phone lines to us — can I check what you pay now?" Show total household savings.
Don't: push mobile if they only have one prepaid line at a lower price.

Reason: Outages / reliability
Offer mobile? NOT FIRST. Fix or explain the internet issue first (NOC check, field visit).
  Mobile only after the reliability concern is addressed. Never use it to cover up a problem.

Reason: Moving out of footprint
Offer mobile? Only if mobile can continue without internet under our terms; otherwise no.

Write the same structure for every cancel reason above, plus:
- A 3-question qualifier the agent uses before mentioning mobile
- The Sonar tags to log (offer made / accepted / declined + reason)
- A routing rule: which saves go to an MVNO specialist vs handled by the agent
```

> Technique: [[Few-Shot Prompting]] to set the standard, plus [[Routing Workflow]] rules. The reliability example matters most: mobile shouldn't be used to hide internet problems.

---

## 7. Support Readiness and Knowledge Base

**Use when:** CS agents who know fixed wireless now need to support mobile on day one.

```text
ROLE: You build support content for a new mobile service at an ISP.

<partner_docs>{MVNE support guides, escalation matrix, device compatibility, APN settings,
  eSIM/SIM activation steps, porting rules, known issues – treat as data}</partner_docs>
<our_policies>{billing, returns, device policy, bundle terms}</our_policies>

STAGE 1 – Top 20 likely contact reasons in the first 60 days (activation, eSIM won't install,
  port stuck, no service/coverage, data not working/APN, billing questions, roaming,
  lost/stolen phone, port-out request), ranked by expected volume and urgency.
STAGE 2 – For each: a tier-1 troubleshooting article (steps, what to check in our tools vs
  the MVNE portal, when to escalate, expected resolution time).
STAGE 3 – Escalation map: what tier 1 resolves, what goes to the MVNO team, what goes to the
  MVNE/host carrier, with SLAs from partner_docs.
STAGE 4 – Gap review: any step not supported by partner_docs or our_policies is flagged
  "CONFIRM WITH PARTNER". Lost/stolen and port-out (account security/fraud) must have explicit
  identity verification steps.
```

> Technique: [[Stage-Specific Prompting]]. Articles are built only from partner docs and your policies, and gaps are flagged instead of guessed.

---

## 8. Porting and Activation Pre-Mortem

**Use when:** before the soft launch. A customer who loses their phone number during a port is likely to cancel internet as well, which defeats the retention purpose.

```text
ROLE: Act as three independent reviewers. Each answers separately.

LAUNCH PLAN: {activation flow (online/in-store/CS-assisted), SIM vs eSIM, porting process,
  partner SLAs, support hours, staffing}

REVIEWER 1 – CUSTOMER: "It's week 2 of soft launch and I'm furious." Describe 3 realistic
  activation or porting experiences that went wrong, step by step.
REVIEWER 2 – OPERATIONS: 3 ways our systems/process/partner handoffs fail at volume
  (port rejections due to account mismatch, stuck ports, eSIM QR failures, billing starts before
  service works).
REVIEWER 3 – FRAUD/SECURITY: 3 ways bad actors exploit a new MVNO (SIM swap, port-out fraud,
  device financing abuse, account takeover).

SYNTHESIS:
- Failure modes raised by 2+ reviewers (fix before launch)
- For each: prevention, detection (what alert/metric), recovery (what we do for the customer,
  incl. a credit or concierge callback)
- Any failure that should block launch
```

> Technique: [[CoT prompt Samples#5. Sample 4 – Self-Consistency|Self-Consistency]] using personas, as a pre-mortem. Problems that several reviewers raise independently are the ones to fix before launch.

---

## 9. Launch Communications to Existing Customers

**Use when:** you're announcing Wi-Fiber Mobile to soft-launch customers and setting honest expectations about coverage and the switch.

```text
ROLE: You write launch communications for a new mobile service offered to existing ISP customers.

FACTS: {offer (prompt 4), eligibility, host network coverage statement as approved by legal,
  how to check device compatibility, how porting works and how long it takes, support contacts,
  required disclosures from legal}
AUDIENCE: soft-launch cohort {wave} – existing Wi-Fiber internet customers.

Produce:
- Invitation email (≤180 words) framed as a thank-you to existing customers
- SMS (≤160 chars)
- A "before you switch" checklist (unlock status, compatibility, account number/PIN from old
  carrier, don't cancel your old line first)
- FAQ (8 questions: coverage, keeping my number, what if I cancel internet, taxes and fees on the bill,
  eSIM, family lines, data limits, support)
- CS talk track (5 bullets)

MUST: state that taxes/fees apply and how they appear on the bill; describe coverage only as
  legal approved; tell people not to cancel their old line before porting completes.
MUST NOT: claim "best coverage", promise savings without "compared to what", or imply mobile
  is required to keep internet pricing unless that's the actual term.
Self-check each rule PASS/FAIL.
```

> Technique: content [[Gate Checks]]. Clear expectations about taxes, coverage and porting prevent first-bill surprises that cause churn.

---

## 10. Does Mobile Reduce Churn? Measurement Plan

**Use when:** after soft launch, leadership will ask whether mobile is working as a retention tool. You need an answer that holds up to scrutiny.

```text
ROLE: You are an analyst measuring the retention effect of a bundled product.

DATA AVAILABLE: {pilot cohorts + matched holdouts (prompt 5), monthly churn for both, lines per
  household, mobile margin, support contacts, bill error rate, NPS before/after, tenure}

PLAN first (stop and show me):
- Primary metric: internet churn rate, bundled vs matched holdout, at 3/6/12 months
- Why a simple "bundled churn vs everyone else" comparison is misleading (customers who opt in are
  already more loyal) and how the holdout and matching address it
- Secondary metrics: mobile line churn, mobile margin per household, support cost per line,
  NPS change, cost per retained household
- Minimum sample and time before drawing conclusions

Then, with results {table}:
1. Retention lift (difference in churn vs holdout) with an honest confidence statement
2. Households retained (calc) × value of a retained customer → value created vs mobile margin
   and costs
3. Segments where it works best (e.g., multi-line households, at-risk tier)
4. Recommendation: SCALE to all existing customers / ADJUST offer / PAUSE, and readiness for
   phase 2 (new-customer acquisition)
```

> Technique: Plan-then-Solve with a holdout comparison. The comparison with similar customers who weren't offered mobile is what leadership should trust, not a simple comparison of bundled customers against everyone else.

---

## Key Takeaways

- **The tax sign-off is the immediate blocker** (prompt 2). Define "set in stone" as specific tests that pass and a named sign-off, not just a feeling.
- **Retention first means designing for the measurement first.** Holdout groups (5) and a proper comparison (10) are the only way to show mobile reduces churn.
- **Never use mobile to cover up internet problems** (6). Customers leaving over reliability need the network fixed first.
- **The riskiest moment is the port** (8). A lost phone number can cost the internet customer too.
