---
title: "Exercise 3 – VPC Flow Logs – How To"
aliases:
  - Exercise 3 How To
course: AWS Cloud Architect – Designing AWS Architecture for Organizations
lessons:
  - L1-A12 Exercise 3
type: how-to
created: 2026-10-17
related:
  - "[[Monitoring and Logging Network Traffic]]"
  - "[[Exercise 2 - Peering and Hybrid DNS - How To]]"
tags:
  - aws/networking/monitoring
  - aws/cloudwatch
  - aws/iam
  - aws/lab
  - how-to
---

# Exercise 3 – VPC Flow Logs – How To

> [!abstract] Goal
> Capture **all traffic** in `TradingSystemVPC` with **VPC Flow Logs**, delivered to a CloudWatch Logs log group. This takes four pieces, built in this order:
> 1. a **log group** (where the logs go)
> 2. an **IAM policy** (what may be written)
> 3. an **IAM role** that the Flow Logs service may assume (who writes)
> 4. the **flow log** itself
>
> It takes about 15 minutes.

**Concepts:** [[Monitoring and Logging Network Traffic]] · **Previous lab:** [[Exercise 2 - Peering and Hybrid DNS - How To]]

> [!warning] Built from the demo video
> I haven't seen the official Exercise 3 sheet. Names come from the instructor's demo (video L1-A12). **Where the sheet differs, use the sheet.**

---

## 0. Before You Start

- [ ] `TradingSystemVPC` exists ([[Exercise 1 - Build the Network - How To|Exercise 1]])
- [ ] Region = **us-west-1** for CloudWatch and VPC. **IAM is global**, so its Region selector doesn't matter.

| Piece | Name |
|---|---|
| Log group | `/aws/tradingsystem/vpcflowlogs` |
| IAM policy | `TradingSystemLogGroupPolicy` |
| IAM role | `TradingSystemLogGroupRole` (the demo's caption is garbled; check the sheet) |
| Flow log | `TradingSystemVPC flow log` |

---

## 1. Create the Log Group

1. **CloudWatch console → Logs → Log groups → Create log group**.
2. **Log group name:** `/aws/tradingsystem/vpcflowlogs`
3. **Retention setting:** **1 month (30 days)**. Logs expire after that.
4. **Log class:** **Standard**
5. **Create**.

---

## 2. Create the IAM Policy

1. **IAM console → Policies → Create policy**.
2. Use the **Visual** editor:
   - **Service:** *CloudWatch Logs*
   - **Actions allowed:**
     - *Write*: `CreateLogGroup`, `CreateLogStream`, `PutLogEvents`
     - *List*: `DescribeLogGroups`, `DescribeLogStreams`
   - **Resources:** **All** (as in the demo)

   Or switch to **JSON** and paste:

   ```json
   {
     "Version": "2012-10-17",
     "Statement": [{
       "Effect": "Allow",
       "Action": [
         "logs:CreateLogGroup",
         "logs:CreateLogStream",
         "logs:PutLogEvents",
         "logs:DescribeLogGroups",
         "logs:DescribeLogStreams"
       ],
       "Resource": "*"
     }]
   }
   ```

3. **Next** → **Policy name:** `TradingSystemLogGroupPolicy` → **Create policy**.

---

## 3. Create the IAM Role

1. **IAM → Roles → Create role**.
2. **Trusted entity type:** **Custom trust policy**. Replace the editor contents with:

   ```json
   {
     "Version": "2012-10-17",
     "Statement": [{
       "Effect": "Allow",
       "Principal": { "Service": "vpc-flow-logs.amazonaws.com" },
       "Action": "sts:AssumeRole"
     }]
   }
   ```

3. **Next** → search and tick **`TradingSystemLogGroupPolicy`** → **Next**.
4. **Role name:** `TradingSystemLogGroupRole` → **Create role**.

> [!tip] Two halves
> The **trust policy** (step 2) says *who* may use the role: the Flow Logs service. The **permissions policy** (section 2) says *what* it may do. If either is wrong, delivery fails ([[Monitoring and Logging Network Traffic#^role-two-halves]]).

---

## 4. Create the Flow Log

1. **VPC console → Your VPCs** → select **TradingSystemVPC** → **Flow logs** tab → **Create flow log**.
2. **Name:** `TradingSystemVPC flow log`
3. **Filter:** **All** (accepted and rejected traffic)
4. **Maximum aggregation interval:** **1 minute**
5. **Destination:** **Send to CloudWatch Logs**
6. **Destination log group:** `/aws/tradingsystem/vpcflowlogs`
7. **Service access / IAM role:** *Use an existing service role* → **`TradingSystemLogGroupRole`**
8. **Log record format:** *AWS default format*
9. **Create flow log**.

> [!success] Check
> The VPC's **Flow logs** tab shows the flow log with status **Active**, destination type *cloud-watch-logs*, and your log group.

---

## 5. Why the Log Group May Stay Empty

Flow logs record traffic on **network interfaces**. After Exercise 2's cleanup, `TradingSystemVPC` may have **no ENIs at all**: no instances, no Resolver endpoints, and gateway endpoints don't use ENIs. With no ENIs, there's nothing to log. That's expected, not a failure.

**Optional, to see real records** (small cost; terminate promptly):

1. **EC2 → Launch instance** → a small instance type in `Private Subnet 1` → no key pair needed → launch.
2. Wait 5–10 minutes, then open **CloudWatch → Log groups → /aws/tradingsystem/vpcflowlogs**. You should see a **log stream named after the instance's ENI** (`eni-…-all`).
3. **Logs Insights**, with the log group selected:

   ```sql
   fields @timestamp, srcAddr, dstAddr, dstPort, action
   | sort @timestamp desc
   | limit 20
   ```

4. **Terminate the instance** when you're done.

> [!note] What you won't see
> Queries to the VPC DNS server (`172.19.0.2`), DHCP, and instance-metadata traffic are **never** in flow logs ([[Monitoring and Logging Network Traffic#3. What Flow Logs Do Not Capture]]).

---

## 6. Troubleshooting

| Problem | Likely cause | Fix |
|---|---|---|
| Role isn't in the flow-log role dropdown | Trust policy principal is wrong | Edit the role's **Trust relationships** to `vpc-flow-logs.amazonaws.com` |
| Flow log status shows an error or *access error* | Permissions policy not attached, or missing actions | Attach `TradingSystemLogGroupPolicy`, and confirm the 5 actions |
| Log group not in the dropdown | Created in another Region | Recreate it in **us-west-1** |
| No log streams after 10+ minutes | No ENIs in the VPC | See section 5 |
| Typed the log group name with a typo | It doesn't match the spec | Delete and recreate. Names can't be renamed. |

---

## 7. Cleanup

The flow log, log group, policy, and role are **not billed by the hour**. Ingestion and storage cost a little per GB, and with an idle VPC that's about zero. Keep them unless the course says to remove them.

When tearing down the whole lesson:

1. Delete the **flow log** (VPC → Flow logs tab → Actions → Delete).
2. Delete the **log group**.
3. Delete the **role**, then the **policy** (IAM).
4. Terminate any test instance.
5. Then follow [[Exercise 1 - Build the Network - How To#10. Cleanup|Exercise 1's cleanup]] for the VPC itself.

---

## 8. CLI Equivalent

*Optional.* This does the same build from the AWS CLI. Save the two JSON documents above as `policy.json` and `trust.json` first.

```bash
aws logs create-log-group --region us-west-1 --log-group-name /aws/tradingsystem/vpcflowlogs
aws logs put-retention-policy --region us-west-1 --log-group-name /aws/tradingsystem/vpcflowlogs --retention-in-days 30
aws iam create-policy --policy-name TradingSystemLogGroupPolicy --policy-document file://policy.json
aws iam create-role --role-name TradingSystemLogGroupRole --assume-role-policy-document file://trust.json
aws iam attach-role-policy --role-name TradingSystemLogGroupRole \
  --policy-arn arn:aws:iam::ACCOUNT_ID:policy/TradingSystemLogGroupPolicy
aws ec2 create-flow-logs --region us-west-1 --resource-type VPC --resource-ids vpc-EXAMPLE \
  --traffic-type ALL --max-aggregation-interval 60 \
  --log-destination-type cloud-watch-logs --log-group-name /aws/tradingsystem/vpcflowlogs \
  --deliver-logs-permission-arn arn:aws:iam::ACCOUNT_ID:role/TradingSystemLogGroupRole \
  --tag-specifications 'ResourceType=vpc-flow-log,Tags=[{Key=Name,Value=TradingSystemVPC flow log}]'
```
