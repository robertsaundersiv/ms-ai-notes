---
title: "AWS Migration Services Overview – Flashcards"
course: AWS Cloud Architect – Designing AWS Architecture for Workloads
type: flashcards
source: "[[AWS Migration Services Overview]]"
created: 2026-10-19
---

#flashcards/aws/workloads/migration-services

Flashcards for [[AWS Migration Services Overview]].

What are the three groups of AWS migration-related services?
?
Assessment services, migration services, and data transfer services.

Which AWS service is the main assessment tool before a migration?
?
AWS Application Discovery Service, which analyzes applications and their dependencies.

Which three AWS services make up the core migration services?
?
AWS Migration Hub (tracking), AWS Database Migration Service (databases), and AWS Application Migration Service (applications).

Which four AWS services handle data transfer?
?
AWS DataSync, AWS Transfer Family, the AWS Snow Family, and AWS Direct Connect.

How do migration services differ from data transfer services?
?
Migration services move workloads (databases, servers, applications) with built-in validation. Data transfer services move data of varying sizes and types.

Which AWS service migrates applications without re-architecting them?
?
AWS Application Migration Service (MGN).

Which AWS service provides a single location to track migration progress?
?
AWS Migration Hub.

Which AWS service moves databases to and from AWS with minimal downtime?
?
AWS Database Migration Service (DMS).

What approach did Emirates use to reduce risk when migrating to AWS?
?
A region-by-region approach that started with low-risk services to build confidence before moving higher-priority systems.

What were the main outcomes of the Emirates migration to AWS?
?
Zero unplanned downtime, improved transparency through monitoring, better decision-making from logging and monitoring, and improved website performance and reliability.

Which AWS services were instrumental in the Emirates migration?
?
AWS DMS, to migrate hundreds of on-prem SQL databases, and AWS DataSync, to transfer large files securely and efficiently.

Why migrate low-risk workloads first?
?
To prove the tooling, runbooks, and team processes before moving critical systems, so problems surface where their impact is small.
