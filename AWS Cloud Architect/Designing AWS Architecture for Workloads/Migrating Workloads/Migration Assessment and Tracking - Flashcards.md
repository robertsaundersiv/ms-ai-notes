---
title: "Migration Assessment and Tracking – Flashcards"
course: AWS Cloud Architect – Designing AWS Architecture for Workloads
type: flashcards
source: "[[Migration Assessment and Tracking]]"
created: 2026-10-19
---

#flashcards/aws/workloads/migration-assessment

Flashcards for [[Migration Assessment and Tracking]].

Why assess the current environment before migrating?
?
To get a clear picture of what exists: dependencies to group servers into applications, and utilization to rightsize resources in AWS.

What are the two approaches of AWS Application Discovery Service?
?
Agentless discovery and agent-based discovery.

Which environments is agentless discovery designed for, and how is it deployed?
?
VMware environments. The Agentless Collector is an OVA file deployed through VMware vCenter.

What data does agentless discovery collect?
?
Static configuration and utilization metrics for virtual machines and databases.

Which environments does agent-based discovery support, and how is it deployed?
?
Both virtual machines and physical servers. The Application Discovery Agent is installed on each server.

What data does agent-based discovery collect?
?
Detailed system data, including system performance, network connections, and running processes.

How are the dependency data and utilization data from discovery used?
?
Dependencies group servers into applications that migrate together. Utilization data rightsizes the target resources in AWS.

How would you discover a mixed estate of VMware VMs and physical servers?
?
Use the agentless collector for the VMware VMs and the agent-based Discovery Agent on the physical servers.

What is AWS Migration Hub?
?
The central place for planning, tracking, and managing application migrations to AWS.

What do Migration Hub journey templates provide?
?
Step-by-step guidance on recommended tasks for each migration phase, plus runbooks to execute them.

What does the Migration Hub Orchestrator do?
?
Speeds up migrations with predefined workflows for common strategies, such as rehosting applications on EC2.

What does the Migration Hub dashboard show?
?
Real-time status and metrics for rehost and replatform migrations.

What are the three main use cases of AWS Migration Hub?
?
Discovering which applications can be migrated (with Application Discovery Service), executing migrations, and modernizing applications after migration.

How many vCPUs does a server with 16 vCPUs at 20% peak CPU need, if you target 60% peak after migration?
?
About 16 × 0.20 / 0.60 ≈ 5.3, so the next instance size up (8 vCPUs).
