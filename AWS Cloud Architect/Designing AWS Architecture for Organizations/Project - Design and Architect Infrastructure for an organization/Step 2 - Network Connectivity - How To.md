---
title: "Step 2 – Network Connectivity – How To"
aliases:
  - Excipient VPC Peering How To
course: AWS Cloud Architect – Designing AWS Architecture for Organizations
type: how-to
created: 2026-10-17
related:
  - "[[Project Overview]]"
  - "[[Step 2 - Connectivity Report]]"
  - "[[Advanced VPC Connectivity]]"
  - "[[Monitoring and Logging Network Traffic]]"
tags:
  - aws/project
  - aws/networking/peering
  - aws/lab
  - how-to
---

# Step 2 – Network Connectivity – How To

> [!abstract] Goal
> In the **Cloud Lab**, peer two VPCs across Regions, open routes and firewalls, prove traffic flows with `ping` and `curl`, and capture **VPC Flow Logs** as evidence.
>
> | Scenario role | Region | VPC CIDR | Name prefix |
> |---|---|---|---|
> | **Account A**: company database (private VPC) | **us-east-1** | `10.0.0.0/16` | `et-db` |
> | **Account B**: analytics application | **us-west-2** | `192.168.0.0/16` | `et-analytics` |
>
> It takes about 60–90 minutes. Cost is **well under \$0.50** if you clean up the same day.

**Project:** [[Project Overview]] · **Record results in:** [[Step 2 - Connectivity Report]]
**Concepts:** [[Building a VPC]] · [[Advanced VPC Connectivity#4. VPC Peering]] · [[Secure and Private Connectivity]] · [[Monitoring and Logging Network Traffic]]

> [!important] Separate Regions, not separate accounts
> The Cloud Lab is **one account**, and the rubric accepts "separate accounts **or Regions**". So "Account A" and "Account B" are simulated by two Regions. Say so in the report.

> [!danger] Cloud Lab budget rules
> - **\$25 for the whole course.** Hitting it ends the session and loses your work.
> - **Never create a NAT gateway.** "VPC and more" offers one, so choose **None**.
> - Launch **exactly two** small instances (concurrency limits can deactivate the account).
> - **No personal info** in names or tags. Use names like `et-db-instance`.
> - Do [[#9. Cleanup – Do This the Same Day]] when you're finished.

---

## 0. Before You Start

- [ ] Cloud Lab open: Udacity **Cloud Resources → Open Cloud Console**. Log out of any personal AWS session first.
- [ ] A screenshot tool ready. You'll capture about 8 screenshots (listed in [[Step 2 - Connectivity Report#4. Screenshot Checklist]]).
- [ ] Open [[Step 2 - Connectivity Report]] next to the console, to paste IDs as you go.

**Estimated cost** (illustrative on-demand prices; check current pricing):

| Item | Rate | 2 hours |
|---|---|---|
| 2 × t3.micro | about \$0.0104/h each | about \$0.04 |
| 2 × public IPv4 | about \$0.005/h each | about \$0.02 |
| Cross-Region transfer (pings and curl, under 1 MB) | about \$0.02/GB | about \$0.00 |
| Flow logs to CloudWatch | about \$0.50/GB ingested | about \$0.00 |
| **Total** | | **about \$0.06** |

---

## 1. Create VPC A in us-east-1

1. Region selector → **US East (N. Virginia) us-east-1** → **VPC** console → **Create VPC**.
2. **Resources to create:** **VPC and more**
3. **Name tag auto-generation:** `et-db`
4. **IPv4 CIDR:** `10.0.0.0/16` · **IPv6:** none · **Tenancy:** default
5. **Number of AZs:** **1** · **Public subnets:** **1** · **Private subnets:** **0**
6. **NAT gateways:** **None**. ⚠️ This is the costly option, so double-check it.
7. **VPC endpoints:** **None**
8. **DNS options:** leave both enabled
9. **Create VPC** → wait for the success page → **View VPC**.

> [!success] Record
> **VPC ID**, **public subnet ID and CIDR** (the wizard shows it, e.g. `10.0.0.0/20`), and **route table ID** (`et-db-rtb-public`) → report section 1.

> [!note] Why a public subnet for a "database" VPC
> It's only so you can log in to the **test** instance with EC2 Instance Connect. In the real design the database sits in a private subnet. Mention this in the report.

## 2. Create VPC B in us-west-2

Repeat section 1 in **US West (Oregon) us-west-2**, with name prefix `et-analytics` and IPv4 CIDR `192.168.0.0/16`. Same choices: 1 AZ, 1 public subnet, **no NAT**, no endpoints.

> [!success] Record
> The VPC B **VPC ID**, **subnet ID and CIDR**, and **route table ID**.

---

## 3. Create the Peering Connection (us-east-1 → us-west-2)

1. Copy **VPC B's VPC ID** (us-west-2).
2. Switch to **us-east-1** → **VPC → Peering connections → Create peering connection**.
3. **Name:** `et-db-to-analytics-pcx`
4. **VPC ID (Requester):** the `et-db` VPC
5. **Select another VPC to peer with:** **Account:** *My account* · **Region:** *Another Region* → **us-west-2** · **VPC ID (Accepter):** paste VPC B's ID
6. **Create peering connection**. Status: **Pending acceptance**.
7. Switch to **us-west-2** → **Peering connections** → select the pending connection → **Actions → Accept request** → **Accept request**.
8. Status becomes **Active** in both Regions.

> [!success] Record and screenshot
> The **Peering connection ID** (`pcx-…`). Take a screenshot of the **Active** status (**screenshot 1**).

> [!note] Why the CIDRs had to differ
> `10.0.0.0/16` and `192.168.0.0/16` don't overlap. Overlapping VPCs **can't** be peered ([[Advanced VPC Connectivity#^peering-rules]]).

---

## 4. Update Route Tables (Both Sides)

| Region | Route table | Add destination | Target |
|---|---|---|---|
| us-east-1 | `et-db-rtb-public` | `192.168.0.0/16` | **Peering Connection** → `pcx-…` |
| us-west-2 | `et-analytics-rtb-public` | `10.0.0.0/16` | **Peering Connection** → `pcx-…` |

For each: **Route tables** → select the table → **Routes → Edit routes → Add route** → set destination and target → **Save changes**.

> [!warning] Both sides, or replies get lost
> A route on one side only lets packets leave. The reply has no way back ([[Advanced VPC Connectivity#6. Lab Walkthrough – Exercise 2 Peering]]).

> [!success] Screenshot
> Both route tables' **Routes** tabs showing the `pcx-…` route (**screenshots 2 and 3**).

---

## 5. Security Groups

Create one SG in each Region (**EC2 → Security Groups → Create security group**, in the matching VPC):

| Region | SG name | Inbound rules |
|---|---|---|
| us-east-1 (VPC A) | `et-db-test-sg` | **All ICMP – IPv4** from `192.168.0.0/16` · **Custom TCP 8080** from `192.168.0.0/16` · **SSH 22** from the **EC2 Instance Connect** prefix list `com.amazonaws.us-east-1.ec2-instance-connect` |
| us-west-2 (VPC B) | `et-analytics-test-sg` | **All ICMP – IPv4** from `10.0.0.0/16` · **Custom TCP 8080** from `10.0.0.0/16` · **SSH 22** from prefix list `com.amazonaws.us-west-2.ec2-instance-connect` |

Leave outbound as the default (all traffic).

> [!tip] Why CIDRs, not SG references
> Security group rules can reference the *peer VPC's* security group only for **same-Region** peering. Across Regions, use the peer **CIDR**. (*Beyond the lecture.*)

> [!warning] "My IP" does NOT work for browser-based Instance Connect
> When you click **Connect → EC2 Instance Connect** in the console, the SSH session comes from **AWS's Instance Connect service IPs in that Region**, not from your computer. The SSH source must be the Region's prefix list (`com.amazonaws.<region>.ec2-instance-connect`, e.g. `com.amazonaws.us-west-1.ec2-instance-connect` in us-west-1). If you can't find the prefix list, temporarily allow **SSH 22 from `0.0.0.0/0`** for the test, then delete the rule during cleanup. "My IP" only works if you SSH from your own terminal with a key pair.

---

## 6. Network ACLs (Explicit Rules for the Rubric)

The **default NACL already allows all traffic** (rule 100). The rubric asks you to **update** NACLs, so add explicit, documented allow rules for the peer range. They're evaluated before rule 100 ([[Secure and Private Connectivity#2. Security Groups vs. Network ACLs]]).

For each VPC: **VPC → Network ACLs** → select the NACL associated with your subnet → **Inbound rules → Edit**, then **Outbound rules → Edit**.

| VPC | Direction | Rule # | Type | Port | Source / destination | Action |
|---|---|---|---|---|---|---|
| A (us-east-1) | Inbound | 90 | All ICMP – IPv4 | — | `192.168.0.0/16` | Allow |
| A | Inbound | 91 | Custom TCP | 1024–65535 | `192.168.0.0/16` | Allow (replies to curl from A) |
| A | Outbound | 90 | All ICMP – IPv4 | — | `192.168.0.0/16` | Allow |
| A | Outbound | 91 | Custom TCP | 8080 | `192.168.0.0/16` | Allow |
| B (us-west-2) | Inbound | 90 | All ICMP – IPv4 | — | `10.0.0.0/16` | Allow |
| B | Inbound | 91 | Custom TCP | 8080 | `10.0.0.0/16` | Allow |
| B | Outbound | 90 | All ICMP – IPv4 | — | `10.0.0.0/16` | Allow |
| B | Outbound | 91 | Custom TCP | 1024–65535 | `10.0.0.0/16` | Allow (replies to A's ephemeral ports) |

> [!note] Why the ephemeral-port rules
> NACLs are **stateless**, so replies need their own rule ([[Secure and Private Connectivity#^ephemeral-ports]]). The curl flows A → B on 8080, and B's reply goes back to A's ephemeral port.

> [!success] Screenshot
> One NACL's inbound and outbound rules (**screenshot 4**).

---

## 7. Launch the Test Instances

In each Region: **EC2 → Launch instance**.

| Setting | VPC A (us-east-1) | VPC B (us-west-2) |
|---|---|---|
| Name | `et-db-instance` | `et-analytics-instance` |
| AMI | **Amazon Linux 2023** | **Amazon Linux 2023** |
| Instance type | **t3.micro** (or t2.micro) | **t3.micro** (or t2.micro) |
| Key pair | *Proceed without a key pair* (Instance Connect handles login) | same |
| Network | VPC `et-db`, its public subnet, **Auto-assign public IP: Enable** | VPC `et-analytics`, its public subnet, auto-assign public IP |
| Security group | `et-db-test-sg` | `et-analytics-test-sg` |
| Storage | Default (8 GB gp3) | Default |

Launch → wait for **Running** and **2/2 status checks**.

> [!success] Record
> Each instance's **Instance ID** and **Private IPv4**.

---

## 8. Enable Flow Logs, Then Test Traffic

### 8a. Flow logs (both VPCs)

Flow logs record traffic metadata for each VPC ([[Monitoring and Logging Network Traffic]]). You need **one flow log per VPC**, so two in total. Pick **Option 1 (CloudWatch Logs)** unless IAM role creation is blocked in the Cloud Lab. Then use **Option 2 (S3)**.

> [!note] Your Regions
> Account A = **us-east-1** (`vpc-03181bb3841a34090`). Account B = **us-west-1** (`vpc-04409d739c492c202`).

#### Option 1 – CloudWatch Logs (recommended)

This takes four pieces, in order: **log groups → IAM policy → IAM role → flow logs**. It's the same pattern as [[Exercise 3 - VPC Flow Logs - How To]].

**Step 1 – Create a log group in each Region**
1. Region selector → **us-east-1**.
2. Search **CloudWatch** → left menu **Logs → Log groups** → **Create log group**.
3. **Log group name:** `/et/project/vpcflowlogs`
4. **Retention setting:** **1 day**. That keeps storage cost near zero.
5. **Log class:** Standard → **Create**.
6. Switch the Region to **us-west-1** and repeat with the **same name**. Log groups are Regional, so each VPC writes to the log group in its own Region.

**Step 2 – Create the IAM policy (once; IAM is global)**
1. Search **IAM** → **Policies** → **Create policy** → the **JSON** tab.
2. Replace the editor contents with:

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

3. **Next** → **Policy name:** `et-flowlogs-policy` → **Create policy**.

**Step 3 – Create the IAM role (once)**
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

3. **Next** → search for and tick **`et-flowlogs-policy`** → **Next**.
4. **Role name:** `et-flowlogs-role` → **Create role**.

> [!warning] If IAM says "not authorized"
> The Cloud Lab may block creating roles or policies. Skip to **Option 2 (S3)**, which needs no role.

**Step 4 – Create the flow log on each VPC**
1. Region → **us-east-1** → **VPC** console → **Your VPCs** → tick `vpc-03181bb3841a34090` (`et-db-vpc`).
2. Bottom panel → **Flow logs** tab → **Create flow log**.
3. Fill in the form:

| Field                        | Value                                                 |
| ---------------------------- | ----------------------------------------------------- |
| Name                         | `et-db-flowlog`                                       |
| Filter                       | **All** (accepted and rejected)                       |
| Maximum aggregation interval | **1 minute**                                          |
| Destination                  | **Send to CloudWatch Logs**                           |
| Destination log group        | `/et/project/vpcflowlogs`                             |
| Service access / IAM role    | **Use an existing service role** → `et-flowlogs-role` |
| Log record format            | **AWS default format**                                |

4. **Create flow log**.
5. Region → **us-west-1** → **Your VPCs** → tick `vpc-04409d739c492c202` → **Flow logs** → **Create flow log** with the same settings, named `et-analytics-flowlog`. Use the us-west-1 log group `/et/project/vpcflowlogs` and the same role.

> [!success] Check
> Each VPC's **Flow logs** tab shows **Status: Active**, destination type *cloud-watch-logs*. If it shows an **access error**, the role's trust policy or permissions are wrong. Recheck steps 2–3.

#### Option 2 – S3 (if IAM role creation is blocked)

No IAM role is needed, because S3 delivery uses a bucket policy that AWS adds automatically.

1. Region → **us-east-1** → **S3** → **Create bucket**.
   - **Name:** `et-flowlogs-use1-<random digits>` (bucket names are globally unique; no personal info)
   - **Region:** us-east-1. Leave everything else at the defaults → **Create bucket**.
2. Open the bucket → **Properties** → copy the **Amazon Resource Name (ARN)**, e.g. `arn:aws:s3:::et-flowlogs-use1-48213`.
3. **VPC → Your VPCs** → tick the us-east-1 VPC → **Flow logs** → **Create flow log**:

| Field                        | Value                                   |
| ---------------------------- | --------------------------------------- |
| Name                         | `et-db-flowlog`                         |
| Filter                       | **All**                                 |
| Maximum aggregation interval | **1 minute**                            |
| Destination                  | **Send to an Amazon S3 bucket**         |
| S3 bucket ARN                | the ARN from step 2                     |
| Log record format            | AWS default · **Log file format:** Text |

4. Repeat in **us-west-1** with a bucket named `et-flowlogs-usw1-<random digits>` and flow log `et-analytics-flowlog`.

**Reading S3 flow logs later:** open the bucket → **AWSLogs/** → your account ID → `vpcflowlogs/` → Region → year/month/day → download a `.log.gz` file and open it. The lines have the same fields as in 8c.

> [!note] Do this before testing
> Flow logs only capture traffic **after** they're created, and records arrive in batches. Wait about **2–5 minutes** after testing before you look.

> [!tip] Report evidence
> Paste each flow log's **ID** (`fl-…`) and its destination (log group or bucket) into the Verification section of [[Step 2 - Connectivity Report]].

**Cleanup for 8a** (part of section 9):
- Delete both flow logs (VPC → **Flow logs** tab → select → **Actions → Delete**).
- Delete both log groups, or empty and delete both buckets.
- Delete `et-flowlogs-role`, then `et-flowlogs-policy`.

### 8b. Connect and test

1. **EC2 → et-db-instance → Connect → EC2 Instance Connect → Connect.** A browser terminal opens.
2. Ping VPC B's instance on its **private** IP:
   ```bash
   ping -c 5 <B-private-IP>
   ```
   **Screenshot 5:** 5 packets transmitted, 5 received, 0% loss.
3. In a second tab, connect to **et-analytics-instance** and start a tiny web server:
   ```bash
   python3 -m http.server 8080
   ```
4. Back on **et-db-instance**:
   ```bash
   curl -s -o /dev/null -w "HTTP %{http_code}\n" http://<B-private-IP>:8080/
   ```
   Expect `HTTP 200`. (**Screenshot 6** shows both terminals: the server log line and the 200.)
5. **Reverse direction:** from **et-analytics-instance** (Ctrl+C the server first):
   ```bash
   ping -c 5 <A-private-IP>
   ```
   **Screenshot 7.**

> [!tip] Optional negative test (strong evidence)
> Temporarily delete the `192.168.0.0/16 → pcx` route in us-east-1 and rerun the ping. It now fails, because nothing routes there. Restore the route and the ping works again. This shows the **peering route** is what carries the traffic.

### 8c. Read the flow logs

Wait about 2–5 minutes. Then **CloudWatch → Logs Insights** (us-east-1) → log group `/et/project/vpcflowlogs`:

```sql
fields @timestamp, srcAddr, dstAddr, srcPort, dstPort, protocol, action, bytes
| filter (srcAddr like "10.0." and dstAddr like "192.168.")
      or (srcAddr like "192.168." and dstAddr like "10.0.")
| sort @timestamp desc
| limit 50
```

- `protocol = 1` means **ICMP** (ping). `protocol = 6` with `dstPort = 8080` means **curl**.
- `action = ACCEPT` confirms the SGs and NACLs allowed the traffic.

**Screenshot 8:** the query results showing ACCEPT records in both directions. (With the S3 option: download one `.log.gz` object and screenshot the matching lines.)

---

## 9. Cleanup – Do This the Same Day

In this order, **in both Regions**:

1. **Terminate** `et-db-instance` and `et-analytics-instance` (EC2 → Instance state → Terminate). This also releases the public IPv4 charge.
2. **Delete the flow logs** (VPC → Flow logs tab → Delete).
3. **Delete the log groups** (or empty and delete the S3 buckets).
4. **Delete the peering connection** (either Region → Peering connections → Actions → Delete).
5. **Delete each VPC** (VPC → Your VPCs → Actions → Delete VPC). The console deletes its subnets, route tables, internet gateway, NACL, and security groups with it.
6. **Delete the flow-logs IAM role and policy**, if you created them.
7. **Next day:** check **Cost Explorer** to confirm nothing is still running.

---

## 10. Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Peering stuck in *Pending acceptance* | Not accepted in the **accepter Region** | Switch to us-west-2 and accept |
| `ping` shows 100% loss | Missing route on either side, SG ICMP rule missing, or the **public** IP was pinged | Check both route tables and SGs. Use **private** IPs. |
| `curl` hangs | SG 8080 missing, NACL ephemeral rule missing, or the server isn't running | Check section 5/6 rules. Keep `python3 -m http.server 8080` running. |
| Instance Connect fails ("Error establishing SSH connection") | SSH source is "My IP" or the wrong Region's prefix list; no public IP; NACL rule 100 removed; no `0.0.0.0/0 → igw` route; non-Amazon-Linux AMI; status checks not finished | SSH 22 from **this Region's** `ec2-instance-connect` prefix list (or `0.0.0.0/0` temporarily). Confirm a public IPv4, the IGW route, and NACL rule 100. Use Amazon Linux 2023, user `ec2-user`. Wait for 2/2 checks. |
| No flow log records | Created after the test, or wrong log group or Region | Rerun the pings after a few minutes. Query in the right Region. |
| Flow log status *Access error* | IAM role trust or permissions wrong | Fix the role, or switch to the S3 option |
| "Not authorized" on a Region | Cloud Lab allows only us-east-1/2 and us-west-1/2 | Stay in us-east-1 and us-west-2 |
