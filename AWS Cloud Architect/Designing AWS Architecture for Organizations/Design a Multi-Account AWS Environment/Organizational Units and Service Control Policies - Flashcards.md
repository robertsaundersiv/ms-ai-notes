---
title: "Organizational Units and Service Control Policies – Flashcards"
course: AWS Cloud Architect – Designing AWS Architecture for Organizations
type: flashcards
source: "[[Organizational Units and Service Control Policies]]"
created: 2026-10-17
---

#flashcards/aws/organizations/scp

Flashcards for [[Organizational Units and Service Control Policies]].

What problems does a badly designed OU structure cause?
?
Confusion, duplicated administrative effort, and increased risk of configuration mistakes.

What benefits does a well-designed OU structure provide?
?
Consistent policy application, easier resource sharing with AWS RAM, and a target for automation to apply changes to groups of accounts.

Why does AWS not recommend OUs that mirror the corporate org chart?
?
Similar accounts exist across departments, so department OUs duplicate effort and increase misconfiguration risk.

How does AWS recommend grouping accounts into OUs?
?
By the function of the accounts, such as production workloads, security tooling, sandbox experimentation, or shared infrastructure.

How many top-level OUs does AWS best-practice guidance recommend?
?
Eleven.

What is the Workloads OU for, and how is it usually subdivided?
?
The company's business applications. It's split into production and non-production (test/staging) OUs.

What is the Sandbox OU for?
?
Developer experimentation, usually under tight spending limits or service restrictions.

Which two accounts are most notable in the Security OU?
?
An account for organization-wide log data and an account for auditing by trusted security staff.

What does the Infrastructure OU hold?
?
Shared services such as backup and restore, identity management, network management, and monitoring.

What are the Suspended, Transitional, Policy Staging, and Exceptions OUs for?
?
Suspended: accounts awaiting deletion. Transitional: accounts from mergers or acquisitions. Policy Staging: testing disruptive policy changes. Exceptions: accounts that fit nowhere else.

Where can developer accounts be placed in a recommended OU structure?
?
In a non-production OU under Workloads, or in the cost-limited Sandbox OU.

Where are SCPs created, and what can they be attached to?
?
They are created in the management account and attached to the root, an OU, or an account.

How do SCPs flow through an organization?
?
They inherit downward, from the root to OUs and from OUs to accounts.

Do service control policies grant permissions?
?
No. They restrict what IAM can grant. Only permissions granted by IAM and allowed by SCPs take effect.

What determines a principal's effective permissions in an account inside an organization?
?
The intersection of its IAM permissions with what every SCP at the account's level and above allows.

What is the effect of an implicit or explicit deny in any SCP above an account?
?
The permission is denied for that account, even if a lower-level SCP allows it.

What is FullAWSAccess, and where is it attached by default?
?
An SCP that allows all actions. It's attached by default to every account, every OU, and the root.

Root allows all, the OU allows S3 and EC2, and the account allows S3 and RDS. What is effective?
?
S3 only, because it's the only service allowed at every level.

Root allows all, the OU allows all but explicitly denies S3, and the account allows all. What is effective?
?
Everything except S3. The OU's explicit deny can't be overridden lower down.

What syntax do SCPs use, and how can they deny actions granularly?
?
The same syntax as IAM policies, using condition elements for fine-grained restrictions.

What are common uses of SCPs?
?
Restricting Regions or instance types, requiring MFA for sensitive actions, requiring encryption, protecting CloudTrail and logs, preventing direct internet access, and preventing accounts from leaving the organization.

Why can SCPs control almost anything in AWS?
?
Nearly every AWS action is an API call, and SCPs can revoke permission to any API action.

Why should a Region-restricting SCP exempt services like IAM and Organizations?
?
Global services are called through a single Region, so a blanket Region deny would break them.
