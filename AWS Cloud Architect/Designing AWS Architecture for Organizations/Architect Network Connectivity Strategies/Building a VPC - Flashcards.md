---
title: "Building a VPC – Flashcards"
course: AWS Cloud Architect – Designing AWS Architecture for Organizations
type: flashcards
source: "[[Building a VPC]]"
created: 2026-10-17
---

#flashcards/aws/networking/vpc

Flashcards for [[Building a VPC]].

What are Steady Volatility Partners' networking requirements for its quant-trading VPC?
?
Some compute needs internet access. Other parts must stay strictly disconnected from the internet. Compute must read and write S3. S3 data must never cross the internet.

What is the scope of a VPC, and where can its resources live?
?
A VPC exists entirely inside one Region, but holds resources in any of that Region's Availability Zones.

What is the purpose of a subnet?
?
To group related compute resources (for example web servers in one, database servers in another). It is their network home and connection point to the rest of the solution.

What does a subnet's route table determine?
?
The complete list of destinations computers in that subnet can reach, and where traffic goes next to reach each one.

When can several subnets share one route table?
?
When they have identical routing needs. Sharing reduces the number of route tables to manage.

How is traffic between subnets in the same VPC routed?
?
Automatically, by the local route that uses the VPC's built-in routing.

What two conditions make a subnet public?
?
The VPC has an internet gateway attached, and the subnet's route table has a route that targets that internet gateway.

What makes a subnet private?
?
Either its VPC has no internet gateway, or its route table has no route to the internet gateway.

What is a private subnet typically used for?
?
Resources other parts of the solution must reach, but which must never directly accept a request from an internet client.

How can an instance in a private subnet download updates without becoming reachable from the internet?
?
Route its outbound traffic through a NAT gateway, which allows outbound requests and blocks inbound connections from the internet.

Where must a NAT gateway be deployed, and why?
?
In a public subnet, so it can have a public IP address and receive responses from the internet. Private instances reach it through the VPC's internal routing.

Which route targets connect a VPC to an on-premises network?
?
A virtual private gateway (VGW) or a transit gateway (TGW).

How do resources reach S3 or DynamoDB privately without crossing the internet?
?
Through a gateway VPC endpoint, which adds a route-table entry that sends that service's traffic to the endpoint.

A subnet has both a default route to a NAT gateway and an S3 prefix-list route to a gateway endpoint. Which path does S3 traffic take?
?
The gateway endpoint, because routing picks the most specific matching route.

How does a VPC keep a subnet strictly disconnected from the internet?
?
By giving its route table no route to an internet gateway or NAT gateway. The absence of a route is the primary control.

How many addresses does a /26 subnet contain, and how many are usable on AWS?
?
64 addresses, 59 usable, because AWS reserves 5 in every subnet.

Which five addresses does AWS reserve in every subnet?
?
The network address, the next address (VPC router), the one after (DNS server), the one after that (reserved for future use), and the last address (broadcast).

Why is "usable = total − 2" wrong for sizing AWS subnets?
?
That generic rule only reserves the network and broadcast addresses. AWS also reserves the router, DNS, and a future-use address, so usable = total − 5.

Why can't headquarters connect after only creating and attaching a virtual private gateway?
?
A VGW is just the AWS side. A customer gateway (the on-premises device details) and a Site-to-Site VPN connection are also needed before tunnels can come up.

How many addresses does a /22 subnet contain?
?
1,024 (2 to the power of 10).

Why must a /22 block start on a third-octet value that is a multiple of 4?
?
A /22 spans four consecutive third-octet values, so it must align to a 4-block boundary.

Why should a gateway endpoint be associated with every route table whose compute uses the bucket?
?
Subnets whose route table lacks the endpoint route send S3 traffic over the internet-gateway path, breaking a "never cross the internet" requirement.

Why leave a VPC's main route table with only local routes and associate every subnet explicitly?
?
Any subnet created later without an explicit association uses the main table, so it starts isolated instead of accidentally public.

Besides a route to the internet gateway, what does an instance in a public subnet need to communicate with the internet?
?
A public IPv4 address, either auto-assigned at launch or an Elastic IP.

How do you give private subnets outbound-only internet access over IPv6?
?
Use an egress-only internet gateway, because NAT gateways don't apply to IPv6.
