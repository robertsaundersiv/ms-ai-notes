---
title: "Cost Optimization and Analysis Strategies – Flashcards"
course: AWS Cloud Architect – Designing AWS Architecture for Organizations
type: flashcards
source: "[[Cost Optimization and Analysis Strategies]]"
created: 2026-10-17
---

#flashcards/aws/cost-management/optimization

Flashcards for [[Cost Optimization and Analysis Strategies]].

What is rightsizing?
?
Matching a resource's type and size to its actual measured demand, so it's neither under-performing nor wasting money.

What does AWS Compute Optimizer do?
?
Recommends the right resources for each workload, covering EC2, RDS, containers, and Lambda.

Is Compute Optimizer enabled by default, and at what scope can you turn it on?
?
No. You opt in, either for one account or for all accounts in an AWS organization.

How long after opting in does Compute Optimizer produce recommendations?
?
Resources typically need about 30 hours of running data, and recommendations then take up to 24 hours to generate.

How much history does Compute Optimizer analyze by default, and what does that cost?
?
The last 14 days of data, free of charge.

What does Compute Optimizer's enhanced infrastructure metrics option provide?
?
Analysis of 93 days of history, for an extra charge.

What inputs does Compute Optimizer use for EC2 recommendations?
?
CPU and GPU utilization, memory usage, network consumption, and storage use (EBS volumes and instance store).

What are the three findings Compute Optimizer can assign to a resource?
?
Under-provisioned, over-provisioned, or optimized.

What accompanies a Compute Optimizer recommendation to change instance type?
?
The best-fit instance type, an estimated monthly savings amount, and a performance risk percentage.

What does the performance risk percentage in a Compute Optimizer recommendation mean?
?
The estimated likelihood that the recommended instance can't support the workload's demand.

Why should you rightsize before buying Savings Plans or Reserved Instances?
?
Downsizing after committing can leave the commitment under-used, wasting the money already committed.

What does AWS Cost Anomaly Detection monitor for?
?
Sudden, surprising changes in spending patterns, while allowing for normal growth.

What kinds of spending does Cost Anomaly Detection flag as anomalies?
?
Use of a never-used service, spending in a never-used Region, and unusually high spend on a regularly used service.

What are the four types of Cost Anomaly Detection monitor?
?
AWS services, linked account, cost allocation tag, and cost category.

When should you use an AWS services cost monitor?
?
When you want to track each service's spending trend separately within an account.

When should you use a linked-account cost monitor?
?
When an account belongs to a single workload or department, so its aggregated spend is what matters.

How do AWS Budgets and Cost Anomaly Detection differ in what they compare spend against?
?
Budgets compare spend to a fixed number you set. Anomaly detection compares spend to your own learned spending pattern.

What does the Cost Optimization Hub provide?
?
Consolidated cost-saving recommendations across the accounts you opt in, ideally the whole organization, with an export option.
