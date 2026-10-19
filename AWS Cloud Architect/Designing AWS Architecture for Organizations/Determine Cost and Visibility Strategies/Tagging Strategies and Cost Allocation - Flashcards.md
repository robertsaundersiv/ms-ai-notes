---
title: "Tagging Strategies and Cost Allocation – Flashcards"
course: AWS Cloud Architect – Designing AWS Architecture for Organizations
type: flashcards
source: "[[Tagging Strategies and Cost Allocation]]"
created: 2026-10-17
---

#flashcards/aws/cost-management/tagging

Flashcards for [[Tagging Strategies and Cost Allocation]].

Why isn't finding an expensive resource enough to cut costs?
?
You also need to know what it's for, who owns it, and who pays before you can safely turn it off.

What questions should a resource's tags be able to answer?
?
Who created it, which project or application it belongs to, which department, whether it's dev/test or production, whom to contact, which cost center pays, and whether it can be turned off off-hours.

What is an AWS tag?
?
A key–value pair of metadata attached to a resource, describing its role in the IT environment.

How many tags can most AWS resources have?
?
Up to 50 unique tags.

Are AWS tags case-sensitive, and what does that imply?
?
Yes. You need a capitalization and naming standard before you start tagging.

What prefix do tags applied automatically by AWS carry?
?
The lowercase prefix aws: .

Why must you never store sensitive or personal information in tags?
?
Tags aren't encrypted, and they aren't designed to hold confidential or personal data.

Why add a custom prefix to your organization's tag keys?
?
It identifies the tags as yours and keeps them distinct from AWS-generated and third-party tags.

What four purposes do tags serve, according to AWS?
?
Cost allocation, automation, resource organization, and access control (by referencing tags in IAM policies).

What is the ideal way to make sure resources are tagged correctly at creation?
?
Deploy through infrastructure as code (CloudFormation or Terraform) that sets tags automatically, offered as Service Catalog products.

What does the Tag Editor let you do?
?
Search resources by Region, resource type, and existing tags, find mis-tagged resources, and apply tags in batches.

What is the Resource Groups Tagging API used for in a tagging strategy?
?
Building scripts and applications that scan the environment for resources that are tagged incorrectly.

Why do some enterprises automatically quarantine or delete untagged resources?
?
It strongly encourages tagging, because an expensive, ownerless resource may disappear within hours or days.

What is a cost allocation tag?
?
A tag activated in Billing so that it appears as a column in billing reports, letting costs be allocated to teams.

What two kinds of cost allocation tags can you activate?
?
AWS-generated tags, such as created-by or stack ID, and user-defined tags you create for your own financial management.

How do AWS Config and service control policies differ in enforcing tagging?
?
Config detects resources missing required tags, then notifies and can remediate. SCPs prevent creating non-compliant resources in the first place.

What does an AWS Organizations tag policy enforce?
?
Standardized tag key capitalization and allowed values, optionally preventing non-compliant tagging operations on chosen resource types.

Does a tag policy require that a tag be present on new resources?
?
No. It validates tag keys and values when used. Requiring a tag needs an SCP that denies requests where the tag is missing.

What is the AWS Cost and Usage Report?
?
The most detailed AWS billing dataset, and the primary source accounting teams use to understand spend and allocate it to departments.

Where do you create a Cost and Usage Report, and which version is current?
?
In Billing and Cost Management under Data Exports. CUR 2.0 is the current standard, and CUR 1.0 is legacy.

How do activated cost allocation tags make chargeback easier?
?
They become columns in the Cost and Usage Report, so costs can be grouped by team or cost center with simple spreadsheet or query work.
