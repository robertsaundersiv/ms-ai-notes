---
title: "Networking for Organizations – Flashcards"
course: AWS Cloud Architect – Designing AWS Architecture for Organizations
type: flashcards
source: "[[Networking for Organizations]]"
created: 2026-10-17
---

#flashcards/aws/networking

Flashcards for [[Networking for Organizations]].

Which physical networking components does AWS replace with virtual services?
?
Routers, switches, gateways, and load balancers. They are provided as virtual services instead of physical hardware.

What is the key difference between cloud networking and on-premises networking?
?
In the cloud you define the desired outcomes of the network design and AWS delivers them. You don't physically deploy and manage hardware.

What is the design target for traffic in a trustworthy network?
?
The only traffic in the network is required traffic. Every flow a business function needs is allowed, and nothing else is.

What happens if a network design is too closed?
?
Critical IT systems can't communicate with each other, so business functions fail.

What are the two costs of allowing unnecessary network traffic?
?
At best it wastes limited network resources. At worst it opens a path for malicious software to disrupt or harm systems.

Why do over-permissive network rules tend to pile up over time while missing rules get fixed quickly?
?
A missing rule breaks something visibly, so someone complains. An excess rule breaks nothing, so it stays unnoticed while it widens the attack surface.

Which kinds of resources or capabilities require the architect to configure the network directly?
?
Virtual machines, database servers, and similar resources; hybrid communication with on-premises sites; and high-level security tools such as AWS Network Firewall.

What is AWS Network Firewall?
?
A managed network firewall and intrusion detection/prevention system (IDS/IPS) for VPCs.

How do security groups enforce least-privilege traffic between application tiers?
?
Each tier's security group allows its port only from the previous tier's security group, not from broad IP ranges. Anything not explicitly allowed is denied.
