---
title: "Exercise 1 – Organize Accounts with AWS Organizations – How To"
aliases:
  - L2 Exercise 1 How To
  - Create and Manage Accounts using AWS Organizations
course: AWS Cloud Architect – Designing AWS Architecture for Organizations
lessons:
  - L2-A07 Exercise 1
type: how-to
created: 2026-10-17
updated: 2026-10-17
related:
  - "[[AWS Organizations]]"
  - "[[Organizational Units and Service Control Policies]]"
  - "[[Exercise 2 - AWS Control Tower - How To]]"
tags:
  - aws/organizations
  - aws/lab
  - how-to
---

# Exercise 1 – Organize Accounts with AWS Organizations – How To

> [!abstract] Goal – "Create and Manage Accounts using AWS Organizations"
> As Steady Volatility Partners' IT team adds AWS accounts, implement a **multi-account strategy** with stronger central management:
> 1. Create an **organization** and its OU tree
> 2. **Invite** the Human Resources account
> 3. Enable **SCPs** and attach `RestrictRelationalDatabases` to Workloads
> 4. **Create** the `MarketPrediction-Prod` account
>
> Everything is done in the **AWS Organizations** console and takes about 20 minutes.

**Concepts:** [[AWS Organizations]] · [[Organizational Units and Service Control Policies]] · **Next lab:** [[Exercise 2 - AWS Control Tower - How To]]
**Source:** the official exercise sheet, cross-checked against the instructor's demo (video L2-A07).

> [!warning] Can't be done with the course's AWS credits
> The course-provided account can't run this exercise. Course sandboxes are typically **member accounts of the provider's own organization**, or are blocked from AWS Organizations. An account can't create an organization while it belongs to one. You have two options:
> - **Study it.** Read this guide alongside the demo video. The concepts are covered in [[AWS Organizations]] and [[Organizational Units and Service Control Policies]].
> - **Do it in your own AWS account.** Organizations, OUs, SCPs, and new member accounts are **free** ([[AWS Organizations#^accounts-free]]). Read [[#0. Before You Start – Using Your Own Account]] first: this permanently changes your account's role, and step 4 creates a real AWS account.

---

## 0. Before You Start – Using Your Own Account

| Effect on your personal account | Why it matters | What to do |
|---|---|---|
| It becomes the organization's **management account** | Org policies (SCPs) **don't** restrict it ([[AWS Organizations#^def-management-account]]), and it will own the bill for any member accounts | Fine for a learning account. Don't do this in an account that's already part of another organization. |
| Step 2 invites `111122223333` | That's AWS's documentation **example ID**, not a real account | The invitation will **fail or sit unaccepted**. That's expected. |
| Step 4 **creates a real AWS account** | It needs an email that has **never** been used for an AWS account. Closing it later starts a **post-closure period** (about 90 days) before it's gone. | Use a plus-address you control, e.g. `you+MarketPredictionProd@gmail.com`. See [[#7. Cleanup – Personal Account]]. |
| No resources are launched | Nothing here is billed | — |

- [ ] Signed in to the account that will be the **management account**, as a user with admin rights
- [ ] Organizations is **global**, so the Region selector doesn't matter

**Values from the sheet:**

| Item | Value |
|---|---|
| OUs under Root | `Corporate`, `Workloads` |
| OU under Corporate | `Human Resources` |
| OUs under Workloads | `Trading System`, `Market Prediction` |
| Invited account | `111122223333` |
| Invitation message | `Hello HR Team - please follow the instructions below to add your AWS account to the corporate AWS Organizations structure.` |
| SCP name | `RestrictRelationalDatabases` |
| SCP effect | Deny **all actions** in **RDS**, **RDS Data API**, **RDS IAM Authentication**, on resource `"*"` |
| SCP target | `Workloads` OU |
| New account | `MarketPrediction-Prod`, with an email address you control |

---

## 1. Create the Organization and OU Tree

### 1a. Create the organization

1. Search **AWS Organizations** → **Create an organization** → confirm.
   - **All features** is enabled by default, and you need it for SCPs ([[AWS Organizations#5. Consolidated Billing vs. All Features]]).

> [!success] Check
> **AWS accounts** shows **Root** containing your account, labeled **management account**.

> [!note] Verify your email now
> AWS emails the management account's address. **Click the verification link.** You can't invite accounts (step 2) until the address is verified.

### 1b. Create the OUs

1. **AWS accounts** → tick **Root** → **Actions** → under *Organizational unit*, **Create new** → name `Corporate` → **Create organizational unit**.
2. Tick **Root** → **Create new** → `Workloads`.
3. Tick **Corporate** → **Create new** → `Human Resources`.
4. Tick **Workloads** → **Create new** → `Trading System`.
5. Tick **Workloads** → **Create new** → `Market Prediction`.

```text
Root
├── Corporate
│   └── Human Resources
├── Workloads
│   ├── Trading System
│   └── Market Prediction
└── <your account>  (management account)
```

> [!tip] Check the parent before each create
> The new OU is created inside whichever OU is **ticked**. If one lands in the wrong place, tick it → **Actions → Move**. (Moving works for accounts; for an OU, delete and recreate it while it's still empty.)

---

## 2. Invite the Human Resources Account

1. **AWS accounts** → **Add an AWS account** → **Invite an existing AWS account**.
2. **Email address or account ID:** `111122223333`
3. **Message:**

   ```text
   Hello HR Team - please follow the instructions below to add your AWS account to the corporate AWS Organizations structure.
   ```

4. **Send invitation**.

> [!success] Check
> **Invitations** (left menu) lists the invitation as **Open**. Or AWS rejects it because `111122223333` isn't a real account. **Either outcome is expected.**

> [!note] What happens with a real account
> The HR account's owner opens **AWS Organizations** in *their* account → **Invitations** → **Accept**. You'd then move it from Root into `Corporate › Human Resources` (**Actions → Move**). The account joins with no SCPs other than FullAWSAccess until you attach some.

---

## 3. Enable SCPs and Create `RestrictRelationalDatabases`

### 3a. Enable SCPs

1. Left menu **Policies** → **Service control policies** → **Enable service control policies**.

> [!success] Check
> **FullAWSAccess** appears, attached by default to Root, every OU, and every account ([[Organizational Units and Service Control Policies#^def-fullawsaccess]]).

### 3b. Create the policy

1. **Service control policies → Create policy**.
2. **Policy name:** `RestrictRelationalDatabases`. Add a description if you like, e.g. *Deny relational database services in workloads*.
3. **Visual editor** (the right-hand panel):
   - **Add actions** → choose service **RDS** → tick **All actions (`rds:*`)**
   - **Add actions** → **RDS Data API** → **All actions (`rds-data:*`)**
   - **Add actions** → **RDS IAM Authentication** → **All actions (`rds-db:*`)**
   - **Effect:** make sure every statement is **Deny**
   - **Add a resource:** **All resources** (`"*"`). The demo instructor fixed this by editing the JSON by hand.
4. Or replace the JSON in the editor with the following. It's the same policy and is the most reliable way:

   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Sid": "RestrictRelationalDatabases",
         "Effect": "Deny",
         "Action": ["rds:*", "rds-data:*", "rds-db:*"],
         "Resource": "*"
       }
     ]
   }
   ```

5. **Create policy**.

| Action prefix | Console service name | Covers |
|---|---|---|
| `rds:*` | RDS | All RDS management API calls (create, modify, delete DB instances…) |
| `rds-data:*` | RDS Data API | Running SQL over HTTPS against Aurora |
| `rds-db:*` | RDS IAM Authentication | `rds-db:connect`, logging in to a database with IAM credentials |

### 3c. Attach it to Workloads

1. Open **RestrictRelationalDatabases** → **Targets** tab → **Attach** → tick **Workloads** → **Attach policy**.

> [!success] Check
> **AWS accounts → Workloads → Policies** tab lists **FullAWSAccess** *and* **RestrictRelationalDatabases**.

> [!note] What this does
> Every account under Workloads, including any later placed in Trading System or Market Prediction, inherits the **explicit deny**. Even an IAM administrator in those accounts can't use RDS. **Corporate › Human Resources is unaffected.** Neither is your management account, because SCPs never apply to it ([[Organizational Units and Service Control Policies#^scp-two-rules]]).

---

## 4. Add the `MarketPrediction-Prod` Account

1. **AWS accounts** → **Add an AWS account** → **Create an AWS account**.
2. **AWS account name:** `MarketPrediction-Prod`
3. **Email address of the account's owner:** an address **you control** that has **never** been used for an AWS account, e.g. `you+MarketPredictionProd@gmail.com`
4. **IAM role name:** leave the default `OrganizationAccountAccessRole`. The management account uses this role to administer the new account.
5. **Create AWS account**. It shows as *creating* for a minute or two, then **Active**.

> [!tip] Put it where it belongs (not required by the sheet)
> New accounts land under **Root**. Tick `MarketPrediction-Prod` → **Actions → Move** → `Workloads › Market Prediction`. It then inherits `RestrictRelationalDatabases`, which you can see on the account's **Policies** tab.

> [!warning] It's a real account
> AWS emails its owner address. The account has **no password** until you use "Forgot password" on the root sign-in page. You don't need to sign in to it for this exercise. To administer it, use **Switch role** from the management account into `OrganizationAccountAccessRole`.

---

## 5. Verify the Whole Exercise

- [ ] Organization exists with **all features**. Your account is the **management account**.
- [ ] OUs: Root → `Corporate` → `Human Resources`; Root → `Workloads` → `Trading System`, `Market Prediction`
- [ ] Invitation to `111122223333` sent with the exact message (open, or rejected as expected)
- [ ] SCPs **enabled**
- [ ] `RestrictRelationalDatabases` denies `rds:*`, `rds-data:*`, `rds-db:*` on `"*"`
- [ ] Policy attached to **Workloads**
- [ ] `MarketPrediction-Prod` is **Active** (and optionally moved to Market Prediction)

---

## 6. Troubleshooting

| Problem | Likely cause | Fix |
|---|---|---|
| "Create an organization" missing, or it errors | Account already belongs to an organization (e.g. the course sandbox) | Use a standalone personal account, or study-only |
| Can't send the invitation | Management account email not verified | Click the verification email link, then retry |
| Invitation rejected immediately | `111122223333` is a documentation example ID | Expected. Move on. |
| No **Service control policies** option | Organization created with consolidated billing only | Enable **all features** (Settings) |
| SCP JSON rejected | Formatting error | Paste the JSON from step 3b exactly |
| Policy shows `"Resource": []` or a specific ARN | Visual editor resource step skipped | Set **All resources**, or use the JSON |
| "Email already associated with an AWS account" | Address was used before | Use a new plus-address |
| Account creation fails with a quota error | New organizations have a low default account quota | Request a quota increase, or reuse your study notes |

---

## 7. Cleanup – Personal Account

Nothing here costs money. Clean up only if you don't want the organization structure kept around, for example before trying [[Exercise 2 - AWS Control Tower - How To|Exercise 2]], which **reuses** it. In this order:

1. **Invitations** → cancel the open invitation, if any.
2. **Close `MarketPrediction-Prod`**: **AWS accounts** → select it → **Close** → confirm. It enters a **post-closure period** (about 90 days) and stays listed as *suspended*.
3. Detach `RestrictRelationalDatabases` from Workloads (**Targets** tab → **Detach**), then **delete** the policy.
4. Delete the OUs, **children first**: Trading System, Market Prediction, Human Resources, then Workloads, Corporate. OUs must be empty to delete.
5. Optionally, **Settings → Delete organization**. This only works once no member accounts remain. If AWS won't allow it while the closed account is in its post-closure period, leave it, since an empty organization costs nothing.
