---
title: "Monitoring and Logging Network Traffic – Flashcards"
course: AWS Cloud Architect – Designing AWS Architecture for Organizations
type: flashcards
source: "[[Monitoring and Logging Network Traffic]]"
created: 2026-10-17
---

#flashcards/aws/networking/monitoring

Flashcards for [[Monitoring and Logging Network Traffic]].

Why isn't implementing network security features enough on its own?
?
They don't make a network immune to attack. You also need ongoing monitoring to verify traffic matches the design and to detect threat actors probing or attacking.

What is a detective control?
?
A capability that identifies proper and improper use of a system, as opposed to a preventive control that blocks it.

What is the most direct way to see what's happening in an AWS network?
?
Capture its traffic with VPC Flow Logs.

At what scopes can VPC Flow Logs be enabled?
?
A whole VPC, particular subnets, or individual network interfaces (including those of instances and VPC endpoints).

Where can VPC Flow Logs be delivered?
?
S3, CloudWatch Logs, or other destinations through Amazon Data Firehose.

What must exist for the VPC Flow Logs service to write to its destination?
?
An IAM role with permission to write logs, that the VPC Flow Logs service is trusted to assume.

What are the two halves of a service role such as the one used by flow logs?
?
A permissions policy that defines what the role can do, and a trust policy that defines who (which service) can assume it.

How can you query VPC flow logs stored in CloudWatch Logs?
?
With CloudWatch Logs Insights.

How can you forward flow log events to a custom application as they arrive?
?
With a CloudWatch Logs subscription filter.

How do you get an automatic alert from patterns in flow logs?
?
Create a metric filter that turns matching log events into a metric, then a CloudWatch alarm on that metric.

How can you query flow logs stored in S3?
?
With Amazon Athena.

Which kinds of traffic are not captured by VPC Flow Logs?
?
Traffic to the VPC's built-in DNS server and router, DHCP traffic, instance metadata service traffic, and Windows license activation traffic.

Why can't flow logs reveal DNS-based data exfiltration, and what fills the gap?
?
Queries to the VPC's built-in DNS server aren't logged in flow logs. Route 53 Resolver query logging fills the gap.

Do VPC Flow Logs contain packet contents?
?
No. They record flow metadata such as addresses, ports, protocol, byte counts, and accept/reject. Payload capture needs traffic mirroring.

What does a spike in rejected flow-log records from one source usually indicate?
?
Someone probing for weaknesses, such as a port scan. Preventive controls are blocking it, but it warrants attention.

Why set a retention period on a flow-log log group?
?
Without one, logs accumulate indefinitely and storage costs keep growing.
