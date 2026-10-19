---
title: "Advanced VPC Connectivity – Flashcards"
course: AWS Cloud Architect – Designing AWS Architecture for Organizations
type: flashcards
source: "[[Advanced VPC Connectivity]]"
created: 2026-10-17
---

#flashcards/aws/networking/hybrid

Flashcards for [[Advanced VPC Connectivity]].

Why do many cloud solutions need connectivity back to corporate headquarters?
?
They must be managed from the corporate network, or they need to reach systems that still live on-premises.

What are the two main ways to connect a VPC to an on-premises location?
?
VPN connectivity through a virtual private gateway, or a transit gateway.

What does a virtual private gateway (VGW) connect?
?
A VPC to a VPN device at the customer's location.

How does a VGW VPN connection provide redundancy?
?
It establishes two IPsec tunnels in an active-passive configuration. If one fails, the other keeps the connection running.

What usable bandwidth does a VGW VPN connection provide, and why?
?
1.25 Gbps. Each tunnel runs at 1.25 Gbps, but only one tunnel is active at a time.

What must a subnet's route table contain to use a VGW connection?
?
A route for the on-premises address range that targets the virtual private gateway.

What is a transit gateway?
?
A massively scalable Regional router that can interconnect up to 5,000 networks, including VPCs, VPN connections, and Direct Connect links.

What does a VPC peering connection do?
?
Connects one VPC to one other VPC, in the same or a different AWS account, so they can communicate.

What IP-address condition must hold for two VPCs to peer?
?
They must have no IP addresses in common. Overlapping CIDRs prevent peering.

Why should an organization avoid overlapping VPC CIDRs even across different accounts?
?
Overlap would block any future peering between those VPCs, so non-overlapping ranges keep that option open.

VPC A peers with B, and B peers with C. Can A talk to C?
?
No. Peering isn't transitive. A and C need their own peering connection.

How many VPCs can participate in one peering connection?
?
Exactly two. More VPCs need multiple peering connections.

What are the steps to establish a working VPC peering connection?
?
One owner requests the peering, the other owner accepts it (across accounts), and both VPCs add route-table entries that send the other VPC's CIDR through the peering connection.

What happens if only one side of a peering connection has a route to the other?
?
Traffic can't make a round trip. Replies have no path back, so connections fail.

How many peering connections does a full mesh of n VPCs require?
?
n(n − 1) / 2, which grows quadratically. A transit gateway needs only n attachments.

Why is non-transitive peering consistent with least-privilege networking?
?
Every VPC-to-VPC path must be created explicitly, so no network becomes reachable as a side effect of another connection.
