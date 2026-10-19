---
title: "A Taste of Your Own Medicine: Design and Architect Infrastructure for an Organization"
aliases:
  - Excipient Project Report
course: AWS Cloud Architect – Designing AWS Architecture for Organizations
type: project-report
status: draft
created: 2026-10-17
related:
  - "[[Project Overview]]"
tags:
  - aws/project
  - project
---

# A Taste of Your Own Medicine: Design and Architect Infrastructure for an Organization

**Project Report: Designing AWS Architecture for Organizations**

> [!tip] How to use this note
> This compiles the four step notes in the **template's order** through embeds. Edit text in the **step notes**, not here. To submit: fill in your details, complete [[Step 2 - Connectivity Report]], switch to reading view, then **Export to PDF** (or copy the sections into the template). Remove this callout before exporting.

| Your Information | |
|---|---|
| **Your Name** | ‹your name› |
| **Date of Submission** | ‹date› |
| **Course Title** | "Designing AWS Architecture for Organizations" |

---

## Executive Summary

Excipient Technologies, a leading pharmaceutical maker, is consolidating its AWS network architecture. The company's network includes:
- an **AWS Control Tower-based** network
- a **standalone AWS account** created by a project manager
- an **AWS Organizations-based** network from an acquired business

As senior cloud architect, my role is to integrate these environments, establish network connectivity, enforce governance, and implement cost controls.

**Key goals and how this report meets them:**

| Goal | Approach | Section |
|---|---|---|
| Integrate the standalone and acquired accounts | A single Control Tower organization with Corporate, Workloads (Dev/Prod), and Acquired Businesses OUs. Invite, enroll, then graduate accounts. | Step 1 |
| Secure, reliable interconnectivity | Inter-Region VPC peering between the database (10.0.0.0/16) and analytics (192.168.0.0/16) VPCs, with least-privilege SGs and NACLs, verified with ping, curl, and Flow Logs | Step 2 |
| Tagging and governance | Required `Environment`, `CostCenter`, `Owner` tags. Prevented by SCP, detected by AWS Config `REQUIRED_TAGS`. | Step 3 |
| Cost management | OU- and tag-scoped AWS Budgets, with automatic actions in Development and manual approval for Production and Acquired | Step 4 |

---

## Multi-Account AWS Architecture Design (Step 1)

**Objective:** design a multi-account architecture and integration strategy.

### OU Hierarchy

![[Step 1 - Multi-Account Architecture Design#1. OU Hierarchy]]

### Integration Strategy

![[Step 1 - Multi-Account Architecture Design#2. Integration Strategy – Overview]]

![[Step 1 - Multi-Account Architecture Design#3. Standalone Account Integration]]

![[Step 1 - Multi-Account Architecture Design#4. Acquired Organization Integration]]

### Governance and Security Policies

![[Step 1 - Multi-Account Architecture Design#5. Governance and Security Policies]]

### Final Architecture

![[Step 1 - Multi-Account Architecture Design#6. Final Architecture Diagram]]

---

## Network Connectivity Plan (Step 2)

**Objective:** establish VPC peering connectivity between accounts.

![[Step 2 - Connectivity Report#Report Section]]

---

## Governance with Tagging Strategies (Step 3)

**Objective:** define and enforce a tagging strategy using SCPs and AWS Config rules.

![[Step 3 - Tagging Governance#1. Tagging Strategy Table]]

![[Step 3 - Tagging Governance#2. Enforcement Design]]

![[Step 3 - Tagging Governance#3. SCP – Deny Creation Without Required Tags]]

![[Step 3 - Tagging Governance#4. AWS Config Rule – Detect Non-Compliant Resources]]

---

## Cost Management Plan (Step 4)

![[Step 4 - Cost Management Controls#Report Section]]

![[Step 4 - Cost Management Controls#1. Notification Channels]]

### 5.1 Budget Configuration

![[Step 4 - Cost Management Controls#2. Budget Configuration]]

### Actions

![[Step 4 - Cost Management Controls#3. Budget Actions]]

![[Step 4 - Cost Management Controls#4. Escalation Flow]]

![[Step 4 - Cost Management Controls#5. Simulated Outputs]]
