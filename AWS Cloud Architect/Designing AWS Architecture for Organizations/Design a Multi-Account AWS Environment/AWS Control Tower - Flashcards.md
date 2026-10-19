---
title: "AWS Control Tower – Flashcards"
course: AWS Cloud Architect – Designing AWS Architecture for Organizations
type: flashcards
source: "[[AWS Control Tower]]"
created: 2026-10-17
---

#flashcards/aws/control-tower

Flashcards for [[AWS Control Tower]].

What is a landing zone?
?
A pre-configured, secure multi-account environment, with accounts and security restrictions in place so workloads are well-architected from day 1.

How did AWS's approach to building landing zones change over time?
?
AWS Professional Services first built them manually as a paid engagement. Control Tower now creates them automatically.

What does Control Tower rely on for its account structure?
?
AWS Organizations.

What happens when Control Tower is launched in an account with no AWS organization?
?
Control Tower creates the organization automatically, and that account becomes the management account for both Organizations and Control Tower.

What happens when Control Tower is launched where an AWS organization already exists?
?
It uses the existing organization. The existing management account becomes the Control Tower management account, and existing OUs can stay as they are or be registered with Control Tower.

What OU and accounts does Control Tower create automatically?
?
A Security OU containing an Audit account and a Log Archive account.

What optional OU can Control Tower create, and why?
?
A Sandbox OU for developer experimentation, which aligns with AWS best practices.

How are Control Tower preventive controls implemented, and what do they do?
?
With service control policies. They block API calls that would make the environment insecure or non-compliant.

How are Control Tower detective controls implemented, and what do they do?
?
With AWS Config rules. They spot misconfigured resources and raise alerts.

How are Control Tower proactive controls implemented, and what do they do?
?
With CloudFormation hooks. They prevent deployment of resources whose templates don't meet requirements.

In what order do proactive, preventive, and detective controls act?
?
Proactive acts before deployment, preventive at the API call, and detective after a resource exists or changes.

How do you bring an existing account that isn't in the organization under Control Tower?
?
Invite it into the organization (removing it from any other organization first), then enroll it in Control Tower.

What prerequisite must be met before an existing account can be enrolled in Control Tower?
?
An IAM role in the account that gives the Control Tower management account administrator privileges.

What does Control Tower Account Factory do?
?
Creates a new account, places it in the chosen OU, and applies all Control Tower security requirements automatically.

What does Account Factory Customization add?
?
Your own blueprints for specialized accounts, which Account Factory then creates.

Which AWS service is Account Factory built on, and what does that service do?
?
AWS Service Catalog, which turns CloudFormation templates into deployable products that non-technical users can launch.

What does AWS Resource Access Manager do?
?
Lets resources in one account be used by other accounts, an OU, or the whole organization.

What two sets of permissions govern a resource shared with AWS RAM?
?
The resource share's permissions set by the sharing account, and the consuming account's own IAM permissions.

How are effective permissions determined for a consuming account in AWS RAM?
?
Only the overlap of the resource share's permissions and the consumer's IAM permissions takes effect. The share sets the maximum.

Which Control Tower feature is an automated system for creating new accounts with security protocols applied?
?
Account Factory.

Which kind of Control Tower control actively blocks insecure actions within the AWS environment?
?
Preventive controls, which are implemented as SCPs that deny the API call.

Which kind of Control Tower control signals administrators when resources are misconfigured into an unsecured state?
?
Detective controls, which are implemented as AWS Config rules that alert on drift.

Which kind of Control Tower control stops a non-compliant CloudFormation template from being deployed?
?
Proactive controls, which are implemented as CloudFormation hooks.

Which Control Tower organizational unit is used for managing the security and auditing accounts?
?
The Security OU, which holds the Audit and Log Archive accounts.

Preventive and proactive controls both block things. How do you tell them apart?
?
Preventive controls block actions (API calls) in the environment. Proactive controls block templates before anything is deployed.
