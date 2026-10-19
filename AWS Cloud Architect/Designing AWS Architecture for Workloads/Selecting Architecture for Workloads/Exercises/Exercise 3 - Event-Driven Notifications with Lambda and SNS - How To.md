---
title: "Exercise 3 – Event-Driven Notifications with Lambda and SNS – How To"
aliases:
  - C2 L1 Exercise 3 How To
  - S3 delete notification Lambda
course: AWS Cloud Architect – Designing AWS Architecture for Workloads
lessons:
  - L1 E3 Demo Part 01
  - L1 E3 Demo Part 02
  - L1 E3 Solution
type: how-to
created: 2026-10-18
related:
  - "[[Re-platforming to Serverless with AWS Lambda]]"
  - "[[Exercise 2 - Convert a Spark ETL Job to AWS Glue - How To]]"
tags:
  - aws/lambda
  - aws/sns
  - aws/s3/events
  - aws/lab
  - how-to
---

# Exercise 3 – Event-Driven Notifications with Lambda and SNS – How To

> [!abstract] Goal
> Convert an on-prem script that **polls a directory** into a **Lambda function** that fires when a file is **deleted** from an S3 bucket and sends an **email through SNS**.
> 1. IAM execution role (S3 read-only + SNS)
> 2. SNS standard topic + confirmed email subscription
> 3. Lambda function with an S3 **delete** trigger and a topic-ARN environment variable
> 4. Test with a simulated event, then with a real upload-and-delete
>
> It takes about 20–30 minutes.

**Concepts:** [[Re-platforming to Serverless with AWS Lambda]] · **Previous lab:** [[Exercise 2 - Convert a Spark ETL Job to AWS Glue - How To]]
**Source:** built from the **solution video** (L1 E3 Solution), with steps cross-checked against the demo (Parts 1–2). The exercise sheet wasn't provided. **Use the sheet's names and bucket where they differ.** The end of the demo says the exercise uses **SES**, but the solution uses **SNS** with **delete** events. If your sheet says SES, see [[#11. Variant – If the Sheet Says SES]].

> [!note] Works in the Udacity account
> The demo and solution run in the Udacity-provided account, with a pre-made bucket (the solution's was the "Lambda SNS delete test" bucket, with a `data/` folder).
> **Cost:** effectively zero. A handful of Lambda invocations and SNS emails are inside the free tiers.

---

## 0. Before You Start

| Item | Solution value |
|---|---|
| IAM role | `LambdaExecutionExerciseRole` |
| Role policies | **AmazonS3ReadOnlyAccess**, **AmazonSNSFullAccess** |
| SNS topic | `LambdaExerciseTopic`, type **Standard** |
| Subscription | Protocol **Email**, your address |
| Lambda function | `LambdaExercise` |
| Runtime | Solution used Python 3.9. **Pick the latest Python** (3.9 is deprecated) |
| Trigger | S3, your delete-test bucket, **All object delete events** only |
| Environment variable | `SNS_TOPIC_ARN` = the topic's ARN |
| Test event | Template **S3 Delete** |

---

## 1. Create the Lambda Execution Role

1. **IAM → Roles → Create role**.
2. **Trusted entity:** AWS service → **Use case:** **Lambda** → **Next**.
3. Tick **AmazonS3ReadOnlyAccess** and **AmazonSNSFullAccess** → **Next**.
4. **Role name:** `LambdaExecutionExerciseRole` → **Create role**.

✅ **Check:** the role exists; its trust relationship shows `lambda.amazonaws.com`.

---

## 2. Create the SNS Topic

1. **SNS → Topics → Create topic**.
2. **Type:** **Standard** (not FIFO).
3. **Name:** `LambdaExerciseTopic` → keep the defaults → **Create topic**.
4. On the topic page, **copy the ARN** (you'll need it in step 5).

✅ **Check:** the topic page shows the type *Standard* and an ARN like `arn:aws:sns:<region>:<account>:LambdaExerciseTopic`.

---

## 3. Subscribe Your Email

1. On the topic → **Create subscription**.
2. **Protocol:** **Email** → **Endpoint:** your email → **Create subscription**.
3. In your inbox, open "AWS Notification – Subscription Confirmation" → **Confirm subscription**.

✅ **Check:** SNS → **Subscriptions** shows the status **Confirmed** (not *Pending confirmation*).

---

## 4. Create the Lambda Function

1. **Lambda → Functions → Create function → Author from scratch**.
2. **Name:** `LambdaExercise` · **Runtime:** latest Python.
3. **Permissions → Change default execution role → Use an existing role →** `LambdaExecutionExerciseRole`.
4. **Create function**.

✅ **Check:** the function page opens with a code editor and a function overview diagram.

---

## 5. Add the S3 Delete Trigger

1. **Function overview → Add trigger → S3**.
2. **Bucket:** your delete-test bucket.
3. **Event types:** select **All object delete events**. **Untick All object create events** if it's selected.
4. Tick the **recursive invocation** acknowledgement → **Add**.

> [!danger] Why delete-only
> A trigger on *create* events plus a function that writes to the same bucket loops forever, and you pay for each call. Delete-only, with a function that never writes to S3, can't loop.

✅ **Check:** the overview shows **S3** as a trigger. Under **Configuration → Triggers**, the event type is `s3:ObjectRemoved:*`.

---

## 6. Set the Environment Variable

1. **Configuration → Environment variables → Edit → Add environment variable**.
2. **Key:** `SNS_TOPIC_ARN` (copy it from the code to avoid typos). **Value:** the topic ARN from step 2.
3. **Save**.

✅ **Check:** the variable appears with the full ARN.

---

## 7. Add the Code and Deploy

Paste into `lambda_function.py`, replacing the default:

```python
import os
import urllib.parse
import boto3

sns_client = boto3.client("sns")
SNS_TOPIC_ARN = os.environ["SNS_TOPIC_ARN"]

# WATCH_DIRECTORY = "/data/incoming"   # on-prem polling loop removed

def lambda_handler(event, context):
    # 1. Extract the bucket name and object key from the event
    record = event["Records"][0]
    bucket_name = record["s3"]["bucket"]["name"]
    object_key = urllib.parse.unquote_plus(record["s3"]["object"]["key"])

    # 2. Send the SNS notification
    sns_client.publish(
        TopicArn=SNS_TOPIC_ARN,
        Message=f"A file has been deleted from {bucket_name}: {object_key}",
        Subject="File deleted",
    )

    # 3. Close out the function
    return {"statusCode": 200, "body": f"Notification sent for file {object_key}"}
```

Click **Deploy** → "Successfully updated the function".

✅ **Check:** the editor no longer says *You have undeployed changes*.

---

## 8. Test with a Simulated Event

1. **Test → Create new event**. **Event name:** `DeleteTestEvent`.
2. **Template:** **S3 Delete**.
3. In the JSON, replace the example bucket name (`example-bucket`) and its ARN with **your bucket**. The key can be any test path, e.g. `data/test.txt`.
4. **Save → Test**.

✅ **Check:** the result is **Succeeded** with "Notification sent for file …", and a **File deleted** email arrives.

---

## 9. Test for Real

1. **S3 →** your bucket → `data/` → **Upload** a small test file. No email should come (create events aren't subscribed).
2. Select the file → **Delete** → type `permanently delete` (or as prompted) → **Delete objects**.
3. Wait for the email. It can take a minute or more.

✅ **Check:** a second **File deleted** email names the real object key.

---

## 10. Verify, Troubleshoot, Clean Up

### Verify
- [ ] Subscription status **Confirmed**.
- [ ] Trigger is **delete events only**.
- [ ] Simulated test succeeded and sent an email.
- [ ] A real delete sent an email; a real upload didn't.
- [ ] **Monitor → View CloudWatch logs** shows one invocation per delete.

### Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Test succeeds, no email | Subscription still pending | Confirm it from the inbox |
| `KeyError: 'SNS_TOPIC_ARN'` | Env var missing or misnamed | Match the code's name exactly |
| `AuthorizationError` on publish | Role lacks SNS publish | Attach SNS full access (or `sns:Publish` on the topic) |
| Old behavior after editing | Code not deployed | **Deploy** |
| Upload triggers an email | Create events still selected | Edit the trigger to delete events only |
| Email names `example-bucket` | Test event JSON not edited | Put your bucket in the test event |
| Key looks like `my+file.txt` | URL-encoded key | `unquote_plus` (already in the code) |

### Cleanup
1. **Lambda →** delete `LambdaExercise` (this also removes its trigger).
2. **SNS →** delete the subscription, then `LambdaExerciseTopic`.
3. **IAM →** delete `LambdaExecutionExerciseRole`.
4. **CloudWatch → Log groups →** delete `/aws/lambda/LambdaExercise`.
5. Leave the course-provided bucket alone.

---

## 11. Variant – If the Sheet Says SES

If the sheet wants email sent **directly via SES** instead of SNS:

- Verify your sender (and, in the SES sandbox, recipient) address under **SES → Verified identities**.
- The execution role needs `ses:SendEmail` instead of SNS publish.
- Replace the publish call with an SES client `send_email` call: source = the verified address, destination = your address, with subject and body.
- No topic, subscription, or topic-ARN variable is needed. Store the email addresses in environment variables instead.

---

## 12. Optional – CLI Equivalent (SNS version)

```bash
aws sns create-topic --name LambdaExerciseTopic
aws sns subscribe --topic-arn <topic-arn> --protocol email --notification-endpoint <you@example.com>

zip function.zip lambda_function.py
aws lambda create-function --function-name LambdaExercise \
  --runtime python3.12 --handler lambda_function.lambda_handler \
  --role <role-arn> --zip-file fileb://function.zip \
  --environment "Variables={SNS_TOPIC_ARN=<topic-arn>}"

aws lambda add-permission --function-name LambdaExercise \
  --statement-id s3invoke --action lambda:InvokeFunction \
  --principal s3.amazonaws.com --source-arn arn:aws:s3:::<bucket>

aws s3api put-bucket-notification-configuration --bucket <bucket> \
  --notification-configuration '{"LambdaFunctionConfigurations":[{"LambdaFunctionArn":"<function-arn>","Events":["s3:ObjectRemoved:*"]}]}'
```

The console's **Add trigger** does the `add-permission` and notification steps for you.
