---
title: "AWS Data Transfer Services – Flashcards"
course: AWS Cloud Architect – Designing AWS Architecture for Workloads
type: flashcards
source: "[[AWS Data Transfer Services]]"
created: 2026-10-19
---

#flashcards/aws/workloads/data-transfer

Flashcards for [[AWS Data Transfer Services]].

When are data transfer tools a better fit than workload migration services?
?
For edge cases such as transferring entire data centers' worth of data, or dedicated transfers of smaller data volumes.

According to the lecture, which service fits transfers larger than 8 TB, and which fits smaller ones?
?
The AWS Snow Family for more than 8 TB, and AWS DataSync for less than 8 TB.

Why can physically shipping data beat transferring it over the network?
?
For massive datasets, bandwidth limits make online transfer take longer than shipping a device.

How do you decide between online and offline transfer?
?
Compare transfer time (data size divided by usable bandwidth) with the shipping round trip and the deadline.

What is AWS Snowcone?
?
The smallest, rugged Snow Family device, with 8 TB HDD or 14 TB SSD storage, 2 vCPUs, and 4 GB of memory.

What are typical Snowcone use cases?
?
Edge computing where space and power are limited, such as remote field offices or construction sites, and disaster recovery.

What is AWS Snowball Edge?
?
A larger Snow Family device in multiple models for terabyte-to-petabyte transfers, with built-in compute.

What are typical Snowball Edge use cases?
?
Relocating an entire data center, temporary storage in remote locations, industrial IoT, and remote media production.

What sets Snowball Edge apart from a plain storage device?
?
Built-in compute that processes data where it's generated, at the edge or in areas with limited connectivity.

What is AWS DataSync?
?
An online data movement and discovery service with built-in security, automation, and network optimization between on-prem systems and AWS storage.

Which AWS storage services can DataSync transfer to?
?
Amazon S3, Amazon EFS, and Amazon FSx for Windows File Server.

What does DataSync handle automatically?
?
Encryption, data validation, and bandwidth optimization.

What are the steps to use DataSync?
?
Create a task with a source and a target, configure it as a one-time migration or ongoing sync, then run the transfer.

What does AWS Direct Connect provide?
?
A dedicated network connection to AWS with consistent performance and lower data transfer costs, ideal for hybrid architectures that need ongoing sync.

How do you set up AWS Direct Connect?
?
Request a connection in the console with your location and Region, have AWS or a partner establish the physical link, then configure it.

What is AWS Transfer Family?
?
A fully managed service for secure file transfers into and out of AWS storage using protocols such as SFTP and FTPS.

What are the setup steps for AWS Transfer Family?
?
Configure the file transfer protocols you need, then set up user access for uploads and downloads.

Roughly how long does 100 TB take over a 1 Gbps link at 80% utilization?
?
About 11.6 days, which usually favors a Snow device.
