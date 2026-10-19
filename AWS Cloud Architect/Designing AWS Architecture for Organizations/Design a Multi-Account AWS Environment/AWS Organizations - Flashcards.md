---
title: "AWS Organizations – Flashcards"
course: AWS Cloud Architect – Designing AWS Architecture for Organizations
type: flashcards
source: "[[AWS Organizations]]"
created: 2026-10-17
---

#flashcards/aws/organizations

Flashcards for [[AWS Organizations]].

Why do growing organizations use AWS accounts rather than VPCs as the container for projects?
?
Accounts give projects greater independence, reducing the risk that a mistake in one project harms another.

What are three common ways organizations divide workloads across multiple AWS accounts?
?
An account per project, an account per department, and separate accounts per environment (development, test/staging, production) for one project.

What three management problems does a large number of standalone AWS accounts create?
?
A separate bill per account, separate user lists that make permissions hard to track, and independent security policies that are hard to keep consistent.

What does AWS charge for an account, for AWS Organizations, and for Control Tower?
?
Nothing for the accounts or the services themselves. Charges come only from resources running in the accounts.

What is an organizational unit (OU)?
?
A logical grouping of accounts within an organization, by function, compliance needs, or common security controls. OUs can be nested.

What is the management account in AWS Organizations?
?
The account that hosts the Organizations service and from which organization changes are made.

Do organization policies such as SCPs apply to the management account?
?
No. Policies applied to the organization don't apply to the management account.

How does an existing AWS account join an organization?
?
It is invited by the organization and accepts, becoming a member account under an OU.

What is the difference between consolidated billing and all features in AWS Organizations?
?
Consolidated billing only aggregates the accounts' bills. All features adds centralized policy management and integration with other AWS services.

How does consolidated billing reduce costs?
?
Usage across all accounts is aggregated before volume-discount tiers are applied, so more usage reaches cheaper tiers.

Why can pooling usage under consolidated billing never cost more than billing accounts separately?
?
When unit prices fall at higher usage tiers, the cost of the total usage is at most the sum of each account's separate cost.

What are service control policies?
?
The centerpiece of Organizations policy management. They enable or disable AWS API calls, or entire services, for accounts, OUs, or the whole organization.

Besides SCPs, which policy types does AWS Organizations offer?
?
Tag policies (standardized tagging), backup policies (backup plans), and AI services opt-out policies (opting out of AI data collection).

What four components make up AWS Control Tower?
?
Account Factory to create accounts, a landing zone that secures accounts consistently, controls for policy management, and a dashboard for an overview.

Why should workloads not run in the management account?
?
Organization policies such as SCPs don't apply to it, so it's the one account without guardrails.
