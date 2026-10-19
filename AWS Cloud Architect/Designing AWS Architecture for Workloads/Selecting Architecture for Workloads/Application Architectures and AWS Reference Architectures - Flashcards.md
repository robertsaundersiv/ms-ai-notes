---
title: "Application Architectures and AWS Reference Architectures – Flashcards"
course: AWS Cloud Architect – Designing AWS Architecture for Workloads
type: flashcards
source: "[[Application Architectures and AWS Reference Architectures]]"
created: 2026-10-18
---

#flashcards/aws/workloads/reference-architectures

Flashcards for [[Application Architectures and AWS Reference Architectures]].

Why must you identify an application's current architecture before migrating?
?
It decides both the best migration strategy and the reference architecture to target.

What is a monolithic architecture?
?
The traditional model where one tightly coupled code base performs multiple business functions, and all components scale together.

Why does a monolith tend to overuse hardware?
?
All components scale together, so to scale one busy function you must scale the whole application.

How are monoliths usually migrated?
?
Rehosted when time is limited, or refactored (typically into microservices) to meet business requirements.

What is a microservices architecture?
?
Software built from small, independent services in separate code bases. Each performs a single function and talks to others through a well-defined interface.

What is a container?
?
A lightweight, portable, self-sufficient unit that packages an application with its dependencies and runs on any system with a container runtime.

What lets microservices scale independently?
?
Containers plus separation of concerns: each service can be scaled on its own current load and predicted demand.

What are data processing services?
?
ETL jobs and functions that process and analyze datasets too large or complex for traditional software, using frameworks like Spark or Hadoop across a cluster.

How do monolith/microservices differ from data processing services as categories?
?
Monolith and microservices describe how an application is built and deployed. Data processing describes the kind of work it does.

What is the rehost reference stack for a monolith with a SQL Server database?
?
A load balancer, an EC2 instance, EBS for local storage, and RDS for SQL Server.

Why add a load balancer when rehosting a monolith that had none on-prem?
?
It's a small "tinker" that prepares for later scaling with Auto Scaling groups and Multi-AZ deployments.

What is the replatform stack for a Docker Compose microservices app with MongoDB?
?
A load balancer, ECS with the Fargate launch type, ECR for images, EFS for shared storage, and DocumentDB.

Why choose ECS rather than EKS for a containerized app?
?
When the app doesn't already use Kubernetes. EKS is the natural target when Kubernetes is already in use.

Why is Fargate useful when traffic volume is uncertain?
?
It's serverless container compute that scales tasks with traffic, so you don't size or manage servers.

Why is DocumentDB chosen for a MongoDB-based app?
?
It's MongoDB-compatible, so the data layer moves with little change.

What is the "analogous managed service" heuristic for replatforming?
?
Map each on-prem component to a compatible managed twin (Kubernetes → EKS, MongoDB → DocumentDB, Hive Metastore → Glue Data Catalog) to keep code changes small.

When does the serverless reference architecture fit?
?
For a business-critical app with unpredictable, high-volume traffic that would otherwise need peak capacity planning and suffers latency at peak.

What are the three components of the serverless reference architecture?
?
API Gateway (front door), Lambda (compute), and DynamoDB (database).

In the big-data reference architecture, what is the AWS target for on-prem Spark, and for on-prem Hadoop?
?
Spark → AWS Glue. Hadoop → Amazon EMR Serverless.

What replaces HDFS/NAS storage and the Hive Metastore in the big-data reference architecture?
?
Amazon S3 for storage, and the Glue Data Catalog for metadata.

What role does PrivateLink play in the big-data reference architecture?
?
It gives private connectivity between the VPC and AWS managed services, so traffic stays off the public internet.

What is the core economic idea of the big-data reference architecture?
?
Cheap, durable storage holds the data, and serverless compute scales up to run jobs and back down to zero afterwards.

What risk comes with "compatible" managed databases?
?
They aren't always feature-identical to the original engine, so the app must be tested against the target's compatibility list before cut-over.
