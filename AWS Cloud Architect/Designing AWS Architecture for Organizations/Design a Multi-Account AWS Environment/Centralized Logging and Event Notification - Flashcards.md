---
title: "Centralized Logging and Event Notification – Flashcards"
course: AWS Cloud Architect – Designing AWS Architecture for Organizations
type: flashcards
source: "[[Centralized Logging and Event Notification]]"
created: 2026-10-17
---

#flashcards/aws/logging

Flashcards for [[Centralized Logging and Event Notification]].

What three needs do logs serve in a cloud architecture?
?
Resolving trouble tickets, forensics such as finding who deleted a resource, and informing the design of the next version.

What does "everything is an API call" mean in AWS?
?
Whether an action starts in the console, the CLI, or an SDK, it ends up as a request to the service's API.

What does AWS CloudTrail log, and where does it store logs?
?
API read and write interactions with AWS services, plus console sign-ins and events from scheduled events. It stores them in S3.

What does CloudTrail not capture?
?
Network requests to compute resources you created, such as traffic to EC2 instances or RDS databases.

What should you use to capture traffic to EC2 or RDS resources?
?
VPC Flow Logs or application logging, since CloudTrail only covers calls to AWS services.

What does AWS Config do?
?
Monitors resource configurations, detects drift from defined settings, notifies administrators, and can trigger automated remediation.

How do CloudTrail and AWS Config differ?
?
CloudTrail records who did what through API calls. Config records what resources look like over time and flags misconfiguration.

Where should an organization aggregate its logs?
?
In the Log Archive account.

Why keep logs in a separate Log Archive account?
?
Admins or attackers in workload accounts can't alter or delete the evidence, and analysis happens in one place.

What query options does CloudWatch Logs Insights offer?
?
A simple proprietary query language, or natural-language queries that AI translates into it.

What is a CloudWatch Logs subscription filter used for?
?
Forwarding log entries to other applications, such as Lambda functions.

How does Amazon Athena run queries over logs, and how is it priced?
?
It loads data from S3 into temporary compute, runs SQL, and releases the compute. It charges a flat price per TB of data read.

What does Athena need before querying log data, and how can it be generated?
?
A table definition describing the data's structure, which an AWS Glue crawler can generate.

Why does storage layout drive Athena cost?
?
Athena charges per data scanned, so partitioning and columnar compressed formats reduce the bytes each query reads.

What does Amazon OpenSearch Service provide for log analysis?
?
A cluster that ingests data from many sources for querying and dashboards, commonly paired with Kibana.

When are third-party tools such as Datadog or Splunk a good choice for logs?
?
When the organization already uses them, or needs features that augment AWS's built-in log management.
