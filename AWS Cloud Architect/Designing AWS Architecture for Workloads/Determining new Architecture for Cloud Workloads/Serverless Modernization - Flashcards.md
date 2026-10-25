---
title: "Serverless Modernization – Flashcards"
course: AWS Cloud Architect – Designing AWS Architecture for Workloads
type: flashcards
source: "[[Serverless Modernization]]"
created: 2026-10-19
---

#flashcards/aws/workloads/serverless-modernization

Flashcards for [[Serverless Modernization]].

What are the three techniques for improving application architecture covered in the lesson?
?
Serverless, application orchestration, and container orchestration.

What is a serverless architecture?
?
An approach where the developer only worries about the application, while the provider handles servers, scaling, and capacity.

What are the main benefits of serverless architecture according to the lecture?
?
Automatic scaling with load (no overprovisioning, capacity at peak), paying only for what you use, and event-driven workflows without always-on servers.

What problem does an API served directly on EC2 usually have, and what replaces it?
?
It needs custom auto scaling and API security configuration. Amazon API Gateway replaces it.

What is Amazon API Gateway?
?
A fully managed service for creating, publishing, maintaining, monitoring, and securing APIs at any scale.

Which serverless service replaces short-lived functions running on EC2?
?
AWS Lambda, which runs code in response to events and manages the underlying compute.

Which serverless option suits relational databases on RDS with changing capacity needs?
?
Amazon Aurora Serverless, which automatically starts up, shuts down, and scales capacity with demand.

What is the maximum runtime of a single AWS Lambda invocation?
?
15 minutes.

When can serverless compute cost more than an EC2 instance?
?
For steady, high-throughput workloads that keep functions busy continuously, where a right-sized instance is cheaper.

How is AWS Lambda compute priced?
?
By GB-seconds (memory multiplied by duration) plus a charge per request.
