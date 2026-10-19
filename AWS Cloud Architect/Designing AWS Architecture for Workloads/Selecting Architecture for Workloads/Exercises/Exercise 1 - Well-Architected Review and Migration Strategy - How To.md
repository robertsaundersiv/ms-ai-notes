---
title: "Exercise 1 – Well-Architected Review and Migration Strategy – How To"
aliases:
  - C2 L1 Exercise 1 How To
  - Health Metrics Kubernetes review
course: AWS Cloud Architect – Designing AWS Architecture for Workloads
lessons:
  - C2-L1-A09 Exercise 1 Solution
type: how-to
created: 2026-10-18
related:
  - "[[Cloud Migration Strategies]]"
  - "[[Optimized Architectures and the Migration Lens]]"
tags:
  - aws/well-architected
  - aws/migration/strategies
  - aws/lab
  - how-to
---

# Exercise 1 – Well-Architected Review and Migration Strategy – How To

> [!abstract] Goal
> Given the spec of a new Health Metrics Inc workload, **perform a six-pillar Well-Architected review** of its current on-prem state and **choose a migration strategy** (rehost / replatform / refactor / retire) with a rationale. It's a **paper exercise**: nothing is built in AWS and nothing costs money.

**Concepts:** [[Optimized Architectures and the Migration Lens]] · [[Cloud Migration Strategies]] · **Next lab:** [[Exercise 2 - Convert a Spark ETL Job to AWS Glue - How To]]
**Source:** built from the **solution video** (C2-L1-A09). The exercise brief wasn't in the transcript bundle. From the solution, the workload is a **Kubernetes application on physical on-prem servers, accessed over a VPN**. Use the brief's exact details where they differ.

---

## 1. Read the Spec and Decompose the Architecture

List the current components layer by layer, the way the lecture decomposes every workload:

| Layer | What to record | Exercise workload (from the solution) |
|---|---|---|
| Networking | Routers, switches, VPN, load balancers | **VPN** for secure access |
| Compute | Servers, clusters, orchestration | **Kubernetes cluster** on physical servers |
| Storage | Local disk, NAS, SAN | *(per the brief)* |
| Database | Engine and version | *(per the brief)* |
| Load profile | Steady, peaky, unpredictable | Servers **provisioned for peak** |

✅ **Check:** you can say in one sentence what the app is (monolith / microservices / data processing) and what runs it.

---

## 2. Do the Six-Pillar Review

For each pillar, write **one strength and one weakness** of the current setup. The solution's answers:

| Pillar | Finding (solution) |
|---|---|
| Operational excellence | Managing Kubernetes on **physical infrastructure** adds significant operational complexity |
| Security | The VPN gives secure access, but **on-prem infrastructure security** is always a concern |
| Reliability | Kubernetes provides resilience, but **hardware failures** on-prem could hit availability |
| Performance efficiency | Efficient at the software level, but **manual hardware upgrades** are very hard |
| Cost optimization | Servers **provisioned for peak load** → overprovisioned infrastructure |
| Sustainability | An **always-on, single-use** cluster consumes significant energy |

✅ **Check:** each row names a concrete cause, not just "could be better".

---

## 3. Spot the Pattern

Ask where the red flags live:

- In the **application/software**? → refactor.
- In the **infrastructure/hardware**, with cloud-friendly software? → **replatform**.
- Everywhere, with low business value? → retire.
- Low strategic value, short deadline? → rehost.

Here every weakness is about **hardware and its management**. Kubernetes itself already gives software-level resilience and efficiency.

---

## 4. Choose and Justify the Strategy

> [!success] Solution
> **Replatform to Amazon EKS.** The Kubernetes application stays largely the same while **AWS manages the underlying hardware** (and the Kubernetes control plane). That removes the hardware-driven red flags: no physical upgrades, no hardware single points of failure, and capacity that can track demand rather than peak.

A good rationale has three parts:
1. **What stays:** Kubernetes manifests and container images.
2. **What changes:** the hosting, to managed EKS (plus, optionally, managed node groups or Fargate, and an AWS load balancer).
3. **Which pillars improve:** operational excellence, reliability, cost, sustainability.

✅ **Check:** the strategy follows from the review, and you could defend why it's *not* refactor (the software isn't the problem) and *not* rehost onto EC2 (you'd keep self-managing Kubernetes).

---

## 5. Verify

- [ ] Every pillar has a finding.
- [ ] The strategy is one of the four Rs and is justified by the findings.
- [ ] The rationale says what stays, what changes, and which pillars improve.
- [ ] Optional: the target services are named (EKS, ECR for images, ELB, EBS/EFS for storage).

---

## 6. Troubleshooting

| Problem | Fix |
|---|---|
| Torn between replatform and refactor | Ask whether the **code or data model** must change. If not, replatform |
| Want ECS instead of EKS | ECS fits apps **without** Kubernetes. This app already uses it, so EKS keeps the investment |
| Review feels generic | Attach evidence: utilization, incidents, upgrade effort, cost |

## 7. Cleanup

Nothing to clean up. No AWS resources are created.
