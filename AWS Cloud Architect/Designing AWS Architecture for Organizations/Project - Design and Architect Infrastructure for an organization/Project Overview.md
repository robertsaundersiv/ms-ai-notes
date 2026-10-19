---
title: "Project – Design and Architect Infrastructure for an Organization"
aliases:
  - A Taste of Your Own Medicine
  - Excipient Technologies Project
  - Project Overview
course: AWS Cloud Architect – Designing AWS Architecture for Organizations
type: project
status: in-progress
created: 2026-10-17
related:
  - "[[Designing AWS Architecture for Organizations]]"
  - "[[Project Report – Excipient Technologies]]"
tags:
  - aws/project
  - aws/organizations
  - aws/networking
  - aws/cost-management
  - project
---

# Project – Design and Architect Infrastructure for an Organization

> [!abstract] The mission
> As **senior cloud architect** for **Excipient Technologies**, a pharmaceutical company, unify three AWS environments into one **centralized, cost-effective, resilient** architecture:
> - an existing **Control Tower** environment (the target)
> - a **standalone AWS account** built by a project manager
> - an **AWS Organizations** network inherited through an **acquisition**
>
> Then connect networks securely, enforce governance with tagging, and design budget controls.

**Section hub:** [[Designing AWS Architecture for Organizations]] · **Compiled report:** [[Project Report – Excipient Technologies]]
**Sources:** the project overview, instructions, environment setup, Cloud Lab rules, rubric, and the report template PDF (5 pages).

---

## 1. Deliverables Map

| Step | How it's done | Working note | Builds on |
|---|---|---|---|
| **1. Multi-account architecture design** | Scenario + report (no AWS) | [[Step 1 - Multi-Account Architecture Design]] | [[AWS Organizations]], [[Organizational Units and Service Control Policies]], [[AWS Control Tower]] |
| **2. Network connectivity** | **Hands-on in the Cloud Lab** | [[Step 2 - Network Connectivity - How To]] → [[Step 2 - Connectivity Report]] | [[Building a VPC]], [[Advanced VPC Connectivity]], [[Secure and Private Connectivity]], [[Monitoring and Logging Network Traffic]] |
| **3. Governance with tagging** | Scenario + report (no AWS) | [[Step 3 - Tagging Governance]] | [[Tagging Strategies and Cost Allocation]] |
| **4. Cost management controls** | Scenario + report (no AWS) | [[Step 4 - Cost Management Controls]] | [[AWS Cost and Usage Monitoring Tools]] |

> [!important] Only Step 2 touches AWS
> The environment setup page says Steps 1, 3, and 4 are completed ==using scenarios and the report template, without directly accessing AWS services==. Their JSON and budget outputs are **simulated**.

---

## 2. Rubric Checklist

### Multi-Account AWS Architecture Design
- [ ] OU hierarchy includes **Root, Corporate OU, Workloads OU, Acquired Businesses OU** → [[Step 1 - Multi-Account Architecture Design#1. OU Hierarchy]]
- [ ] Integration steps for **onboarding the standalone account** → [[Step 1 - Multi-Account Architecture Design#3. Standalone Account Integration]]
- [ ] Integration steps for **linking the acquired organization's accounts** → [[Step 1 - Multi-Account Architecture Design#4. Acquired Organization Integration]]
- [ ] **Governance and security policies (SCPs)** → [[Step 1 - Multi-Account Architecture Design#5. Governance and Security Policies]]
- [ ] **Diagram** of the architecture that matches the hierarchy → [[Step 1 - Multi-Account Architecture Design#6. Final Architecture Diagram]]

### Establish Network Connectivity
- [ ] **VPC peering** between two VPCs in **separate accounts or Regions**
- [ ] **Route tables, security groups, and network ACLs** updated
- [ ] Verified with **ping** (and curl), plus **VPC Flow Logs / CloudWatch Logs**
- [ ] **Screenshots** of the successful connection and of the logs → [[Step 2 - Connectivity Report]]

### Implement Governance with Tagging Strategies
- [ ] **Tagging strategy table** (keys such as Environment, CostCenter, Owner, with purposes) → [[Step 3 - Tagging Governance#1. Tagging Strategy Table]]
- [ ] **SCP JSON** denying resource creation without required tags → [[Step 3 - Tagging Governance#3. SCP – Deny Creation Without Required Tags]]
- [ ] **AWS Config rule JSON** flagging non-compliant resources → [[Step 3 - Tagging Governance#4. AWS Config Rule – Detect Non-Compliant Resources]]

### Configure Cost Management Controls
- [ ] **Budget configurations**: names, thresholds, notifications → [[Step 4 - Cost Management Controls#2. Budget Configuration]]
- [ ] **Budget actions** that notify and/or enforce → [[Step 4 - Cost Management Controls#3. Budget Actions]]
- [ ] **Simulated outputs** for alerts and enforcement → [[Step 4 - Cost Management Controls#5. Simulated Outputs]]

---

## 3. Cloud Lab Rules That Shape Step 2

| Rule (from "AWS Sign In and Costs") | Impact on this project |
|---|---|
| **Regions:** `us-east-1` (default), `us-east-2`, `us-west-1`, `us-west-2` only | Use **us-east-1** and **us-west-2** for cross-Region peering (the setup page's example) |
| **Budget:** \$25 for the whole course (about \$10 is typical). Hitting it ends the session and **loses your work**. | Use **t3.micro / t2.micro**. **No NAT gateways.** Terminate everything the same day. |
| **Session time limit** | Work is saved unless the budget is exhausted. Re-launch from the Cloud Gateway. |
| **Billing dashboard disabled**; Cost Explorer works | Track spend in **Cost Explorer** |
| **Concurrency limits**: exceeding them **deactivates the account** | Launch exactly **two** instances |
| **No personal information** in resources: no emails, names, phone numbers, or tags with personal data | Use role or team aliases (e.g. `Owner = cloud-architecture`), never your name or email |
| One account only | "Separate accounts" isn't possible, so peer across **Regions** (the rubric allows "accounts **or** Regions") |
| Organizations and Route 53 restricted | Steps 1, 3, and 4 are design and simulation only, which is why the project is structured this way |

---

## 4. Submission Checklist

- [ ] Fill **Your Name** and **Date of Submission** in [[Project Report – Excipient Technologies]]
- [ ] Review and personalize the drafted text in Steps 1, 3, and 4. You should be able to defend every choice.
- [ ] Complete Step 2 in the Cloud Lab and paste your **real IDs and screenshots** into [[Step 2 - Connectivity Report]]
- [ ] Export the diagrams as images. In Obsidian, Mermaid renders in reading view: screenshot it, or export the note to PDF.
- [ ] Export [[Project Report – Excipient Technologies]] to **PDF**, or copy it into the template PDF/DOCX
- [ ] **Terminate all Step 2 resources** ([[Step 2 - Network Connectivity - How To#9. Cleanup – Do This the Same Day]])
