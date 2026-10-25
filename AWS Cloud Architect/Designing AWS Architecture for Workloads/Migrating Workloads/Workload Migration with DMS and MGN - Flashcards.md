---
title: "Workload Migration with DMS and MGN – Flashcards"
course: AWS Cloud Architect – Designing AWS Architecture for Workloads
type: flashcards
source: "[[Workload Migration with DMS and MGN]]"
created: 2026-10-19
---

#flashcards/aws/workloads/dms-mgn

Flashcards for [[Workload Migration with DMS and MGN]].

Which AWS service migrates databases, and which migrates applications?
?
AWS Database Migration Service (DMS) migrates databases. AWS Application Migration Service (MGN) migrates applications.

How does AWS DMS achieve zero downtime during migration?
?
The source database stays fully operational while the data is migrated, with ongoing replication keeping the target current until cutover.

What is a homogeneous database migration?
?
A migration between the same database engine, such as on-prem PostgreSQL to PostgreSQL on Amazon RDS.

What is a heterogeneous database migration?
?
A migration between different database engines, such as on-prem PostgreSQL to MySQL on Amazon RDS.

What is needed in addition to DMS for a heterogeneous migration?
?
Schema conversion, such as the AWS Schema Conversion Tool or DMS Schema Conversion, because DMS moves data while engine-specific schema and code must be converted.

What must you set up first before DMS can migrate an on-prem database?
?
Network access from AWS to the on-prem database: a VPN or Direct Connect, plus security groups and network ACLs that allow the traffic.

What is a DMS replication instance?
?
The DMS compute node that performs the migration, sized by data volume and migration complexity.

What are DMS source and target endpoints?
?
Connection definitions for the on-prem source database and the AWS target database, such as Amazon RDS.

What are the steps of a DMS migration, in order?
?
Enable network access, create a replication instance, create source and target endpoints, create a migration task, start and monitor it, validate the data, then cut over.

How can you validate a DMS migration?
?
Run comparison queries or data validation tools, and with ongoing replication, confirm that new source changes appear in the target.

What is AWS Application Migration Service?
?
An automated lift-and-shift (rehost) service that migrates applications to AWS without requiring changes to them.

What was AWS MGN formerly called, and which service did it replace?
?
It was formerly CloudEndure Migration, and it replaced the deprecated AWS Server Migration Service.

What sources can AWS MGN migrate from?
?
Physical servers; on-prem VMs on VMware vSphere, Hyper-V, Oracle VM, or KVM; other clouds such as Azure and GCP; and EC2 instances in other AWS accounts or Regions.

What are the steps of an AWS MGN migration?
?
Configure a staging subnet, install the replication agent on source servers, replicate continuously, launch test instances, cut over traffic, then do any post-launch configuration.

Why does MGN launch test instances before cutover?
?
To verify the migrated application works correctly in AWS before shifting production traffic.

When should you use DMS instead of MGN for a database server?
?
When the target is a managed service such as Amazon RDS, or a different engine. MGN only rehosts the server as-is on EC2.
