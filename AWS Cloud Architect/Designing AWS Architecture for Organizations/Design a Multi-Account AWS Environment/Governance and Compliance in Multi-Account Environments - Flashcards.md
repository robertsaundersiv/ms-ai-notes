---
title: "Governance and Compliance in Multi-Account Environments – Flashcards"
course: AWS Cloud Architect – Designing AWS Architecture for Organizations
type: flashcards
source: "[[Governance and Compliance in Multi-Account Environments]]"
created: 2026-10-17
---

#flashcards/aws/governance

Flashcards for [[Governance and Compliance in Multi-Account Environments]].

What is governance in the context of cloud architecture?
?
Balancing speed and agility with accountability: explaining spend and value to leadership, and proving to regulators that sensitive data is protected.

What are systems that help IT comply with governance best practices called?
?
Compliance regimes or governance frameworks.

What are the two layers of building a compliant cloud solution?
?
Building on a cloud platform that is itself well-governed, and implementing your own workload controls that stop unsafe actions and notify on drift.

What is AWS Artifact?
?
A free self-service portal where AWS users download auditor and accreditation documents showing that AWS itself is well-governed.

What does AWS Artifact prove, and what does it not prove?
?
It proves AWS's own platform compliance. It doesn't prove that your workload's configuration is compliant.

What are the three Control Tower control guidance levels?
?
Mandatory, strongly recommended, and elective.

What is special about Control Tower mandatory controls?
?
They are always on and can't be disabled.

What do Control Tower mandatory controls protect, and why?
?
Control Tower's own resources (Log Archive S3 buckets, CloudTrail, CloudWatch Logs, Config rules, IAM roles, SNS topics and subscriptions), so Control Tower keeps working and keeps its visibility.

What is the default state of strongly recommended and elective controls?
?
Off. You enable them as needed.

What kinds of risks do strongly recommended controls address?
?
Unrestricted inbound access such as open SSH, publicly accessible S3 buckets or RDS databases, CloudTrail not logging, and an unsecured root user.

Which root-user protections are among the strongly recommended controls?
?
Requiring MFA on the root user and disallowing root user access keys.

Why are root-user controls critical?
?
The root user has unrestricted power, so stolen root credentials could be used to script the deletion of every resource in an account.

What do elective controls typically enforce?
?
Enterprise-grade restrictions, such as preventing changes to S3 encryption, logging, bucket policies, lifecycle, and replication, and requiring MFA for deletions.

What does AWS Audit Manager do?
?
Generates reports demonstrating compliance with frameworks, using evidence gathered automatically from your accounts.

Where does AWS Audit Manager get its evidence?
?
From AWS Config, AWS CloudTrail, and its own API calls that inspect your environment's configuration.

Why enable Control Tower controls at the OU level rather than per account?
?
One enablement covers every account in the OU, including accounts added later, so effort scales with OUs, not accounts.
