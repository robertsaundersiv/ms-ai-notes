---
title: "Exercise 1 – Build the Network – How To"
aliases:
  - Exercise 1 How To
  - Build the TradingSystemVPC
course: AWS Cloud Architect – Designing AWS Architecture for Organizations
lessons:
  - L1-A10 Exercise 1
type: how-to
created: 2026-10-17
related:
  - "[[Building a VPC]]"
  - "[[Exercise 1 - Build the Network]]"
  - "[[Exercise 2 - Peering and Hybrid DNS - How To]]"
tags:
  - aws/networking/vpc
  - aws/lab
  - how-to
---

# Exercise 1 – Build the Network – How To

> [!abstract] Goal
> Build `TradingSystemVPC` in **us-west-1** with two public and two private subnets across two AZs. Add an internet gateway for the public tier, a virtual private gateway for HQ, and an S3 gateway endpoint for the private tier. All of it is done in the **VPC console**. It takes about 20–30 minutes.

**Concepts:** [[Building a VPC]] · **My results:** [[Exercise 1 - Build the Network]] · **Next lab:** [[Exercise 2 - Peering and Hybrid DNS - How To]]

> [!warning] Console labels drift
> AWS renames buttons and menus from time to time. If a label here doesn't match exactly, look for the closest equivalent in the same place.

---

## 0. Before You Start

- [ ] Sign in to the course's **temporary AWS account**
- [ ] Top-right Region selector → **US West (N. California) us-west-1**. Check this before *every* step: resources are created in whatever Region is selected.
- [ ] Open the **VPC console** (search "VPC" in the top search bar)
- [ ] Find out which AZs your account has: **Create subnet → Availability Zone** dropdown. If there is no `us-west-1b`, use `us-west-1c` wherever this guide says "second AZ". That's normal for this Region ([[Exercise 1 - Build the Network#3. The AZ Deviation – us-west-1c]]).

| Resource | Name to use |
|---|---|
| VPC | `TradingSystemVPC` |
| Subnets | `Public Subnet 1`, `Public Subnet 2`, `Private Subnet 1`, `Private Subnet 2` |
| Internet gateway | `TradingSystemIGW` |
| Route tables | `TradingSystemPublicRouteTable`, `TradingSystemPrivateRouteTable` |
| Virtual private gateway | `VPN to Corp HQ` |
| Gateway endpoint | `TradingSystemS3Endpoint` |

---

## 1. Create the VPC

1. Left menu **Virtual private cloud → Your VPCs** → **Create VPC**.
2. **Resources to create:** choose **VPC only**. (*VPC and more* would auto-create subnets, routes, and gateways with its own names and CIDRs, which you don't want here.)
3. **Name tag:** `TradingSystemVPC`
4. **IPv4 CIDR block:** *IPv4 CIDR manual input* → `172.19.0.0/16`
5. **IPv6 CIDR block:** *Amazon-provided IPv6 CIDR block* (network border group `us-west-1`)
6. **Tenancy:** Default
7. **Create VPC**.

> [!success] Check
> The VPC details show IPv4 `172.19.0.0/16` and an IPv6 `/56` starting `2600:…`.

---

## 2. Create the Four Subnets

You can create all four in one form with **Add new subnet**.

1. **Subnets → Create subnet**.
2. **VPC ID:** `TradingSystemVPC`.
3. Fill in each subnet, clicking **Add new subnet** between them:

| Subnet name | Availability Zone | IPv4 subnet CIDR block |
|---|---|---|
| `Public Subnet 1` | `us-west-1a` | `172.19.0.0/26` |
| `Public Subnet 2` | second AZ (`us-west-1b`, or `us-west-1c`) | `172.19.0.64/26` |
| `Private Subnet 1` | `us-west-1a` | `172.19.4.0/22` |
| `Private Subnet 2` | second AZ | `172.19.8.0/22` |

4. Leave **IPv6 subnet CIDR block** empty. The exercise doesn't ask for subnet IPv6.
5. **Create subnet**.

> [!success] Check
> The **Subnets** list (filter by the VPC) shows four rows. Available IPv4 addresses: **59** for each `/26` and **1019** for each `/22`, because AWS reserves 5 per subnet ([[Building a VPC#^aws-reserved-five]]).

---

## 3. Create and Attach the Internet Gateway

1. **Internet gateways → Create internet gateway**.
2. **Name tag:** `TradingSystemIGW` → **Create internet gateway**.
3. On the success banner, click **Attach to a VPC**. Or use **Actions → Attach to VPC**.
4. Select `TradingSystemVPC` → **Attach internet gateway**.

> [!success] Check
> State = **Attached**, with VPC ID = `TradingSystemVPC`.

---

## 4. Create the Route Tables and Associate Subnets

1. **Route tables → Create route table**.
   - **Name:** `TradingSystemPublicRouteTable`. **VPC:** `TradingSystemVPC` → **Create route table**.
2. Repeat for `TradingSystemPrivateRouteTable`.
3. Select **TradingSystemPublicRouteTable** → **Subnet associations** tab → **Edit subnet associations**. Tick `Public Subnet 1` and `Public Subnet 2` → **Save associations**.
4. Select **TradingSystemPrivateRouteTable** → **Subnet associations** → **Edit subnet associations**. Tick `Private Subnet 1` and `Private Subnet 2` → **Save associations**.

> [!tip] Leave the main route table alone
> The VPC also has an unnamed **main** route table (Main = Yes). Don't add routes to it or use it. Any subnet you forget to associate falls back to it, and with only local routes, that subnet stays isolated ([[Exercise 1 - Build the Network#^main-table-safe]]).

---

## 5. Create and Attach the Virtual Private Gateway

1. Left menu **Virtual private network (VPN) → Virtual private gateways** → **Create virtual private gateway**.
2. **Name tag:** `VPN to Corp HQ`
3. **Autonomous System Number (ASN):** *Amazon default ASN*
4. **Create virtual private gateway**.
5. Select it → **Actions → Attach to VPC** → `TradingSystemVPC` → **Attach to VPC**.

> [!success] Check
> State moves from *attaching* to **attached**. This can take a minute, so refresh.

> [!note] Not a working VPN yet
> You're only building the **AWS side**. A **customer gateway** and a **Site-to-Site VPN connection** would complete it, but they need HQ's device details, which the exercise doesn't provide. Don't create a VPN connection: it's billed hourly.

---

## 6. Create the S3 Gateway Endpoint

1. **Endpoints → Create endpoint**.
2. **Name tag:** `TradingSystemS3Endpoint`
3. **Type** (or *Service category*): **AWS services**
4. **Services:** search `s3` → select **`com.amazonaws.us-west-1.s3`** with **Type = Gateway**. Don't pick the *Interface* row: it's billed and works differently ([[Secure and Private Connectivity#4. VPC Endpoints – The Side Door]]).
5. **VPC:** `TradingSystemVPC`
6. **Route tables:** tick **only** `TradingSystemPrivateRouteTable`
7. **Policy:** *Full access* (the exercise default; see [[Secure and Private Connectivity#5. Worked Example – Locking S3 to the VPC]] for the hardened version)
8. **Create endpoint**.

> [!success] Check
> Status = **Available**. The private route table's **Routes** tab now has a `pl-…` destination with target `vpce-…`. AWS adds it automatically.

---

## 7. Add the Routes

### Public route table

1. Select **TradingSystemPublicRouteTable** → **Routes** tab → **Edit routes**.
2. **Add route:** Destination `0.0.0.0/0` → Target **Internet Gateway** → `TradingSystemIGW`.
3. **Add route:** Destination `::/0` → Target **Internet Gateway** → `TradingSystemIGW`.
4. **Save changes**.

### Private route table

1. Select **TradingSystemPrivateRouteTable** → **Routes** → **Edit routes**.
2. **Add route:** Destination `192.168.48.0/20` → Target **Virtual Private Gateway** → `VPN to Corp HQ`.
3. **Save changes**.
4. Confirm the S3 `pl-…` → `vpce-…` route is still listed.

> [!warning] Don't add a default route to the private table
> No `0.0.0.0/0` or `::/0` route goes here. Its absence is what keeps the private subnets "strictly disconnected" ([[Building a VPC#^isolation-by-routing]]).

---

## 8. Verify the Whole Build

- [ ] **Your VPCs → TradingSystemVPC → Resource map** shows 4 subnets → 2 named route tables → IGW (public) / VGW + S3 endpoint (private)
- [ ] Public table routes: `local` ×2, `0.0.0.0/0 → igw-…`, `::/0 → igw-…`
- [ ] Private table routes: `local` ×2, `192.168.48.0/20 → vgw-…`, `pl-… → vpce-…`
- [ ] Each table's **Subnet associations** tab lists the right two subnets under *Explicit subnet associations*
- [ ] IGW **Attached**, VGW **attached**, endpoint **Available**

**Optional – capture the build for your records:** CloudFormation → **IaC generator** → *Start a scan* → *Create template*, then select the VPC's resources. That's how [[Exercise 1 - Build the Network|my results]] were captured. Redact the account ID before committing it.

---

## 9. Troubleshooting

| Problem | Likely cause | Fix |
|---|---|---|
| `us-west-1b` isn't in the AZ list | The account only has two AZs in this Region | Use `us-west-1c` |
| "CIDR block is invalid" or "conflicts with another subnet" | Typo, or a `/22` that isn't aligned | Use the exact CIDRs above. `/22` blocks start at `.4.0`, `.8.0`, … |
| "CIDR … is not within the VPC's CIDR" | Subnet created in the wrong VPC | Check **VPC ID** in the subnet form |
| VPC, subnets, etc. "disappeared" | Region selector changed | Switch back to **us-west-1** |
| IGW target missing from the route editor | IGW isn't attached yet | Attach it first (step 3) |
| VGW target missing | VGW still *attaching* | Wait, refresh, then edit routes |
| No `pl-…` route in the private table | Endpoint associated with the wrong table, or the interface type was chosen | Endpoint → **Route tables** tab → *Manage route tables* |

---

## 10. Cleanup

> [!important] Don't tear down yet
> **Exercises 2 and 3 build on `TradingSystemVPC`.** Clean up only after Exercise 3, or when the course says so. Nothing in this exercise is billed by the hour, so leaving it up costs nothing.

When you do tear down, work in this order:

1. Delete the endpoint `TradingSystemS3Endpoint`.
2. **Detach**, then delete, the VGW `VPN to Corp HQ`.
3. **Detach**, then delete, the IGW `TradingSystemIGW`.
4. Delete the VPC. That also removes its subnets, custom route tables, default NACL, and default SG.

---

## 11. CLI Equivalent

*Optional.* This does the same build from the AWS CLI. Replace the `*-EXAMPLE` IDs with the ones each command returns.

```bash
aws ec2 create-vpc --region us-west-1 --cidr-block 172.19.0.0/16 --amazon-provided-ipv6-cidr-block \
  --tag-specifications 'ResourceType=vpc,Tags=[{Key=Name,Value=TradingSystemVPC}]'
aws ec2 create-subnet --vpc-id vpc-EXAMPLE --cidr-block 172.19.0.0/26  --availability-zone us-west-1a \
  --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=Public Subnet 1}]'
aws ec2 create-subnet --vpc-id vpc-EXAMPLE --cidr-block 172.19.0.64/26 --availability-zone us-west-1c \
  --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=Public Subnet 2}]'
aws ec2 create-subnet --vpc-id vpc-EXAMPLE --cidr-block 172.19.4.0/22  --availability-zone us-west-1a \
  --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=Private Subnet 1}]'
aws ec2 create-subnet --vpc-id vpc-EXAMPLE --cidr-block 172.19.8.0/22  --availability-zone us-west-1c \
  --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=Private Subnet 2}]'
aws ec2 create-internet-gateway \
  --tag-specifications 'ResourceType=internet-gateway,Tags=[{Key=Name,Value=TradingSystemIGW}]'
aws ec2 attach-internet-gateway --internet-gateway-id igw-EXAMPLE --vpc-id vpc-EXAMPLE
aws ec2 create-route-table --vpc-id vpc-EXAMPLE \
  --tag-specifications 'ResourceType=route-table,Tags=[{Key=Name,Value=TradingSystemPublicRouteTable}]'
aws ec2 create-route-table --vpc-id vpc-EXAMPLE \
  --tag-specifications 'ResourceType=route-table,Tags=[{Key=Name,Value=TradingSystemPrivateRouteTable}]'
aws ec2 associate-route-table --route-table-id rtb-PUBLIC  --subnet-id subnet-PUBLIC1   # repeat for each subnet
aws ec2 create-vpn-gateway --type ipsec.1 \
  --tag-specifications 'ResourceType=vpn-gateway,Tags=[{Key=Name,Value=VPN to Corp HQ}]'
aws ec2 attach-vpn-gateway --vpn-gateway-id vgw-EXAMPLE --vpc-id vpc-EXAMPLE
aws ec2 create-vpc-endpoint --vpc-id vpc-EXAMPLE --vpc-endpoint-type Gateway \
  --service-name com.amazonaws.us-west-1.s3 --route-table-ids rtb-PRIVATE \
  --tag-specifications 'ResourceType=vpc-endpoint,Tags=[{Key=Name,Value=TradingSystemS3Endpoint}]'
aws ec2 create-route --route-table-id rtb-PUBLIC  --destination-cidr-block 0.0.0.0/0 --gateway-id igw-EXAMPLE
aws ec2 create-route --route-table-id rtb-PUBLIC  --destination-ipv6-cidr-block ::/0 --gateway-id igw-EXAMPLE
aws ec2 create-route --route-table-id rtb-PRIVATE --destination-cidr-block 192.168.48.0/20 --gateway-id vgw-EXAMPLE
```
