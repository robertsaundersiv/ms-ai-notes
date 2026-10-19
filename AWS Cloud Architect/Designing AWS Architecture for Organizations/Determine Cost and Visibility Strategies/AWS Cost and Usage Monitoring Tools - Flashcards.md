---
title: "AWS Cost and Usage Monitoring Tools – Flashcards"
course: AWS Cloud Architect – Designing AWS Architecture for Organizations
type: flashcards
source: "[[AWS Cost and Usage Monitoring Tools]]"
created: 2026-10-17
---

#flashcards/aws/cost-management/monitoring

Flashcards for [[AWS Cost and Usage Monitoring Tools]].

What two questions does cloud cost visibility need to answer?
?
What are we paying for, and are we getting business value for it?

When an AWS bill is higher than expected, what is usually the cause?
?
The bill accurately reflects the services that were used, so the first step is finding out what was used.

What is AWS Cost Explorer?
?
The first-stop tool for viewing and analyzing AWS spend as charts and graphs, with filters, forecasts, and saved reports.

How is Cost Explorer enabled, and how long until data appears?
?
It's enabled the first time you open its console, and past cost data appears within 24 hours.

How much history and how far a forecast does Cost Explorer show?
?
The preceding 13 months of costs, and a 12-month forecast based on recent usage trends.

By which dimensions can Cost Explorer filter spend to find outliers?
?
Service, Region, Availability Zone, instance type, platform (such as Linux or Windows), and account.

What are Cost Explorer saved reports?
?
Stored report configurations that sit alongside AWS's built-in reports, such as daily and monthly costs and Savings Plans or RI usage.

What does AWS Budgets do?
?
Sets planned spend or usage and alerts when actual or forecasted values cross thresholds, including under-use of commitments.

What is a zero spend budget for?
?
Accounts for testing new ideas. It notifies you if any spending occurs beyond the Free Tier.

Why would you create a budget that alerts on low usage?
?
To ensure pre-committed Savings Plans or Reserved Instances are actually being used, since unused commitments waste money.

Where can AWS Budgets send notifications?
?
SNS topics, email addresses, and chat tools such as Slack and Microsoft Teams.

What kinds of thresholds can a cost budget alert on?
?
Actual or forecasted spend crossing a fixed dollar amount or a percentage of the budget, with multiple thresholds per budget.

Why add forecasted-spend thresholds to a budget?
?
They warn you early in the period that you're on track to overspend, before actual spend crosses the limit.

What can AWS budget actions do when spending exceeds a budget?
?
Apply IAM policies with deny permissions to users, groups, or roles; attach SCPs to OUs; and turn off EC2 or RDS instances.

Where must an SCP budget action be configured?
?
In the organization's management account, because only it can change SCPs.

Why are budget actions that shut down instances best limited to dev/test environments?
?
Turning off production systems can disrupt live users, causing lost business and customer goodwill.

What does AWS Budgets need in order to perform budget actions?
?
A service role with permissions to make the changes.

What does AWS Trusted Advisor's cost optimization category do?
?
Runs dozens of checks that flag where money is being wasted.

Which under-utilized resources do Trusted Advisor cost checks flag?
?
EC2 instances and their EBS volumes, Redshift clusters, RDS database servers, and unused NAT gateways.

Why does Trusted Advisor flag Lambda functions that often hit their timeout?
?
Repeated timeouts waste compute, since the function runs to its limit without completing.

Why does Trusted Advisor flag S3 buckets with no lifecycle policy?
?
Objects can accumulate endlessly, so storage costs grow without limit.
