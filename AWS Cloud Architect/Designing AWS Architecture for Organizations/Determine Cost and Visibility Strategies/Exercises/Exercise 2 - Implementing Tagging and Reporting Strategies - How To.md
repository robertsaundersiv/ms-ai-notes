---
title: "Exercise 2 – Implementing Tagging and Reporting Strategies – How To"
aliases:
  - L3 Exercise 2 How To
  - Implementing tagging and reporting strategies
course: AWS Cloud Architect – Designing AWS Architecture for Organizations
lessons:
  - L3-A07 Exercise 2
type: how-to
created: 2026-10-17
updated: 2026-10-17
related:
  - "[[Tagging Strategies and Cost Allocation]]"
  - "[[Exercise 1 - Using AWS Cost Explorer and Compute Optimizer for Cost Analysis - How To]]"
tags:
  - aws/cost-management/tagging
  - aws/organizations
  - aws/lab
  - how-to
---

# Exercise 2 – Implementing Tagging and Reporting Strategies – How To

> [!abstract] Goal
> Make sure resources are **tagged for cost allocation**, and that **reports** reach the finance team:
> 1. Create the Organizations **tag policy** `SVPTagPolicy1` and attach it to `DeveloperTestArea`
> 2. **Activate cost allocation tags**: four AWS-generated and two user-defined
> 3. **Export** a CUR 2.0 report (prefix `CostReport`) and the Cost Optimization Hub recommendations (prefix `OptimHubRecs`)
>
> It takes about 20 minutes.

**Concepts:** [[Tagging Strategies and Cost Allocation]] · **Previous lab:** [[Exercise 1 - Using AWS Cost Explorer and Compute Optimizer for Cost Analysis - How To]]
**Source:** the official exercise sheet, cross-checked against the instructor's demo (video L3-A07). (The sheet's objectives list also says "Enable Compute Optimizer". That's a carry-over from Exercise 1; no step here does it.)

> [!warning] Optional, and not possible on Udacity-provided accounts
> - **Step 1 (tag policy):** needs the **management account** of an organization with the `DeveloperTestArea` OU from [[Exercise 2 - Implementing Governance Policies in AWS Control Tower - How To|Lesson 2's Control Tower lab]].
> - **Step 2:** in an organization, cost allocation tags are activated from the **management account**.
> - **Step 3's second export:** needs the Cost Optimization Hub enabled ([[Exercise 1 - Using AWS Cost Explorer and Compute Optimizer for Cost Analysis - How To#3. Enable the Cost Optimization Hub|Exercise 1, step 3]]).
> - **Cost:** policies and tags are free. Exports store files in **S3**, which costs pennies a month.

---

## 0. Before You Start

**Values from the sheet:**

| Item | Value |
|---|---|
| Tag policy name | `SVPTagPolicy1` |
| Tag 1 key | `svp:costcenter`, **all lowercase**, "use this capitalization" |
| Tag 1 allowed values | `0001`, `0002`, `0003` |
| Tag 1 enforced on | `ec2:instance`, `ec2:natgateway`, `dynamodb:table`, `s3:bucket`, `sagemaker:model-package` |
| Tag 2 key | `svp:typeofenvironment`, use this capitalization |
| Tag 2 allowed values | `Development`, `Testing`, `Production` |
| Tag 2 enforced on | **All resource types** |
| Policy target | `DeveloperTestArea` OU |
| AWS-generated tags | `aws:autoscaling:groupName`, `aws:cloudformation:stack-id`, `aws:createdBy`, `aws:ec2launchtemplate:id` |
| User-defined tags | `Name`, `Owner` |
| Export 1 | Standard export, **CUR 2.0**, prefix `CostReport` |
| Export 2 | Standard export, **Cost Optimization Hub recommendations**, prefix `OptimHubRecs` |

> [!note] Lowercase on purpose
> The sheet uses `svp:costcenter`, not the demo's `SVP:CostCenter`. Tag keys are **case-sensitive**, and "use this capitalization" means only the exact lowercase form is compliant ([[Tagging Strategies and Cost Allocation#^tag-rules]]).

---

## 1. Configure the Organizations Tag Policy

1. **AWS Organizations → Policies → Tag policies**. If prompted, **Enable tag policies**.
2. **Create policy** → **Policy name:** `SVPTagPolicy1`.

> [!warning] Two different "tags" sections
> The form's top **Tags** section tags the *policy object itself*. Leave it empty. Define the enforced tags in the **New tag key** sections below it, as the instructor points out.

### New tag 1 – `svp:costcenter`

3. **Tag key:** `svp:costcenter`
4. Tick **Use the capitalization that you specified above for the tag key**.
5. Tick **Specify allowed values for this tag key** → add `0001`, `0002`, `0003`.
6. Tick **Prevent noncompliant operations for this tag** → **Specify resource types** → select:
   - `ec2:instance`
   - `ec2:natgateway`
   - `dynamodb:table`
   - `s3:bucket`
   - `sagemaker:model-package`

### New tag 2 – `svp:typeofenvironment`

7. **Add tag key** → `svp:typeofenvironment`
8. Tick **Use this capitalization**.
9. **Allowed values:** `Development`, `Testing`, `Production`
10. **Prevent noncompliant operations** → **all resource types** (as the sheet says; select every service or resource type the console offers).
11. **Create policy**.

### Attach it

12. Open `SVPTagPolicy1` → **Targets** → **Attach** → select **`DeveloperTestArea`** → **Attach policy**.

**JSON equivalent** (*beyond the lecture*, for the policy's JSON editor). Tag 2's "all resource types" is shown with per-service `ALL_SUPPORTED` entries. Add the services you use, or set it in the visual editor:

```json
{
  "tags": {
    "svp:costcenter": {
      "tag_key": { "@@assign": "svp:costcenter" },
      "tag_value": { "@@assign": ["0001", "0002", "0003"] },
      "enforced_for": {
        "@@assign": [
          "ec2:instance",
          "ec2:natgateway",
          "dynamodb:table",
          "s3:bucket",
          "sagemaker:model-package"
        ]
      }
    },
    "svp:typeofenvironment": {
      "tag_key": { "@@assign": "svp:typeofenvironment" },
      "tag_value": { "@@assign": ["Development", "Testing", "Production"] },
      "enforced_for": {
        "@@assign": ["ec2:ALL_SUPPORTED", "s3:ALL_SUPPORTED", "dynamodb:ALL_SUPPORTED"]
      }
    }
  }
}
```

> [!success] Check
> **AWS accounts → DeveloperTestArea → Policies** lists `SVPTagPolicy1`.

> [!note] What it enforces
> In `DeveloperTestArea` accounts, tagging a listed resource with `svp:costcenter = 9` or `SVP:CostCenter = 0001` is **rejected**. A resource with **no** `svp:costcenter` tag at all is **still allowed**. Requiring the tag needs an SCP ([[Tagging Strategies and Cost Allocation#^tag-enforcement-layers]]).

---

## 2. Enable Cost Allocation Tags

1. **Billing and Cost Management → Cost allocation tags**.
2. **AWS-generated cost allocation tags** tab → select:
   - `aws:autoscaling:groupName`
   - `aws:cloudformation:stack-id`
   - `aws:createdBy`
   - `aws:ec2launchtemplate:id`
   → **Activate** → confirm.
3. **User-defined cost allocation tags** tab → select **`Name`** and **`Owner`** → **Activate** → confirm.

> [!warning] If `Name` or `Owner` isn't listed
> User-defined keys only appear after they've been **used on a resource**, which can take up to about 24 hours. Tag any resource (an S3 bucket is fine) with `Owner = <you>`, then come back. Activation applies **going forward**, not retroactively.

> [!success] Check
> All six tags show **Active**. They'll appear as columns in the CUR export.

---

## 3. Export Cost Reports

### 3a. CUR 2.0 export (prefix `CostReport`)

1. **Billing and Cost Management → Data Exports → Create**.
2. **Export type:** **Standard data export**
3. **Export name:** e.g. `SVP-CUR2-CostReport`
4. **Data table:** **CUR 2.0**
5. **Time granularity:** Hourly (the demo's default) or Daily. **File format:** Parquet (good for Athena) or CSV (good for spreadsheets).
6. **Data export storage settings:** **Select an existing bucket**, or **Create a new bucket** (e.g. `svp-cost-reports-<random>`, Region us-west-1). AWS applies the bucket policy the export needs.
7. **S3 path prefix:** `CostReport`
8. **Create**.

### 3b. Cost Optimization Hub recommendations export (prefix `OptimHubRecs`)

1. **Data Exports → Create**.
2. **Export type:** **Standard data export**
3. **Data table:** **Cost optimization recommendations** (from Cost Optimization Hub)
4. **Export name:** e.g. `SVP-OptimHubRecs`
5. **S3 bucket:** the same bucket, or another
6. **S3 path prefix:** `OptimHubRecs`
7. **Create**.

> [!note] Delivery timing
> The first files usually arrive within about **24 hours**. An empty bucket right after creation is normal.

---

## 4. Verify the Whole Exercise

- [ ] `SVPTagPolicy1` exists:
  - [ ] `svp:costcenter` (lowercase, values `0001`/`0002`/`0003`, enforced on the 5 resource types)
  - [ ] `svp:typeofenvironment` (Development/Testing/Production, all resource types)
- [ ] `SVPTagPolicy1` attached to **DeveloperTestArea**
- [ ] AWS-generated tags **Active**: `aws:autoscaling:groupName`, `aws:cloudformation:stack-id`, `aws:createdBy`, `aws:ec2launchtemplate:id`
- [ ] User-defined tags **Active**: `Name`, `Owner`
- [ ] Data Exports lists a **CUR 2.0** export with prefix `CostReport`
- [ ] Data Exports lists a **cost optimization recommendations** export with prefix `OptimHubRecs`

---

## 5. Troubleshooting

| Problem | Likely cause | Fix |
|---|---|---|
| No **Tag policies** option | Not the management account, or the organization lacks all features | Management account with all features, or study only |
| `DeveloperTestArea` OU missing | Lesson 2's Control Tower lab not done | Create the OU in Organizations, or attach to another OU for practice |
| JSON rejected on `enforced_for` | Unsupported resource type string | Use the visual editor's resource list |
| `Owner` or `Name` not listed | Key never used on a resource | Tag a resource, then wait up to 24 hours |
| Can't activate tags | Member account in an organization | Activate from the management account |
| No recommendations data table | Cost Optimization Hub not enabled | Do Exercise 1, step 3 first |
| Bucket name taken | S3 names are global | Add a random suffix |

---

## 6. Cleanup

1. **Data Exports** → delete both exports.
2. **Empty**, then **delete** the bucket (if you created one).
3. Optionally deactivate the six cost allocation tags.
4. **Organizations → Tag policies → SVPTagPolicy1** → **Targets** → detach from `DeveloperTestArea` → delete the policy.
