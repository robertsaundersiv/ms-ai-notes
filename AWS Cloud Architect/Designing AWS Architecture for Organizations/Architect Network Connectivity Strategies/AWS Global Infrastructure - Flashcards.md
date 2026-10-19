---
title: "AWS Global Infrastructure – Flashcards"
course: AWS Cloud Architect – Designing AWS Architecture for Organizations
type: flashcards
source: "[[AWS Global Infrastructure]]"
created: 2026-10-17
---

#flashcards/aws/global-infrastructure

Flashcards for [[AWS Global Infrastructure]].

What is an AWS Region?
?
A massive cluster of AWS hardware located in the area of a major city, connected to other Regions by AWS's dedicated fiber-optic backbone.

What is an Availability Zone?
?
An independent cluster of data centers within a Region, with its own separate power and networking, located miles from any other AZ.

What is the minimum number of Availability Zones in an AWS Region?
?
Three.

Why is a fault in one Availability Zone unlikely to affect another in the same Region?
?
Each AZ has separate power and networking and is physically located miles away from the others.

How many Regions does a typical AWS solution need, and how is the Region usually chosen?
?
Usually one, the Region closest to the users of the solution.

When is a multi-Region architecture justified?
?
For mission-critical systems that must stay reliable even through a city-sized disaster.

What is the minimum number of Availability Zones a well-architected solution should use, and why?
?
At least two, so that a fault in one AZ doesn't prevent access to all of the solution's resources.

Which AWS services are automatically multi-AZ, and which make you choose the AZ?
?
S3 and DynamoDB automatically use multiple AZs. EC2 lets you choose the AZ for each resource.

How do Regions, VPCs, subnets, and resources nest?
?
A VPC is deployed in a Region. Its subnets sit in that Region's AZs. Compute resources live in subnets.

If each of two independent AZs is 99.9% available, what is the availability of a design that survives while either is up?
?
1 − (0.001)² = 99.9999%, assuming the AZs fail independently.

Why might an AZ name like us-west-1b exist in one AWS account but not another, and how do you compare AZs across accounts?
?
AZ names are mapped to physical AZs differently per account (and some Regions expose only some AZs). Compare by AZ ID (e.g. usw1-az1), which is the same in every account.

Besides latency to users, what factors should drive Region selection?
?
Compliance and data-residency rules, which services are available in the Region, and price.
