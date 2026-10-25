---
title: "Application and Container Orchestration – Flashcards"
course: AWS Cloud Architect – Designing AWS Architecture for Workloads
type: flashcards
source: "[[Application and Container Orchestration]]"
created: 2026-10-19
---

#flashcards/aws/workloads/orchestration

Flashcards for [[Application and Container Orchestration]].

What is AWS Step Functions?
?
A serverless workflow service for coordinating multiple AWS services and streamlining serverless applications.

What are the main features of AWS Step Functions?
?
A visual workflow, JSON-based state machines, and automated workflows with built-in tracking and error handling.

How does Step Functions solve the lecture's sales-and-finance order-log problem?
?
A state machine runs the sales Lambda on each new S3 order log first, then the finance Lambda that loads the results into RDS.

Why orchestrate a workflow with Step Functions instead of chaining Lambda functions directly?
?
Ordering, retries, error handling, and execution history live in the state machine instead of being hidden in function code.

What does container orchestration automate?
?
Managing, scaling, and deploying containers across a cluster of machines, including replicas, auto scaling, and networking.

Why is running Docker on EC2 with your own registry operationally inefficient?
?
The load balancer, auto scaling groups, Docker daemons, and registry must all be configured and maintained manually.

What is Amazon ECS?
?
A fully managed container orchestration service that runs, stops, and manages Docker containers on a cluster.

What is AWS Fargate?
?
A serverless compute engine for containers that provisions and removes compute automatically, with no infrastructure to manage.

What is Amazon ECR?
?
A fully managed Docker container registry for storing, managing, and deploying container images securely.

What role does Amazon EFS play in a containerized architecture on Fargate?
?
It provides elastic, shared, persistent storage that every task can use.

What does an ECS launch type choose?
?
The compute infrastructure for tasks: EC2 instances you manage, or serverless Fargate.

Do Fargate tasks require Amazon EFS?
?
No. Fargate tasks have built-in ephemeral storage. EFS is needed only for persistent or shared storage.

When would you choose Amazon EKS over Amazon ECS?
?
When you already have Kubernetes workloads and skills, or need Kubernetes portability.
