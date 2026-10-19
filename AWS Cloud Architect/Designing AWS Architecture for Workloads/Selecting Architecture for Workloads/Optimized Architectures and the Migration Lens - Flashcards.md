---
title: "Optimized Architectures and the Migration Lens – Flashcards"
course: AWS Cloud Architect – Designing AWS Architecture for Workloads
type: flashcards
source: "[[Optimized Architectures and the Migration Lens]]"
created: 2026-10-18
---

#flashcards/aws/workloads/migration-lens

Flashcards for [[Optimized Architectures and the Migration Lens]].

What is an optimized cloud architecture?
?
One whose resources satisfy business requirements while minimizing expense, balancing scalability, performance, and cost efficiency, with security designed in.

What are the three consequences of a non-optimal architecture?
?
Overprovisioning (inflated cost), underprovisioning (performance bottlenecks), and security vulnerabilities.

What causes overprovisioning in a cloud architecture?
?
Not being elastic enough to scale down during low demand, so you pay for more resources than you need.

What causes underprovisioning in a cloud architecture?
?
Not being elastic enough to scale up for peak demand, which causes performance bottlenecks and slows critical operations.

What is cloud "sticker shock"?
?
A sharp rise in operating costs once applications run in the cloud, typical when moving from a fixed-cost (on-prem) model to a variable-cost model without changing how cost is managed.

In the retailer case study, what separated the successful migration from the struggling one?
?
Deliberate migration planning (and a planned move from monolith to microservices) versus rushing to meet deadlines, which created multiple inconsistent environments and sticker shock.

What did the struggling retailer have to buy after migrating?
?
Tools to manage workload placement, data movement, and financial tracking.

What is the AWS Well-Architected Framework?
?
AWS's guide to designing and operating systems that are reliable, secure, efficient, and cost-effective in the cloud, organized into six pillars.

What is the Well-Architected Migration Lens?
?
A domain-specific extension of the framework with best practices for migrating on-premises or hybrid workloads into fully cloud-based environments.

What are the six Well-Architected pillars?
?
Operational excellence, security, reliability, performance efficiency, cost optimization, and sustainability.

What does the operational excellence pillar focus on?
?
Running and monitoring systems to deliver business value, e.g. monitoring performance with CloudWatch.

What does the security pillar focus on, and which practices did the lecture name?
?
Protecting information, systems, and assets: least privilege, AWS KMS for keys, and AWS Secrets Manager for secrets.

What does the reliability pillar focus on?
?
The workload performing its intended function consistently and correctly, through backups, load balancers, and replicas for redundancy.

How are the performance efficiency and cost optimization pillars connected?
?
Performance efficiency is using compute resources efficiently, and that directly drives cost. Wasted capacity is wasted spend.

What does the sustainability pillar focus on?
?
Minimizing the environmental impact of cloud workloads, e.g. rightsizing, using shared infrastructure, and reducing redundancy where possible.

What are the three phases of an AWS migration?
?
Assess, Mobilize, and Migrate & Modernize.

What is the output of the Assess phase?
?
A comprehensive inventory of applications, dependencies, usage patterns, and business value, which forms the basis of migration planning.

What happens in the Mobilize phase?
?
You select the migration strategy: what changes, if any, you make to the application as it moves to the cloud.

What three things happen in the Migrate & Modernize phase?
?
Choose the architecture pattern, choose the AWS services that implement it, and deploy it.

Which four migration strategies does the course treat as part of the migration lens?
?
Rehost, replatform, refactor, and retire.

Why do the Well-Architected pillars need explicit trade-offs?
?
They pull against each other. Reliability wants redundancy, while cost and sustainability want less of it, so a review should state which pillar is favored and why.

If a fleet is sized for peak demand that is 10× average demand, what is its utilization?
?
About 10%. Roughly 90% of the capacity you pay for is idle, which is the economic argument for elastic designs.
