---
title: "Secure and Private Connectivity – Flashcards"
course: AWS Cloud Architect – Designing AWS Architecture for Organizations
type: flashcards
source: "[[Secure and Private Connectivity]]"
created: 2026-10-17
---

#flashcards/aws/networking/security

Flashcards for [[Secure and Private Connectivity]].

Why should you limit the network traffic VPC resources can send and receive?
?
Most applications need only a few communications, and limiting traffic to those reduces the ways threat actors can target your systems.

What does a firewall do to traffic that doesn't meet its rules?
?
Drops it, so the traffic never reaches its destination.

What are the two complementary firewall technologies that protect VPC resources?
?
Security groups and network access control lists (NACLs).

What do security groups protect?
?
Elastic network interfaces: instances, VPC interface endpoints, and some Lambda capabilities.

What do network ACLs protect?
?
Subnets. They limit the traffic that can flow into and out of a subnet.

How does a security group treat reply traffic?
?
It lets replies to permitted traffic through without checking rules, because it assumes reply traffic is trustworthy.

How does a network ACL treat reply traffic?
?
It checks replies against its rules for that direction, just like requests.

Under what two conditions does a network ACL drop traffic?
?
When no rule permits it, or when an explicit deny rule blocks it.

For a request coming in from the internet, which firewall checks it first?
?
The network ACL (at the subnet boundary), then the security group.

For a request an instance sends out, which firewall checks it first?
?
The security group, then the network ACL.

What is a security group's default behavior for outbound traffic, and when might you change it?
?
It allows all outbound requests. You might restrict it in high-security environments.

Why must a network ACL allow ephemeral ports in the opposite direction?
?
Replies go to the client's short-lived high-numbered port, and the NACL checks replies. Without that rule, responses are dropped.

How do you block a specific malicious IP range for a whole subnet when security groups can't deny?
?
Add a network ACL explicit deny rule, evaluated before any allow rules.

What is a VPC endpoint?
?
A resource in a VPC that acts as a side door to another AWS service, keeping that traffic inside the AWS network.

Which services do gateway endpoints support, and how do they work?
?
Only S3 and DynamoDB. They add an entry to chosen route tables that redirects that service's requests to the endpoint.

How do interface endpoints work, and which services do they support?
?
They create an elastic network interface in at most one subnet per AZ, as the connection point to the service. They support most AWS services.

What technology implements interface endpoints?
?
AWS PrivateLink.

Why does AWS recommend a DNS name for an interface endpoint?
?
So applications can refer to the endpoint by name rather than by IP address.

Which firewall protects an interface endpoint, and why?
?
A security group, because an interface endpoint is an elastic network interface.

Why is a VPC endpoint valuable for compliance even though same-Region traffic usually stays on AWS's network anyway?
?
It removes the need for an internet route, it can be restricted by an endpoint policy, and resources can verify requests came through it. That makes private access enforceable and auditable.

How do you stop a compromised host from copying data to an attacker's bucket through an S3 endpoint?
?
Attach an endpoint policy that allows access only to the organization's approved buckets.
