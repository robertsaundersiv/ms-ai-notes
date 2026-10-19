---
title: "Re-platforming to Serverless with AWS Lambda – Flashcards"
course: AWS Cloud Architect – Designing AWS Architecture for Workloads
type: flashcards
source: "[[Re-platforming to Serverless with AWS Lambda]]"
created: 2026-10-18
---

#flashcards/aws/workloads/lambda

Flashcards for [[Re-platforming to Serverless with AWS Lambda]].

What does the Doctor Scheduling System move to in the serverless pattern?
?
API Gateway for networking, AWS Lambda for the application, and DynamoDB for storage.

Why does Lambda suit the Doctor Scheduling System?
?
Its workload is small but unpredictable and highly concurrent. Lambda scales with requests and charges only when it runs.

Why does DynamoDB suit the Doctor Scheduling System?
?
A serverless key-value database scales automatically with unpredictable load and gives consistently low latency.

What is AWS Lambda?
?
A serverless compute service that runs your code in response to events, with no servers to provision or manage.

What is an event-driven function?
?
Code that runs only when an event arrives and then exits, replacing long-running processes that loop and poll.

What three changes turn a directory-polling script into a Lambda function?
?
Remove the continuous loop and make it an event handler; get the bucket and object from the S3 event instead of the file system; publish the notification through the AWS SDK.

Where does a Lambda function get the details of the S3 object that triggered it?
?
From the event payload, which lists records containing the bucket name, object key, and event type.

Why should S3 object keys from events be decoded?
?
They arrive URL-encoded (spaces become plus signs), so keys with special characters would otherwise be wrong.

What is Amazon SNS?
?
A pub/sub notification service: publishers send to a topic, and every subscription (email, SMS, SQS, Lambda, HTTP) receives the message.

Why use a standard SNS topic rather than FIFO in this lab?
?
The lab doesn't need strict ordering or deduplication, and email subscriptions need a standard topic.

What must happen before an SNS email subscription delivers messages?
?
The recipient must confirm the subscription from the confirmation email.

What is boto3?
?
The official AWS SDK for Python, used to create, configure, and call AWS services programmatically.

What is a Lambda execution role?
?
The IAM role a function assumes when it runs. Its policies define which AWS APIs the code may call.

Why does the exercise role pair S3 read-only with SNS full access?
?
The function only reads S3 event information and must publish to SNS. SNS read-only wouldn't allow publishing.

What is the true least-privilege permission for the S3-delete notifier?
?
Publish to the one SNS topic, plus basic logging. S3 permissions aren't needed because the event already carries the bucket and key.

Why store the SNS topic ARN in an environment variable?
?
It separates configuration from code, so the same code works with any topic or account without edits.

What is recursive invocation?
?
A function triggered by writes to a bucket that writes back to the same bucket, re-invoking itself in an endless, billed loop.

How does the exercise avoid recursive invocation?
?
It triggers only on object delete events (create events unticked), and the function never writes to the bucket.

What is the difference between Deploy and Test in the Lambda console?
?
Deploy publishes the edited code. Test invokes the function with a simulated event before any real change happens.

Why test a Lambda function with a template event before real uploads or deletes?
?
It checks the code path and permissions in isolation, quickly and repeatably, without changing real data.

What delivery guarantee do S3 event notifications have, and what does it imply?
?
At-least-once, with no ordering guarantee. Handlers should be idempotent and tolerate duplicates.

What is a cold start?
?
The extra latency when Lambda must initialize a new execution environment before running the handler. It matters for latency-sensitive spikes.

Why create SDK clients outside the Lambda handler?
?
They're initialized once per execution environment and reused across invocations, which cuts per-call latency.

What would you add to keep a booking spike on Lambda from overwhelming DynamoDB?
?
Throttling at API Gateway and reserved concurrency on the function, to bound how much load reaches the database.
