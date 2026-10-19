---
title: "Exercise 1 – Using AWS Cost Explorer and Compute Optimizer for Cost Analysis – How To"
aliases:
  - L3 Exercise 1 How To
  - Using AWS Cost Explorer and Compute Optimizer for cost analysis
course: AWS Cloud Architect – Designing AWS Architecture for Organizations
lessons:
  - L3-A06 Exercise 1
type: how-to
created: 2026-10-17
updated: 2026-10-17
related:
  - "[[AWS Cost and Usage Monitoring Tools]]"
  - "[[Cost Optimization and Analysis Strategies]]"
  - "[[Exercise 2 - Implementing Tagging and Reporting Strategies - How To]]"
tags:
  - aws/cost-management
  - aws/compute-optimizer
  - aws/lab
  - how-to
---

# Exercise 1 – Using AWS Cost Explorer and Compute Optimizer for Cost Analysis – How To

> [!abstract] Goal
> The CFO wants AWS costs **documented and minimized**, especially overspending on the trading team's **expensive GPU instances**. In this exercise you:
> 1. **Analyze recent spending** with Cost Explorer reports and Free Tier usage
> 2. Enable **Cost Anomaly Detection** with a 10% email alert
> 3. Enable the **Cost Optimization Hub** for the organization
> 4. Enable **Compute Optimizer** for the organization, with GPU/ML rightsizing preferences
>
> It takes about 20 minutes, plus a 12–24-hour wait for findings.

**Concepts:** [[AWS Cost and Usage Monitoring Tools]] · [[Cost Optimization and Analysis Strategies]] · **Next lab:** [[Exercise 2 - Implementing Tagging and Reporting Strategies - How To]]
**Source:** the official exercise sheet, cross-checked against the instructor's demo (video L3-A06).

> [!warning] Optional, and not possible on Udacity-provided accounts
> The sheet says so explicitly. Organization-related steps (steps 3–4 here, including the Cost Optimization Hub) can't be done in the course accounts. To do it anyway, use **your own account**:
> - **Steps 1–2** work in any standalone account with billing access.
> - **Steps 3–4** "for all accounts in the Organization" need an organization's **management account**. In a standalone account, opt in **just that account**.
> - **Cost:** everything here is free. That covers the Cost Explorer console, saved reports, anomaly detection, the Cost Optimization Hub, and Compute Optimizer with a 32-day lookback.

---

## 0. Before You Start

- [ ] Signed in with **Billing and Cost Management** access (the management account, for organization-wide steps)
- [ ] Cost Explorer opened at least once before. The first visit **enables** it, and data takes **up to 24 hours** to appear.
- [ ] An email address for anomaly alerts

**Values from the sheet:**

| Item | Value |
|---|---|
| Monthly report name | `TradingSystemReport-(Month)-(Year)`, e.g. `TradingSystemReport-October-2026` |
| Weekly report name | `TradingSystemReport-Weekly-3rdMonday-(Month)-(Year)`, e.g. `TradingSystemReport-Weekly-3rdMonday-October-2026` |
| Anomaly alert | **Email** when spend is **10% above expected** |
| Cost Optimization Hub scope | **All accounts in the organization** |
| Compute Optimizer scope | **All accounts in the organization** |
| Rightsizing instance families | **P, G, Trn, Inf** |
| Lookback period | **32 days** |
| Optimization goal | **Maximum savings** |

---

## 1. Analyze Recent AWS Spending

### 1a. Daily Costs report

1. **Billing and Cost Management → Cost Explorer saved reports** (Reports).
2. Open the AWS-provided **Daily costs** report.
3. **Identify the date of your greatest expense** in recent usage. Write it down.

### 1b. This month's report

4. Go to **Cost Explorer**.
5. **Date range:** choose **Month to date** (or a custom range from the 1st of this month to today) → **Apply**.
6. **Save to report library** → name: `TradingSystemReport-<Month>-<Year>` → save.

> [!tip] If this month has almost no data
> The demo hit this and switched to an earlier, busier month. If you do that, name the report after the month it covers.

### 1c. This week's report

7. Change the **date range** to **this week only** → **Apply**.
8. **Save to report library** → name: `TradingSystemReport-Weekly-3rdMonday-<Month>-<Year>`. The name reflects a weekly report run on the **third Monday** of the month.

### 1d. Read the monthly report

9. Use **recently accessed reports** (or Reports) to **switch to the monthly report**.
10. **Group by: Service.** Observe which **services contributed most** to this month's spend.

### 1e. Confirm and check Free Tier

11. Go back to **Cost Explorer saved reports**. Both of your reports now appear **alongside the AWS-provided reports**.
12. **Billing and Cost Management → Free Tier**: **observe Free Tier utilization** for each service. The demo showed SNS at 16,000 of 1M requests, and KMS at 233 of 20,000.

> [!success] Check
> - The top-spend date from **Daily costs** is noted.
> - Both named reports are in the library.
> - You know the top services this month and your Free Tier status.

---

## 2. Enable Cost Anomaly Detection

1. **Billing and Cost Management → Cost Anomaly Detection → Cost monitors → Create monitor**.
2. **Monitor type:** **AWS services**. That tracks each service separately, as in the demo ([[Cost Optimization and Analysis Strategies#3. AWS Cost Anomaly Detection]]).
3. **Monitor name:** e.g. `TradingSystemServicesMonitor`
4. **Alert subscription → Create a new subscription:**
   - **Subscription name:** e.g. `TradingSystemAnomalyEmail`
   - **Alerting frequency:** **Individual alerts** (immediate email) or **Daily summaries**. The sheet just asks for an email alert.
   - **Threshold:** **Percentage above expected spend → 10**
   - **Recipients:** your email address
5. **Create monitor**.

> [!success] Check
> **Cost monitors** lists the monitor, with your subscription showing a **10%** threshold and **email** delivery.

---

## 3. Enable the Cost Optimization Hub

1. **Billing and Cost Management → Cost Optimization Hub**.
2. **Enable**, choosing **all member accounts in the organization**. That option exists only in the management account. A standalone account enables itself.
3. **View available savings opportunities.** A new or idle account may show none, which is expected.

> [!note] Needed for Exercise 2
> Exercise 2 exports these recommendations, so the hub must be enabled first.

---

## 4. Enable Compute Optimizer

1. Open the **Compute Optimizer** console → **Get started**.
2. **Opt in:** choose **all accounts within this organization** (management account), or this account only.
3. Left menu **Preferences → Rightsizing preferences** (in some consoles: *General → Rightsizing recommendation preferences*) → **Edit**:
   - **Scope:** the organization or account, **all Regions**
   - **Preferred instance families:** limit recommendations to **P**, **G**, **Trn**, **Inf**
     - P and G are NVIDIA GPU families. Trn is AWS Trainium; Inf is AWS Inferentia.
   - **Lookback period:** **32 days**. 14 is the default; 93 needs paid enhanced infrastructure metrics.
   - **Recommendation goal / savings estimation mode:** **Maximum savings**. This weighs recommendations toward cost reduction rather than performance headroom.
   - **Save**.
4. **Observe** the recommendation **categories** the dashboard lists, such as EC2 instances, Auto Scaling groups, EBS volumes, Lambda functions, ECS on Fargate, and RDS. Findings arrive over the next **12+ hours**. **Revisit tomorrow.**

> [!note] Empty findings are normal
> Compute Optimizer needs about **30 hours** of resource runtime before recommending ([[Cost Optimization and Analysis Strategies#2. AWS Compute Optimizer]]). An account with no P/G/Trn/Inf instances will have no findings within these families.

> [!question] Why restrict to GPU/ML families
> It focuses the analysis on the CFO's **special concern**, the trading team's GPU spend, instead of drowning it among cheap general-purpose instances.

---

## 5. Verify the Whole Exercise

- [ ] Top-spend date found in **Daily costs**
- [ ] `TradingSystemReport-<Month>-<Year>` (month to date) and `TradingSystemReport-Weekly-3rdMonday-<Month>-<Year>` (this week) saved
- [ ] Top services this month observed; both reports visible among the provided reports
- [ ] Free Tier utilization reviewed
- [ ] Cost monitor with an **email** alert at **10% above expected**
- [ ] Cost Optimization Hub enabled for **all organization accounts**; opportunities viewed
- [ ] Compute Optimizer opted in for **all organization accounts**; preferences: **P, G, Trn, Inf**, **32-day lookback**, **maximum savings**
- [ ] Reminder set to revisit Compute Optimizer **tomorrow**

---

## 6. Troubleshooting

| Problem | Likely cause | Fix |
|---|---|---|
| Access denied on billing pages | Udacity account or IAM restrictions | Use your own account, or study only (the sheet marks it optional) |
| Cost Explorer empty | Enabled less than 24 hours ago | Wait |
| No "all accounts in organization" option | Not the management account | Enable for this account only |
| Lookback or goal option missing | Console version differs, or account-level preferences are only editable at org level | Edit preferences at the organization scope from the management account |
| No Compute Optimizer findings | No eligible instances, or under 30 hours + 24 hours | Revisit later. Expected with no GPU instances. |

---

## 7. Cleanup

Nothing here is billed, and **Exercise 2 depends on the Cost Optimization Hub**. To remove later: delete the cost monitor and subscription, delete the two saved reports, and opt out of Compute Optimizer and the Cost Optimization Hub in their settings.
