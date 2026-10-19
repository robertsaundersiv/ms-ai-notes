---
title: "DNS and Network Resolution – Flashcards"
course: AWS Cloud Architect – Designing AWS Architecture for Organizations
type: flashcards
source: "[[DNS and Network Resolution]]"
created: 2026-10-17
---

#flashcards/aws/networking/dns

Flashcards for [[DNS and Network Resolution]].

Where is the built-in DNS server in every VPC?
?
At a reserved address in the VPC's range: the base of the VPC CIDR plus two (e.g. 172.19.0.2).

What DNS configuration does a new EC2 instance get automatically?
?
It sends name-resolution requests to the VPC's DNS server and gets an internal DNS name generated from its private IPv4 address, plus a public one if it has a public IP.

What is Amazon Route 53?
?
AWS's fully managed DNS service. It resolves names, acts as a domain registrar, hosts DNS zones, and provides advanced routing.

What can Route 53 do as a domain registrar?
?
Register new domains, and transfer in domains registered with other registrars.

What is the difference between a private and a public hosted zone?
?
A private hosted zone controls DNS within one or more VPCs. A public hosted zone is exposed to the internet.

Which advanced routing strategies does Route 53 support?
?
Multi-location and active-passive failover, latency-based routing, geographic routing, and distributing traffic across locations.

Why can't on-premises DNS resolve names in a Route 53 private hosted zone by default?
?
Cloud and on-premises use entirely separate DNS systems, and the private zone isn't visible outside its VPCs.

What does a Route 53 Resolver inbound endpoint do?
?
Receives DNS queries forwarded from the on-premises DNS server, so on-premises clients can resolve cloud names.

What does a Route 53 Resolver outbound endpoint do?
?
Forwards cloud-originated DNS queries for the corporate domain to the on-premises DNS server, as directed by a forwarding rule.

What decides which queries go through an outbound resolver endpoint?
?
A resolver forwarding rule that maps a domain to target DNS servers, associated with the VPC.

Why should resolver endpoints have IP addresses in at least two Availability Zones?
?
Each IP is an interface in one AZ, so two AZs keep hybrid DNS working if one AZ fails.

Besides a forwarding rule, what must exist for an outbound endpoint to reach on-premises DNS?
?
A network path, such as a VPN route, to the target DNS server's IP.

Where can DNS query logs be sent for troubleshooting?
?
S3, CloudWatch Logs, or Amazon Data Firehose.

Why should lab Route 53 Resolver components be removed promptly, and in what order?
?
They can generate significant ongoing costs. Disassociate the VPC from the rule, delete the rule, then delete the inbound and outbound endpoints.

Why does DNS failover never take effect instantly?
?
Resolvers cache answers for the record's TTL, so clients keep using the old answer until it expires.
