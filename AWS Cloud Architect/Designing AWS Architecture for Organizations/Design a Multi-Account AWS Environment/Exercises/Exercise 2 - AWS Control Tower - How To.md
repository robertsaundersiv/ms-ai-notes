---
title: "Exercise 2 – Implementing Governance Policies in AWS Control Tower – How To"
aliases:
  - L2 Exercise 2 How To
  - Implementing Governance Policies in AWS Control Tower
course: AWS Cloud Architect – Designing AWS Architecture for Organizations
lessons:
  - L2-A08 Exercise 2
type: how-to
created: 2026-10-17
updated: 2026-10-17
related:
  - "[[AWS Control Tower]]"
  - "[[Governance and Compliance in Multi-Account Environments]]"
  - "[[Exercise 1 - Manage Accounts using AWS Organizations - How To]]"
tags:
  - aws/control-tower
  - aws/lab
  - how-to
---

# Exercise 2 – Implementing Governance Policies in AWS Control Tower – How To

> [!abstract] Goal
> As new accounts join Steady Volatility Partners' organization, enforce **best-practice security configurations**:
> 1. Create a **Control Tower landing zone**, then **register** the Exercise 1 OUs
> 2. Enable a **detective** control on `DeveloperTestArea`: alert if S3 Block Public Access is removed
> 3. Enable a **preventive** control on `Human Resources`: no S3 replication changes
> 4. Enable a **proactive** control on `Workloads`: no DynamoDB tables without point-in-time recovery
> 5. Create a programmer's account with **Account Factory** in `DeveloperTestArea`
>
> All in the **Control Tower** console. The landing zone alone takes **30–60+ minutes**.

**Concepts:** [[AWS Control Tower]] · [[Governance and Compliance in Multi-Account Environments]] · **Previous lab:** [[Exercise 1 - Manage Accounts using AWS Organizations - How To]]
**Source:** the official exercise sheet, cross-checked against the instructor's demo (video L2-A08).

> [!warning] Not possible with the course credits, and not free in your own account
> Control Tower must run from an organization's **management account**, so it fails in the course sandbox for the same reason as [[Exercise 1 - Manage Accounts using AWS Organizations - How To#0. Before You Start – Using Your Own Account|Exercise 1]]. If you do it in your own account, know these four things first:
> - **Real accounts:** it creates **three real AWS accounts**: Log Archive, Audit, and the programmer's account.
> - **Ongoing charges:** Control Tower is free, but it switches on **AWS Config**, **CloudTrail**, and **S3 log storage** in every governed account. With no workloads that's typically small, but it **never stops** until you decommission.
> - **Hard to undo:** decommissioning a landing zone is a multi-step process, and it doesn't close the accounts it created ([[#9. Cleanup – Personal Account]]).
> - **Prerequisite:** you need the organization and OUs from Exercise 1.

---

## 0. Before You Start

- [ ] Exercise 1 done in this account: organization with **all features**; OUs `Corporate › Human Resources` and `Workloads › Trading System, Market Prediction`
- [ ] Signed in to the **management account** with admin rights. **Not** as the root user: Control Tower setup recommends an IAM or Identity Center admin.
- [ ] Region selector = **US West (N. California) us-west-1**. This becomes the **home Region**.
- [ ] **Three unused email addresses** you control. Plus-addressing works:

| Account | Example email | Notes |
|---|---|---|
| Log Archive | `you+LogArchive@gmail.com` | Created during setup |
| Audit | `you+SecurityAudit@gmail.com` | Created during setup |
| New programmer | `you+Developer2@gmail.com` | Created in step 5 |

**Values from the sheet:**

| Setting | Value |
|---|---|
| Home Region | `us-west-1` (N. California) |
| Foundational OU name | `SVPCorpSecurity` |
| Additional OU name | `DeveloperTestArea` |
| Account access | **IAM Identity Center** |
| CloudTrail | **Enabled** |

---

## 1. Create the Landing Zone

1. Search **Control Tower** → **Set up landing zone**.
2. **Region settings:**
   - **Home Region:** `US West (N. California)`
   - **Region deny setting:** leave the default (*Not enabled*). The sheet doesn't ask for it.
   - **Additional Regions for governance:** none
3. **Configure organizational units:**
   - **Foundational OU:** `SVPCorpSecurity`
   - **Additional OU:** `DeveloperTestArea`
4. **Configure shared accounts:**
   - **Log archive account** email: `you+LogArchive@…` (leave the account name at its default)
   - **Audit account** email: `you+SecurityAudit@…`
5. **Additional configurations:**
   - **AWS account access configuration:** **AWS Control Tower sets up AWS account access with IAM Identity Center**
   - **AWS CloudTrail:** **Enabled**
   - Log retention and KMS encryption: leave the defaults
6. **Review** → tick the acknowledgement(s) that Control Tower will create roles, accounts, and resources → **Set up landing zone**.
7. **Wait** for the dashboard progress bar to finish.

> [!success] Check
> **Organization** shows `SVPCorpSecurity` (with the **Audit** and **Log Archive** accounts) and `DeveloperTestArea`. Both are **Registered**. Your Exercise 1 OUs show **Not registered**.

### 1b. Register the Exercise 1 OUs (parents first)

1. **Control Tower → Organization** → select `Workloads` → **Actions → Register organizational unit** → confirm. Wait for **Registered**.
2. Same for `Corporate`.
3. Then the children: `Trading System` and `Market Prediction` (under Workloads), and `Human Resources` (under Corporate).

> [!success] Check
> All seven non-root OUs show **Registered**. If `MarketPrediction-Prod` is in Market Prediction, registering that OU also **enrolls** the account.

---

## 2. Detective Control – S3 Block Public Access (`DeveloperTestArea`)

The sheet asks for a control that "will notify administrators if a user removes the Block Public Access setting from an S3 bucket".

1. **Control Tower → Controls library → All controls**.
2. Filter **Service = Amazon S3** and **Behavior = Detective**. The demo found 18 controls. Then search **`public access`**, which leaves about 3.
3. Choose the control that checks **S3 Block Public Access settings are enabled**. The demo used the account-level Block Public Access check.
4. **Enable control** → select OU `DeveloperTestArea` → **Enable control**.

> [!note] Why detective
> It doesn't *stop* developers from experimenting. It flags the change (as an AWS Config rule) so admins are notified ([[AWS Control Tower#^ct-keyword-cues]]).

---

## 3. Preventive Control – S3 Replication Changes (`Human Resources`)

The sheet asks for a control that "will not permit changes to S3 buckets that modify replication configuration settings".

1. **Controls library** → search **`replication`**.
2. Choose **Disallow changes to replication configuration for Amazon S3 buckets**. It's an elective, **preventive** (SCP-based) control.
3. **Enable control** → OU `Human Resources` → **Enable control**.

> [!note] Why preventive
> Replication sends copies of data somewhere else. For HR's employee records, the change should be **blocked at the API**, not just reported.

---

## 4. Proactive Control – DynamoDB Point-in-Time Recovery (`Workloads`)

The sheet asks for a control that "will prevent creation of DynamoDB tables unless point-in-time recovery is activated".

1. **Controls library** → filter **Behavior = Proactive** → search **`DynamoDB`**.
2. Choose the control requiring **point-in-time recovery** on DynamoDB tables.
3. **Enable control** → OU `Workloads`. As the sheet warns, the console reports a **prerequisite** control.
4. **Copy the prerequisite's name or ID.** In the demo it was **CT.CLOUDFORMATION.PR.1**, the CloudFormation control that protects the hook machinery proactive controls depend on. Search for it → **Enable control** on `Workloads`.
5. Return to the DynamoDB PITR control → **Enable control** on `Workloads`.

> [!success] Check
> `Workloads` → **Controls** tab lists the CloudFormation prerequisite **and** the DynamoDB PITR control as **Enabled**. Child OUs (Trading System, Market Prediction) inherit them.

> [!note] Why proactive
> It rejects a **CloudFormation template** that creates a table without PITR *before deployment* (a CloudFormation hook). Tables created outside CloudFormation aren't checked by this control.

---

## 5. Account Factory – New Programmer Account (`DeveloperTestArea`)

1. **Control Tower → Account factory → Create account**. (Some console versions put it under **Organization → Create resources → Create account**.)
2. **Account email:** `you+Developer2@…`
3. **Display name:** your choice, e.g. `Developer2` (the demo's name)
4. **IAM Identity Center user:** an email, first name, and last name for the programmer. You can use your own.
5. **Organizational unit:** `DeveloperTestArea`
6. **Create account**. Provisioning takes several minutes and runs through **Service Catalog** behind the scenes ([[AWS Control Tower#^def-account-factory]]).

> [!success] Check
> The new account appears under `DeveloperTestArea` with state **Enrolled**. IAM Identity Center emails the programmer user an invitation.

---

## 6. Verify the Whole Exercise

- [ ] Landing zone **Available**, home Region **us-west-1**
- [ ] `SVPCorpSecurity` OU contains **Audit** and **Log Archive** accounts
- [ ] `DeveloperTestArea` OU exists
- [ ] `Workloads`, `Corporate`, `Trading System`, `Market Prediction`, `Human Resources` all **Registered**
- [ ] **Detective** S3 Block Public Access control enabled on `DeveloperTestArea`
- [ ] **Preventive** "disallow S3 replication changes" control enabled on `Human Resources`
- [ ] **Proactive** DynamoDB PITR control (plus its CloudFormation prerequisite) enabled on `Workloads`
- [ ] Programmer account **Enrolled** in `DeveloperTestArea`

---

## 7. Mapping to the Sheet's Objectives

| Sheet objective | Section | Control behavior and mechanism |
|---|---|---|
| Create a landing zone | 1 | — |
| Detective control on an OU | 2 | Detective: AWS Config rule |
| Preventive control on an OU | 3 | Preventive: SCP |
| Proactive control on an OU | 4 | Proactive: CloudFormation hook |
| Add an account via Account Factory | 5 | Service Catalog product |

---

## 8. Troubleshooting

| Problem | Likely cause | Fix |
|---|---|---|
| "Set up landing zone" fails pre-checks | Account isn't a management account; an existing **AWS Config** recorder or **CloudTrail** trail conflicts; IAM Identity Center already enabled in another Region | Read the pre-check message. Remove or align the conflicting resource, or run from the correct account. |
| "Email address already in use" | Address is tied to another AWS account | Use a new plus-address |
| Can't register a child OU | Parent not registered yet | Register `Workloads` and `Corporate` first |
| OU registration fails | An account inside can't be enrolled | Open the account's enrollment error, then fix or move the account |
| Proactive control won't enable | Prerequisite control missing | Enable the named prerequisite on the same OU first |
| Account Factory create fails | Account quota reached, or email reused | Check Organizations quotas; use a new email |
| Control Tower pages are empty | Wrong Region | Switch to the **home Region**, us-west-1 |

---

## 9. Cleanup – Personal Account

Control Tower keeps charging small amounts until it's **decommissioned**. That's a multi-step process AWS documents, and it does **not** close the accounts it created.

1. Disable the controls you enabled (optional, before decommissioning).
2. Follow AWS's **Decommission a landing zone** procedure from the Control Tower console or documentation. Read it fully first.
3. **Close** the Log Archive, Audit, and programmer accounts in **AWS Organizations** (each enters a ~90-day post-closure period).
4. Then follow [[Exercise 1 - Manage Accounts using AWS Organizations - How To#7. Cleanup – Personal Account|Exercise 1's cleanup]] for the OUs and organization.

> [!warning] Don't delete Control Tower resources by hand
> Deleting Log Archive buckets, Config rules, or Control Tower roles directly is what the **mandatory controls** exist to prevent. It leaves the landing zone broken and harder to decommission ([[Governance and Compliance in Multi-Account Environments#3. Control Tower Control Guidance Levels]]).
