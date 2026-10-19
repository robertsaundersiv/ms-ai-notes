---
title: "Exercise 2 – Peering and Hybrid DNS – How To"
aliases:
  - Exercise 2 How To
course: AWS Cloud Architect – Designing AWS Architecture for Organizations
lessons:
  - L1-A11 Exercise 2
type: how-to
created: 2026-10-17
related:
  - "[[Advanced VPC Connectivity]]"
  - "[[DNS and Network Resolution]]"
  - "[[Exercise 1 - Build the Network - How To]]"
  - "[[Exercise 3 - VPC Flow Logs - How To]]"
tags:
  - aws/networking/peering
  - aws/route53
  - aws/lab
  - how-to
---

# Exercise 2 – Peering and Hybrid DNS – How To

> [!abstract] Goal
> Extend `TradingSystemVPC` with:
> - **VPC peering**: a cross-account request to an HR VPC (expected to fail), and a working same-account peering to a "Market Prediction VPC"
> - **Hybrid DNS** through **Route 53 Resolver**: outbound and inbound endpoints, a forwarding rule for `steadyvolatility.com`, and query logging to CloudWatch Logs
>
> Then **clean up the Resolver resources right away**, because they're billed by the hour.

**Concepts:** [[Advanced VPC Connectivity]] · [[DNS and Network Resolution]] · **Previous lab:** [[Exercise 1 - Build the Network - How To]] · **Next lab:** [[Exercise 3 - VPC Flow Logs - How To]]

> [!warning] Built from the demo video
> I haven't seen the official Exercise 2 sheet. Names and values below come from the instructor's demo (video L1-A11). **Where the sheet gives different names, IDs, or IPs, use the sheet.** Placeholders are marked `‹from sheet›`.

> [!danger] Cost
> Each Resolver endpoint IP is billed per hour, roughly \$0.125 per IP-hour (check current pricing). This lab creates 4 IPs, about **\$0.50 per hour, or about \$365 a month if forgotten**. Do sections 3–6 in one sitting, verify, then do section 7 immediately.

> [!warning] Route 53 is restricted on Udacity-provided accounts
> The Lesson 3 exercise sheet states that **Route 53 access is restricted** in the course accounts, and that **Organization-related** exercises aren't possible there. Sections 3–7 (Resolver endpoints, rule, query logging) will likely fail in the course account. Do sections 1–2 (peering) there, and study the DNS sections or use your own account. In your own account the Resolver endpoints are **billed hourly**, so follow the cleanup immediately.

---

## 0. Before You Start

- [ ] [[Exercise 1 - Build the Network - How To|Exercise 1]] is complete, and `TradingSystemVPC` still exists
- [ ] Region selector = **us-west-1** (Route 53 *Resolver* is Regional, even though Route 53 hosted zones are global)
- [ ] Note your two AZs (e.g. `us-west-1a` and `us-west-1c`) and which private subnet is in each

---

## 1. Cross-Account Peering Request (Expected to Fail)

This shows the cross-account workflow. The target account and VPC are placeholders, so **an error is the expected outcome**.

1. **VPC console → Peering connections → Create peering connection**.
2. **Name:** `TradingSystemVPC-HRVPC Peering Connection` (or the sheet's name)
3. **VPC ID (Requester):** `TradingSystemVPC`
4. **Select another VPC to peer with:**
   - **Account:** *Another account* → Account ID `111122223333`
   - **Region:** *This Region (us-west-1)*
   - **VPC ID (Accepter):** `‹from sheet›` (the demo used a placeholder ID)
5. **Create peering connection** → expect an **error**, or a request that ends up *failed*. Move on.

> [!note] What would happen with a real account
> The request would sit in **Pending acceptance** until the HR account's owner accepted it in *their* console. Then both sides would add routes ([[Advanced VPC Connectivity#4. VPC Peering]]).

---

## 2. Same-Account Peering to the Market Prediction VPC

### 2a. Get a second VPC

The demo reuses the account's **default VPC** (`172.31.0.0/16`), which doesn't overlap `172.19.0.0/16`.

1. **Your VPCs**: is there a VPC with **Default VPC = Yes**?
   - **No:** **Actions → Create default VPC → Create default VPC**.
2. Select the default VPC → click the pencil in the **Name** column → `Market Prediction VPC` → save.

### 2b. Create and accept the peering

1. **Peering connections → Create peering connection**.
2. **Name:** `TradingSystemVPC-MarketPredictionVPC Peering Connection`
3. **Requester:** `TradingSystemVPC`
4. **Accepter:** *My account*, *This Region*, VPC = `Market Prediction VPC`
5. **Create peering connection**.
6. Select it → **Actions → Accept request** → **Accept request**.

> [!success] Check
> Status = **Active**.

### 2c. Add the routes

1. **Route tables → TradingSystemPrivateRouteTable → Routes → Edit routes → Add route**:
   - Destination `172.31.0.0/16` → Target **Peering Connection** → the `pcx-…` you just created → **Save changes**.
2. **Recommended, though the demo skipped it.** Without it, replies have no path back. Open the **Market Prediction VPC's main route table** → **Edit routes → Add route**:
   - Destination `172.19.0.0/16` → Target **Peering Connection** → same `pcx-…` → **Save changes**.

> [!tip] Why both sides
> A route on one side only lets packets *leave*. Replies need a matching route on the other side ([[Advanced VPC Connectivity#6. Lab Walkthrough – Exercise 2 Peering]]).

---

## 3. Outbound Resolver Endpoint – "Outbound HQ"

1. **Route 53 console → Resolver → Outbound endpoints → Create outbound endpoint**. Confirm the Region is us-west-1.
2. **Endpoint name:** `Outbound HQ`
3. **VPC in the Region:** `TradingSystemVPC`
4. **Security group:** the VPC's **default** security group (as in the demo)
5. **Endpoint type:** **IPv4**
6. **Protocols:** leave the default (**Do53**)
7. **IP addresses**, two of them, in **different AZs**:
   - IP 1: AZ `us-west-1a` → subnet **Private Subnet 1** → *Use an IP address that is selected automatically*
   - IP 2: second AZ → subnet **Private Subnet 2** → automatic
8. **Create outbound endpoint**. Status goes *Creating* → **Operational** after a few minutes.

---

## 4. Inbound Resolver Endpoint – "Inbound from HQ"

1. **Resolver → Inbound endpoints → Create inbound endpoint**.
2. **Endpoint name:** `Inbound from HQ`
3. **VPC:** `TradingSystemVPC` · **Security group:** default · **Endpoint type:** IPv4
4. **IP addresses:** one in each AZ, in the private subnets, **selected automatically**
5. **Create inbound endpoint** and wait for **Operational**.

> [!note] The default security group in real life
> The default SG allows inbound traffic **only from itself**, so HQ's DNS server couldn't actually reach this inbound endpoint. A production endpoint gets its own SG allowing **TCP and UDP 53** from `192.168.48.0/20` ([[DNS and Network Resolution#5. Pitfalls and Failure Modes]]). For the lab, follow the demo.

---

## 5. Outbound Forwarding Rule

1. **Resolver → Rules → Create rule**.
2. **Name:** `outbound resolver rule`
3. **Rule type:** **Forward**
4. **Domain name:** `steadyvolatility.com`
5. **VPCs that use this rule:** `TradingSystemVPC`
6. **Outbound endpoint:** `Outbound HQ`
7. **Target IP addresses:** `172.31.16.2`, port `53` (the demo's value; use the sheet's if different)
8. **Submit** / **Create rule**.

> [!question] About that target IP
> `172.31.16.2` is in the default VPC's range, not HQ's `192.168.48.0/20`. In a real design the target must be the corporate DNS server, reachable over the VPN. Treat this as a lab placeholder ([[DNS and Network Resolution#^dns-needs-route]]).

---

## 6. Query Logging to CloudWatch Logs

1. **Resolver → Query logging → Configure query logging**.
2. **Name:** e.g. `TradingSystemDNSQueryLogs`
3. **Query logs destination:** **CloudWatch Logs log group** → *Create log group* → name `SteadyVolatilityPartners/DNSlogs` (the demo's caption was garbled, so use the sheet's exact name)
4. **VPCs to log queries for:** **Add VPC** → `TradingSystemVPC`
5. **Configure query logging**.

> [!success] Verify before cleanup
> - Outbound and inbound endpoints are **Operational**, each with 2 IPs in 2 AZs
> - The rule shows **Associated VPCs: TradingSystemVPC**
> - The query logging config shows the VPC associated and its destination log group
> - Peering connection to Market Prediction VPC is **Active**, and the route exists in the private table
>
> Screenshot these now if the course wants evidence, because the next step deletes them.

---

## 7. Cleanup – Do This Now

This is the instructor's order. The rule must be disassociated before it can be deleted, and the endpoint can't be deleted while a rule uses it.

1. **Resolver → Rules → outbound resolver rule → Disassociate VPC** → select `TradingSystemVPC` → disassociate. Wait for it to finish.
2. **Delete** the rule.
3. **Inbound endpoints → Inbound from HQ → Delete** (type the confirmation).
4. **Outbound endpoints → Outbound HQ → Delete**.
5. *Optional, beyond the demo:* **Query logging** → the config → **Stop logging queries** (disassociate the VPC) → **Delete**. It's not billed per hour, but it's tidy.

> [!important] Keep these
> The **peering connection** and its routes cost nothing while idle, so they can stay unless the sheet says otherwise. The **Market Prediction (default) VPC** can stay too.

> [!success] Confirm
> **Inbound endpoints** and **Outbound endpoints** lists are both empty.

---

## 8. Troubleshooting

| Problem | Likely cause | Fix |
|---|---|---|
| Can't create peering: overlapping CIDR | The second VPC overlaps `172.19.0.0/16` | Use the default VPC (`172.31.0.0/16`) or another non-overlapping VPC |
| Peering stuck in *Pending acceptance* | Not accepted yet | **Actions → Accept request** |
| No "Create default VPC" option | A default VPC already exists | Just rename it |
| Outbound/Inbound endpoint creation fails | Picked two IPs in the **same** AZ, or a subnet from another VPC | One IP per AZ, both in `TradingSystemVPC` private subnets |
| Endpoint stuck in *Creating* | Normal for a few minutes | Wait and refresh |
| Can't delete the outbound endpoint | A rule still references it | Disassociate and delete the rule first |
| Can't delete the rule | Still associated with a VPC | Disassociate the VPC first |
| Resolver menus show nothing you created | Wrong Region | Switch to us-west-1 |
