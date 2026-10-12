---
title: "Financial Controller Prompt Library"
aliases:
  - Controller Prompts
type: reference
status: review
created: 2026-10-01
related:
  - "[[CEO Prompt Library]]"
  - "[[COO Prompt Library]]"
  - "[[NOC Director Prompt Library]]"
  - "[[IT Director Prompt Library]]"
  - "[[Customer Service Director Prompt Library]]"
  - "[[Marketing Director Prompt Library]]"
  - "[[MVNO Launch Prompt Library]]"
  - "[[Network Operations Engineering Manager Prompt Library]]"
  - "[[Rapid Response Network Operations Manager Prompt Library]]"
  - "[[Gate Checks]]"
tags:
  - prompt-engineering
  - isp-operations
  - finance
  - reference
---

# Financial Controller Prompt Library

> [!abstract] TL;DR
> Ten prompts for **Wi-Fiber's Financial Controller**, built around four concerns: **strong financial controls**, **cutting expenses where it won't disrupt operations**, **combining scattered tracking methods into one place**, and **managing a budget smaller than everyone's project and upgrade list**. ==The controller keeps financial records accurate and makes sure limited money goes to what protects churn, uptime and cash first.== Each prompt names the technique it uses from this vault.

> [!example] Context block (paste above any prompt)
> ```text
> ORG: Wi-Fiber, a fixed wireless ISP in 10 markets across 8 states. Billing and subscriber data in
> Sonar; accounting system {QuickBooks / NetSuite / other}; departments: Network Ops (NOC),
> Customer Service, Field Ops, Marketing, IT, and a new MVNO (mobile) department.
> COMPANY PRIORITIES: lower churn, raise EBITDA, improve customer sentiment, long-term stability.
> I am the Financial Controller. Keep operations running while tightening controls and spend.
> ```

> [!note] Shared rules
> - **The ledger is the source of truth.** Do the math in your accounting system or spreadsheets and give the model the results. Use the model to classify, structure, find gaps and write. ([[Sonar Ticket and Outage Classification - How-To#^compute-dont-ask|compute, don't ask]])
> - **Check every classification the model produces** against the source records before posting entries or making decisions. ([[Output Validation]])
> - **Never paste bank account numbers, card numbers, SSNs/EINs, payroll detail or credentials.** Use vendor names, categories and totals, and keep confidential financials in approved tools.
> - **Accounting treatment, tax and audit questions go to your CPA or auditor.** The model can help prepare the questions.

> [!todo]- Contents
> | # | Prompt | Concern | Technique |
> |---|---|---|---|
> | 1 | [[#1. Internal Controls Gap Assessment]] | Controls | Checklist gate |
> | 2 | [[#2. Month-End Close and Reconciliation Checklist]] | Controls | Structured output |
> | 3 | [[#3. Spend Cube from AP and Card Exports]] | Expenses | Few-shot classification |
> | 4 | [[#4. Operations-Safe Expense Reduction]] | Expenses | Logic gates |
> | 5 | [[#5. Tracking Inventory and Single Source of Truth Design]] | One location | Task decomposition |
> | 6 | [[#6. Category and Cost-Center Mapping]] | One location | Few-shot + validation gate |
> | 7 | [[#7. Standard Project and Spend Request Intake]] | Budget | Structured output |
> | 8 | [[#8. Budget Prioritization When Demand Exceeds Budget]] | Budget | Tree-of-Thought |
> | 9 | [[#9. "Not Now" Budget Communication]] | Budget | Content gates |
> | 10 | [[#10. Monthly Budget vs Actual and Rolling Forecast]] | All | Plan-then-solve |

---

## 1. Internal Controls Gap Assessment

**Use when:** you're tightening controls in a growing company where people wear several hats and segregation of duties is hard.

```text
ROLE: You are an internal controls advisor for a mid-sized company with a small finance team.

<current_state>{who can: create vendors, approve invoices, release payments, change bank details,
  issue customer credits/refunds in Sonar, write off bad debt, approve payroll changes, use company
  cards (limits), approve POs (thresholds); how reconciliations are done and reviewed; system
  access list by role}</current_state>

Assess against these control areas (score each STRONG / ADEQUATE / WEAK / MISSING, citing current_state):
 1. Segregation of duties (vendor setup vs approval vs payment)
 2. Delegation of authority (approval thresholds by role and amount)
 3. Vendor master changes (bank detail change verification – call-back procedure)
 4. Customer credits, refunds and write-offs in Sonar (limits, approval, review)
 5. Company cards and expense reimbursement
 6. Reconciliations (bank, Sonar billing → GL, AR, AP, inventory/equipment) and review evidence
 7. System access and user reviews
 8. Journal entries (who posts, who reviews, thresholds)

Then:
- Top 5 risks by likelihood × impact (fraud, error, payment diversion)
- For a small team: COMPENSATING CONTROLS where full segregation isn't possible (e.g., owner
  review of payment runs, monthly vendor-change report reviewed by CFO)
- A draft Delegation of Authority matrix (role × spend type × threshold)
Only score areas with information provided. Mark others "UNKNOWN – need info".
```

> Technique: a checklist gate from [[Gate Checks]]. Compensating controls make the result workable for a small team.

---

## 2. Month-End Close and Reconciliation Checklist

**Use when:** your close is inconsistent, slow or dependent on one person, and you want a standard, reviewable close.

```text
ROLE: You design month-end close processes for subscription businesses.

<current_close>{steps done today, who does them, timing (day of close), systems, pain points,
  how long close takes}</current_close>
SPECIFICS: subscription revenue in Sonar (billing, credits, proration, MVNO mobile charges and
  telecom taxes/fees collected), deferred revenue if applicable, tower leases, equipment/CPE
  inventory, capitalized labor for installs/towers (if applicable), accruals for vendor bills.

Respond ONLY in this format:
## Close calendar (Day −2 to Day +N: task | owner role | system | output | reviewer)
## Reconciliations (account | method | source data | tolerance | evidence retained)
   – include Sonar billed revenue → GL, cash receipts → bank, credits issued → policy,
     taxes/fees collected → remitted liability
## Review & sign-off (who signs each section; what they look at)
## Flux analysis (accounts to explain if variance > {X% or $Y} vs last month and budget)
## Automation candidates (which steps could be scripted or pulled automatically)
## Single points of failure (tasks only one person knows how to do) + backup owner
Flag any step where the preparer and reviewer are the same person.
```

> Technique: [[Structured Outputs]]. A standard format makes the close repeatable and easy to audit, and points out where one person is a single point of failure.

---

## 3. Spend Cube from AP and Card Exports

**Use when:** you want to see where the money actually goes: duplicate tools, forgotten subscriptions, scattered vendors.

```text
ROLE: You categorize company spend for analysis.

<transactions>{12 months of AP + card + reimbursement lines: date, vendor, memo, amount,
  department/cost center if coded, GL account}</transactions>

Classify each vendor into: category / sub-category / department / RECURRING or ONE-TIME /
  OPERATIONALLY CRITICAL (Y/N/UNSURE). Examples of my standard:

- "Acme Tower Holdings – site 114 rent" → Network / Tower leases / NOC / RECURRING / Y
- "Zoom – monthly" + "Microsoft Teams" both present → IT / Collaboration software / Company /
  RECURRING / N – flag DUPLICATE FUNCTION
- "Home Depot" on a field tech card → Field / Install materials / Field / ONE-TIME / UNSURE
- "Transit Provider X – 10G" → Network / Upstream bandwidth / NOC / RECURRING / Y

Then output:
1. Spend by category and department (table with totals; I'll verify against the GL)
2. Duplicate-function tools and subscriptions, with spend
3. Vendor fragmentation: categories with 5+ vendors (consolidation candidates)
4. Unusual items for review (round numbers, new vendors with large first payments, split
   transactions just under approval thresholds)
Mark low-confidence classifications "REVIEW".
```

> Technique: [[Few-Shot Prompting]]. Four examples set the categories and the critical/non-critical standard. Item 4 doubles as a fraud and controls check.

---

## 4. Operations-Safe Expense Reduction

**Use when:** you need savings but can't risk outages, slower repairs or worse customer service, all of which increase churn.

```text
ROLE: You evaluate expense-reduction ideas for operational and churn risk.

<ideas>{each: description, annual savings, department, what changes operationally}</ideas>
CHURN VALUE: {$ value of a 0.1 pt churn change – from CEO library prompt 7, if available}

For each idea, apply the OPERATIONS GATE:
1. Does it touch network uptime, repair speed (MTTR), field capacity, CS staffing/hold times,
   or customer billing accuracy? (Y/N + how)
2. If yes: the specific failure mode (e.g., cutting spares → longer outages → churn)
3. Break-even: how much churn or outage increase would erase the savings? (calc if data given)
4. Verdict: GREEN (no operational touch – do it), YELLOW (do it with a guardrail metric and owner
   who can reverse it), RED (risk outweighs savings – don't)

Then:
- Total GREEN + YELLOW savings
- 5 additional "low-regret" ideas typical for ISPs (unused software seats, duplicate tools,
  vendor consolidation, contract renegotiation at renewal, avoidable truck rolls, paper
  billing → e-bill, energy at tower sites), flagged as ideas to validate, not facts
- Who must agree before each YELLOW item goes ahead (department head)
```

> Technique: logic [[Gate Checks]] applied to cost decisions. Cuts that threaten uptime or service are caught before they're made, not after churn goes up.

---

## 5. Tracking Inventory and Single Source of Truth Design

**Use when:** budgets, project spend, equipment, contracts and KPIs are tracked in many spreadsheets, apps and inboxes, and nobody trusts the numbers.

```text
ROLE: You are a finance systems architect consolidating scattered tracking into one place.

<trackers>{for each tracker: name, owner/department, tool (Excel, Google Sheet, Sonar, accounting
  system, Smartsheet, email, etc.), what it tracks, update frequency, key fields, who uses it,
  known problems}</trackers>
TARGET PLATFORM: {e.g., accounting system + one shared workbook / BI tool / ERP module} – or
  "recommend one".

STEP 1 – INVENTORY: Group trackers by subject (budget, project spend, capex, equipment/CPE
  inventory, contracts/leases, headcount, KPIs). Show overlaps (same data tracked in 2+ places)
  and conflicts (different numbers for the same thing).
STEP 2 – SYSTEM OF RECORD: For each subject, name the single system of record and why.
  Everything else becomes a view or report, not a separate copy.
STEP 3 – DATA MODEL: Standard fields every department must use: GL account, cost center
  (department + market), project ID, vendor ID, date, amount. Define each field.
STEP 4 – MIGRATION PLAN: Phases (start with the highest-pain subject), owner per tracker, retire
  date per old tracker, and how to keep departments from going back to side spreadsheets.
STEP 5 – GOVERNANCE: Who can change the structure, monthly data-quality checks.
```

> Technique: [[Task Decomposition]]. Splitting the work into inventory, system of record, data model, migration and governance makes a big consolidation project manageable.

---

## 6. Category and Cost-Center Mapping

**Use when:** you're merging historical data from different trackers, and each department used its own labels ("Tower stuff", "NOC Misc", "Radios-Q2").

```text
ROLE: You map inconsistent spend labels to a standard chart of accounts and cost centers.

STANDARD CHART OF ACCOUNTS: {list of GL accounts with descriptions}
STANDARD COST CENTERS: {department × market codes}
<legacy_rows>{source tracker, legacy category label, description/memo, department, amount}</legacy_rows>

Examples:
- "Tower stuff – Lakeview generator fuel" (NOC tracker) → GL 6120 Site Power & Fuel / CC NOC-LKV / HIGH
- "Radios-Q2" (Field tracker, $14,200, 40 units) → GL 1510 Network Equipment (capex?) / CC FLD-ALL /
  REVIEW – capitalization threshold decision needed
- "Misc" ($87, "lunch for install crew") → GL 6450 Meals / CC FLD-{market unknown} / REVIEW – market missing

For each row: mapped GL, cost center, confidence (HIGH / REVIEW), and reason.
GATE RULES:
- Only use GL accounts and cost centers from the standard lists. Never invent one.
- Anything that might be capex vs opex → REVIEW with the question to ask.
- Missing market/department → REVIEW, don't guess.
Then: a mapping table (legacy label → standard) reusable for future imports, and the % of dollars
  that mapped HIGH vs REVIEW.
```

> Technique: [[Few-Shot Prompting]] with a closed-list validation gate from [[Output Validation]]. The output can only use accounts from your list, and the mapping table can be reused as a lookup on future imports.

---

## 7. Standard Project and Spend Request Intake

**Use when:** project and upgrade requests arrive as emails, hallway conversations and slide decks, so they can't be compared fairly.

```text
ROLE: You design a standard request form for capital and project spending.

DEPARTMENTS: NOC, CS, Field, Marketing, IT, MVNO. COMPANY PRIORITIES: churn, EBITDA, customer
  sentiment, stability.

Create:
1. A one-page REQUEST TEMPLATE with required fields:
   - Description, requester, department, markets affected
   - Type: MUST-DO (safety, legal/regulatory, contractual, end-of-life with outage risk) /
     PROTECT (uptime, churn, security) / GROW (revenue) / EFFICIENCY (cost savings) / NICE-TO-HAVE
   - Cost: capex, one-time opex, ongoing annual opex; cash timing by month
   - Benefit: quantified (outage minutes avoided, churn reduction, revenue, savings) with
     the source of each estimate
   - Cost of delay: what happens if this waits 6 / 12 months
   - Can it be phased or scaled down? Minimum viable version and its cost
   - Dependencies and the people/crews needed
2. A SCORING RUBRIC (weights tied to company priorities) that I can apply consistently.
3. A SUBMISSION CHECK: the reasons a request is sent back incomplete (no cost-of-delay, no
   ongoing opex, benefit with no source).
Then turn this pasted request into the template and flag missing items: {paste a messy request}
```

> Technique: [[Structured Outputs]]. Every request has the same fields, so prompt 8 can compare them fairly. The submission check rejects incomplete requests.

---

## 8. Budget Prioritization When Demand Exceeds Budget

**Use when:** total requests are well over the budget and you need a defensible way to decide what gets funded, phased or deferred.

```text
ROLE: You help a Financial Controller allocate a constrained budget across competing requests.

BUDGET: capex {amount}, opex increase {amount}, by quarter if cash timing matters.
<requests>{standardized requests from prompt 7: type, cost, cash timing, quantified benefit,
  cost of delay, phase-able Y/N + minimum version cost, department}</requests>
CONSTRAINTS: {covenants, minimum cash balance, crew capacity, vendor lead times}

1. FUND FIRST: MUST-DO items. Show their total and what's left.
2. Build 3 allocation approaches for the remaining budget, evaluated separately:
   a) Highest risk-reduction first (uptime/churn PROTECT items)
   b) Highest financial return first (EBITDA / payback)
   c) Phased: minimum versions of many items now, full versions later
   For each: what's funded, deferred and cut; expected impact on churn/uptime/EBITDA (from requests'
   estimates, labeled); cash low point; which departments are most affected.
3. Prune approaches that break constraints.
4. Recommend one (or a blend) with: a funded list, a "next in line if money frees up" list with
   triggers (e.g., savings from prompt 4, revenue beat), and a deferred list with the
   cost-of-delay risk the business is accepting.
5. Items where the requester's benefit estimate looks weak and needs challenge.
```

> Technique: [[Tree-of-Thought]]. Comparing three different allocation approaches makes the trade-offs clear and gives leadership a real choice.

---

## 9. "Not Now" Budget Communication

**Use when:** you have to tell department heads their projects are deferred or cut, and you want them to stay on board instead of finding workarounds.

```text
ROLE: You help a Financial Controller communicate budget decisions to department heads.

DECISION: {for this department: funded items, phased items, deferred items, cut items, and the
  reason for each from the prioritization (prompt 8)}
DEPARTMENT HEAD: {role, what they care about, how they're measured}

Write:
1. A message (≤250 words): what's funded first, then what's not and why (tied to company
   priorities and real constraints), what would change the decision, and the next review date.
2. Options for them: the minimum viable version, phasing, an opex-for-capex swap, or a savings
   they could find in their own budget to self-fund.
3. A talk track for a live conversation, including 4 likely pushbacks with honest responses.
4. What I need from them (updated cost-of-delay, phasing plan, risk acceptance sign-off for
   deferred safety/uptime items).

MUST: lead with what they ARE getting; give the real reason; give a review date.
MUST NOT: blame another department, imply the project lacks merit if it was simply outranked,
  or promise future funding.
Self-check each rule PASS/FAIL.
```

> Technique: content [[Gate Checks]]. Clear rules keep a difficult message honest and respectful, and the risk-acceptance step records who accepted the risk of a deferral.

---

## 10. Monthly Budget vs Actual and Rolling Forecast

**Use when:** each month you want to catch overspends early, free up money for the "next in line" list and reforecast the year.

```text
ROLE: You produce a monthly budget-vs-actual review and rolling forecast for a Controller.

<bva>{by department and GL category: month actual, month budget, YTD actual, YTD budget,
  prior forecast for full year}</bva>
<commitments>{open POs, signed contracts not yet billed, approved projects not yet started}</commitments>
<context>{known one-time items, timing shifts, department explanations}</context>

PLAN first: how to separate timing vs permanent variances and how to treat commitments in the
  forecast. Stop and show me.

Then:
1. Variances over {X% or $Y}: department, amount, TIMING / PERMANENT / ONE-TIME / UNEXPLAINED
   (quote the explanation from context, or mark UNEXPLAINED – ask owner)
2. Full-year forecast = YTD actual + commitments + remaining run-rate (show math by department)
3. Forecast vs budget: projected over/under by department
4. Money freed up (permanent underspends) → which "next in line" item it could fund (prompt 8)
5. Early warnings: departments on track to overspend, with the month they'll hit budget
6. A 5-line summary for the CEO/COO
Use only numbers provided. Flag anything that doesn't reconcile.
```

> Technique: Plan-then-Solve from [[CoT prompt Samples#6. Sample 5 – Plan-then-Solve]]. You approve the variance method first, and the forecast feeds the prioritization in prompt 8 each month.

---

## Key Takeaways

- **Standardize first, then prioritize.** The intake form (7) and data model (5, 6) have to exist before budget decisions (8) can be fair and repeatable.
- **Expense cuts must pass an operations check** (4). Savings that cause outages or slower service come back as churn.
- **"Not now" is a decision that needs follow-up.** Deferred items get triggers (8), honest communication (9) and a monthly check for freed-up money (10).
- **Controls should be sized for a small team.** Compensating controls (1) and preparer/reviewer checks (2) are realistic where full segregation of duties isn't.
