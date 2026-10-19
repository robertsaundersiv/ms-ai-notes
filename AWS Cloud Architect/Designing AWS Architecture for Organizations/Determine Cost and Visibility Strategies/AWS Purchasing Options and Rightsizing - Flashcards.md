---
title: "AWS Purchasing Options and Rightsizing – Flashcards"
course: AWS Cloud Architect – Designing AWS Architecture for Organizations
type: flashcards
source: "[[AWS Purchasing Options and Rightsizing]]"
created: 2026-10-17
---

#flashcards/aws/cost-management/purchasing

Flashcards for [[AWS Purchasing Options and Rightsizing]].

What are the three main drivers of IT and cloud costs?
?
Compute, storage, and data transfer.

What are the three main EC2 purchasing options?
?
On-Demand, Savings Plans and Reserved Instances, and Spot Instances.

What are the benefits and drawbacks of On-Demand Instances?
?
Instant compute with no long-term commitment, billed only while running, but at full retail price.

What kind of workload suits On-Demand Instances?
?
Workloads with unpredictable demand, where you turn capacity on and off as needed.

What discounts do Savings Plans and Reserved Instances offer?
?
About 30% for committing to 1 or 3 years, and up to 72% with partial or full prepayment.

What kind of workload suits Savings Plans or Reserved Instances?
?
Workloads with a consistent, predictable baseline of compute demand.

Why should you track utilization of Savings Plans and Reserved Instances?
?
Committed capacity is paid for whether or not it's used, so unused commitments waste money.

At what utilization does a commitment with discount d beat On-Demand?
?
When the fraction of hours you'd use the instance exceeds 1 − d, for example 70% for a 30% discount.

What is the difference between zonal and regional Reserved Instances?
?
Zonal RIs apply in one AZ and reserve capacity there. Regional RIs apply across a Region's AZs.

What is the difference between standard and convertible Reserved Instances?
?
Standard RIs give the deepest discount but fix the instance family. Convertible RIs can be exchanged for other types but have a smaller discount.

What happens to the unused portion of a Reserved Instance reservation?
?
It's lost, wasting the money spent on it.

What do you commit to with a Savings Plan?
?
A dollar amount per hour of compute spend, with usage across Regions counting toward it and anything above it billed at On-Demand rates.

What are the three kinds of Savings Plan?
?
Compute Savings Plans (EC2, Lambda, and Fargate), EC2 Instance Savings Plans, and SageMaker Savings Plans.

Which does AWS now recommend, Savings Plans or Reserved Instances?
?
Savings Plans, because they're newer and more flexible.

What is the key capacity difference between zonal Reserved Instances and Savings Plans?
?
Zonal RIs reserve capacity. Savings Plans don't, so the instance type you want might be unavailable at that moment.

What are Spot Instances?
?
Spare EC2 capacity sold at a deep discount, routinely 70% off and sometimes 80–90%, that AWS can reclaim.

How much warning do you get before AWS reclaims a Spot Instance?
?
Two minutes.

Why does AWS offer Spot Instances?
?
To earn revenue from surplus capacity that would otherwise sit idle as AWS adds hardware.

What workloads suit Spot Instances?
?
Interruptible work: batch processing, data analytics, graphics rendering, stateless web servers, and some containerized applications.

How should Spot be combined with other purchasing options for application servers?
?
Run Spot servers alongside servers of the same type on non-interruptible On-Demand or committed capacity.

When should data be stored in S3 Standard?
?
For hot data accessed at least once a month. It's stored across multiple AZs with millisecond access.

When does S3 Standard-IA save money, and what is its minimum storage duration?
?
When data is retrieved less than about once a month. Objects deleted early are billed for 30 days.

Why can S3 Standard-IA cost more than S3 Standard?
?
It charges per-GB retrieval fees, which outweigh the storage savings if data is retrieved too often.

What makes S3 One Zone-IA cheaper, and what data suits it?
?
It stores data in a single AZ. It's only for data that can be recreated from another, more resilient source.

What are the minimum storage durations for S3 Glacier and Glacier Deep Archive?
?
90 days for Glacier, and 180 days for Glacier Deep Archive.

What data suits the S3 Glacier storage tiers?
?
Archival data retrieved less often than once a quarter.

When should you use S3 Intelligent-Tiering, and what does it cost?
?
When access patterns are unknown or change over time. It charges a small per-object monitoring fee.

What does an S3 lifecycle policy do, and why should it include expiration?
?
It moves objects to cheaper classes as they age. Expiration deletes objects once they lose value, so storage costs don't grow forever.

What does Amazon S3 Storage Lens provide?
?
Aggregated usage metrics across all buckets in an account or organization, with trends, cost recommendations, and outlier detection.

How does S3 volume pricing work?
?
The per-GB price drops for usage above each tier threshold, such as above 50 TB and 450 TB, with usage pooled across an organization.
