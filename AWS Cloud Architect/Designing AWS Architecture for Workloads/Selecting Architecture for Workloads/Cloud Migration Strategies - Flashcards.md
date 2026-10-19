---
title: "Cloud Migration Strategies – Flashcards"
course: AWS Cloud Architect – Designing AWS Architecture for Workloads
type: flashcards
source: "[[Cloud Migration Strategies]]"
created: 2026-10-18
---

#flashcards/aws/workloads/migration-strategies

Flashcards for [[Cloud Migration Strategies]].

What is a migration strategy?
?
The approach used to move a workload into the AWS cloud. AWS publishes prescriptive guidance for implementing each one.

What is the rehost strategy, and its nickname?
?
"Lift & shift": move the application with little or no change.

What kind of application is the usual candidate for rehosting?
?
Low-complexity, non-strategic applications, where the time to change the application isn't worth the effort.

What is the replatform strategy, and its nickname?
?
"Lift, tinker & shift": migrate while making key optimizations, usually by moving onto AWS managed services (e.g. adding Auto Scaling groups).

What is the refactor strategy?
?
Re-architecting the core application to fit its usage patterns, taking full advantage of cloud-native features for agility, performance, and scalability.

What kind of application is the usual candidate for refactoring?
?
Strategic applications with strong business demand to scale, accelerate releases, and reduce cost.

What does the retire strategy mean?
?
Decommissioning or archiving the application and shutting down its service stack.

What are two reasons to retire an application?
?
To eliminate the cost of hosting and maintaining it, and to reduce the security risk of unsupported operating systems or components. Low usage and poor performance are further triggers.

Which three of AWS's seven Rs does the course leave out?
?
Retain (keep on-prem for now), relocate (hypervisor-level move, e.g. VMware Cloud on AWS), and repurchase (switch to a different product, usually SaaS).

Why was the Health Trend Analysis Spark cluster refactored rather than rehosted?
?
The architecture itself was the problem (always-on, underutilized, high fixed cost, complex to manage), and AWS has purpose-built managed big-data services that remove that overhead.

Why was the legacy reporting tool retired?
?
It was obsolete, insecure, unreliable, costly, and low-value, and decommissioning was already scheduled, so migrating wasn't worth the effort.

What was the defining problem of the Doctor Scheduling System?
?
High volumes of concurrent reads and writes at peak, on a single server with no automatic failover.

Why was the Doctor Scheduling System moved to a managed serverless platform rather than rewritten from scratch?
?
Cloud-native features like auto scaling and managed infrastructure fix its scaling and reliability problems without a complete rewrite.

What strategy fits an application already running on an on-prem Kubernetes cluster, and what target?
?
Replatform to Amazon EKS. The Kubernetes app stays largely the same, and AWS manages the underlying infrastructure.

In the Exercise 1 review, where did all the red flags come from?
?
The hardware and its management (physical cluster ops, hardware failures, manual upgrades, peak provisioning, always-on energy), not the software.

What general rule does the Kubernetes exercise illustrate?
?
When the software is already cloud-friendly and the problems are all infrastructure, replatform onto a managed service instead of refactoring.

What practical test separates a replatform from a refactor?
?
If the data model or execution model changes (e.g. relational → key-value, server → event-driven functions), it's a refactor. If only the hosting changes, it's a replatform.

Why should "retire" be considered in every assessment?
?
It's usually the highest-return decision: it removes both cost and attack surface with almost no migration effort.

What is the risk of rehosting a peak-sized server unchanged?
?
You carry the same overprovisioning into the cloud and now pay for it hourly. Rightsizing and a later replatform should be planned.
