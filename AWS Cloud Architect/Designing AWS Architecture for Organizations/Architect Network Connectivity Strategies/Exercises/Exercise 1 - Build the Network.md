---
title: "Exercise 1 – Build the Network"
aliases:
  - Exercise 1 Results
  - TradingSystemVPC Build
course: AWS Cloud Architect – Designing AWS Architecture for Organizations
lessons:
  - L1-A10 Exercise 1
type: lab-results
status: complete
created: 2026-10-17
source: "[[Building a VPC#7. Lab Walkthrough – Exercise 1]]"
related:
  - "[[Building a VPC]]"
  - "[[AWS Global Infrastructure]]"
tags:
  - aws/networking/vpc
  - aws/lab
  - lab-results
---

# Exercise 1 – Build the Network

> [!success] Result
> ==Every required resource, name, CIDR, association, and route matches the exercise.== There is one deviation: the second AZ is `us-west-1c` instead of `us-west-1b`. That's an account-level constraint, not an error, and the design still spans two AZs. A few settings the exercise didn't ask about are worth knowing before later labs (see [[#4. Beyond the Exercise – Settings Worth Knowing]]).

**Spec:** [[Building a VPC#7. Lab Walkthrough – Exercise 1]] · **How to:** [[Exercise 1 - Build the Network - How To]]
**Evidence:** `Exercise1-template-1792279033571.yaml` in this folder. It's a CloudFormation **IaC generator** export of the live resources, taken after the lab.

---

## 1. Checklist Against the Spec

| Spec item | Expected | Built | ✓ |
|---|---|---|---|
| Region | `us-west-1` | `us-west-1` (from the IaC generator ARN) | ✅ |
| VPC | `TradingSystemVPC`, `172.19.0.0/16`, Amazon IPv6 | `vpc-06256dbdb40e3370a`, `172.19.0.0/16`, IPv6 `2600:1f1c:b81:1b00::/56` (Amazon-provided) | ✅ |
| Public Subnet 1 | `us-west-1a`, `172.19.0.0/26` | `us-west-1a` (`usw1-az1`), `172.19.0.0/26` | ✅ |
| Public Subnet 2 | `us-west-1b`, `172.19.0.64/26` | **`us-west-1c`** (`usw1-az3`), `172.19.0.64/26` | ⚠️ AZ, see [[#3. The AZ Deviation – us-west-1c]] |
| Private Subnet 1 | `us-west-1a`, `172.19.4.0/22` | `us-west-1a` (`usw1-az1`), `172.19.4.0/22` | ✅ |
| Private Subnet 2 | `us-west-1b`, `172.19.8.0/22` | **`us-west-1c`** (`usw1-az3`), `172.19.8.0/22` | ⚠️ AZ |
| Internet gateway | `TradingSystemIGW`, attached | `igw-011a3f53fd974f6f6`, attached to the VPC | ✅ |
| Route tables | Public + private, custom | `TradingSystemPublicRouteTable` (`rtb-0403…`), `TradingSystemPrivateRouteTable` (`rtb-0fc7…`) | ✅ |
| Associations | 2 subnets each | Public table: 2 subnets. Private table: 2 subnets. Main table: none | ✅ (see the note below) |
| VGW | `VPN to Corp HQ`, attached | `vgw-0846af59abb691b60`, `ipsec.1`, Amazon ASN 64512, attached | ✅ |
| S3 endpoint | `TradingSystemS3Endpoint`, gateway, private table | Gateway, `com.amazonaws.us-west-1.s3`, route tables = private table | ✅ |
| Public routes | `0.0.0.0/0` and `::/0` → IGW | Both → `igw-011a…` | ✅ |
| Private routes | `192.168.48.0/20` → VGW; S3 route present | `192.168.48.0/20` → `vgw-0846…`; `pl-6ba54002` → `vpce-021b…` | ✅ |
| Private subnets isolated | No internet route | No `0.0.0.0/0` or `::/0` in the private table | ✅ |

> [!note] One thing the template can't prove
> The association resources reference subnet **IDs**, but the exported subnet resources only carry **names and CIDRs**. The counts are right (2 + 2), but the export doesn't show *which* IDs are the public subnets. To confirm the pairing, run:
>
> ```bash
> aws ec2 describe-route-tables --region us-west-1 \
>   --filters Name=vpc-id,Values=vpc-06256dbdb40e3370a \
>   --query "RouteTables[].{Table:Tags[?Key=='Name']|[0].Value,Subnets:Associations[].SubnetId}"
> aws ec2 describe-subnets --region us-west-1 \
>   --filters Name=vpc-id,Values=vpc-06256dbdb40e3370a \
>   --query "Subnets[].[Tags[?Key=='Name']|[0].Value,SubnetId,CidrBlock,AvailabilityZone]" --output table
> ```
>
> Or open **VPC → Your VPCs → TradingSystemVPC → Resource map**.

---

## 2. Route Tables as Built

| Table | Destination | Target | Purpose |
|---|---|---|---|
| **Public** `rtb-04034306a024d7af4` | `172.19.0.0/16` | `local` | Intra-VPC (IPv4) |
| | `2600:1f1c:b81:1b00::/56` | `local` | Intra-VPC (IPv6) |
| | `0.0.0.0/0` | `igw-011a3f53fd974f6f6` | Internet (IPv4) |
| | `::/0` | `igw-011a3f53fd974f6f6` | Internet (IPv6) |
| **Private** `rtb-0fc7b39db18c9780e` | `172.19.0.0/16` | `local` | Intra-VPC (IPv4) |
| | `2600:1f1c:b81:1b00::/56` | `local` | Intra-VPC (IPv6) |
| | `192.168.48.0/20` | `vgw-0846af59abb691b60` | HQ over VPN |
| | `pl-6ba54002` (S3 prefix list) | `vpce-021bfe9965a663b23` | Private S3 path |
| **Main** (untagged) `rtb-0ae231039088c544b` | `172.19.0.0/16`, IPv6 `/56` | `local` | Default for any *unassociated* subnet |

> [!tip] The main route table is a safe default
> The VPC's **main** route table was left with only `local` routes, and all four subnets are **explicitly** associated with custom tables. Any subnet created later without an association falls back to the main table. That makes it isolated by default instead of accidentally public. This is good practice. ^main-table-safe

---

## 3. The AZ Deviation – us-west-1c

The exercise says `us-west-1b`, but the subnets landed in **`us-west-1c`** (AZ ID `usw1-az3`).

- **Why it happened** (*beyond the lecture*): AZ **names** like `us-west-1b` are mapped to physical AZs **differently in each AWS account**. The stable identifiers are **AZ IDs** (`usw1-az1`, `usw1-az3`). N. California is also a known exception to "every Region has at least three AZs": most accounts can only use **two** AZs there. If your account's console offered `us-west-1a` and `us-west-1c`, then `1c` was the right choice.
- **Does it break the design?** No. The requirement is **two AZs**, one subnet per tier per AZ ([[AWS Global Infrastructure#^two-az-rule]]). Public 2 and Private 2 share `usw1-az3`, and Public 1 and Private 1 share `usw1-az1`. That's exactly the intended layout.
- **For organization-scale work:** when several accounts must co-locate resources, compare **AZ IDs**, not names ([[AWS Global Infrastructure#7. Critical Analysis]]).

---

## 4. Beyond the Exercise – Settings Worth Knowing

None of these were required, but each matters in a later lesson or a real deployment.

| Setting in the export | Value | Implication | Where it matters |
|---|---|---|---|
| Subnet IPv6 CIDRs | **None** (the VPC has a `/56`, but no subnet got a `/64`) | The `::/0 → IGW` route is **dormant**: no instance can get an IPv6 address yet | If IPv6 is required, assign a `/64` to each subnet |
| `MapPublicIpOnLaunch` (public subnets) | `false` | Instances launched in the "public" subnets **won't get a public IPv4 address automatically**, so they can't reach the internet despite the IGW route | Enable auto-assign, or attach Elastic IPs ([[Building a VPC#10. Critical Analysis]]) |
| `EnableDnsHostnames` | `false` (default for a new VPC) | No DNS hostnames for instances. **Route 53 private hosted zones** and interface-endpoint **private DNS** need it set to `true`. | [[DNS and Network Resolution#1. DNS Inside Every VPC]] |
| `EnableDnsSupport` | `true` | The VPC resolver at `172.19.0.2` works | [[DNS and Network Resolution#^def-vpc-dns]] |
| DHCP options | `AmazonProvidedDNS`, domain `us-west-1.compute.internal` | Instances use the VPC resolver and get `*.us-west-1.compute.internal` names | DNS note |
| Endpoint policy | Default **full access** (`"Action": "*"`, `"Resource": "*"`) | Private subnets can reach **any** S3 bucket through the endpoint, which is an exfiltration path | Tighten it ([[Secure and Private Connectivity#5. Worked Example – Locking S3 to the VPC]]) |
| Network ACL | The **default** NACL on all four subnets | Allow-all in both directions. SGs are the only filter. | [[Secure and Private Connectivity#2. Security Groups vs. Network ACLs]] |
| S3 endpoint on the public table | **Not** associated | Public-subnet S3 traffic would use the IGW path | [[Building a VPC#10. Critical Analysis]] |

---

## 5. About the Exported Template

The file is a **CloudFormation IaC generator** snapshot. It's a good audit record, but it is **not redeployable as-is**:

| Issue | Why it would fail or misbehave |
|---|---|
| Hard-coded IDs (`rtb-…`, `subnet-…`, `vpc-…`, `igw-…`) instead of `!Ref` | It would point at the *existing* lab resources, not new ones |
| `local` routes exported as `AWS::EC2::Route` with `GatewayId: local` | Local routes are created automatically and can't be declared |
| `AWS::EC2::VPCCidrBlock` repeating the primary `172.19.0.0/16` | The primary CIDR is already set on the VPC, so this would conflict |
| Default NACL, main route table, and DHCP options exported as resources | These are VPC defaults, not resources you create |
| `DeletionPolicy: Retain` everywhere | Deleting the stack would leave every resource behind |

> [!tip] Turning it into real infrastructure as code (*beyond the lecture*)
> Rewrite it with `!Ref` and `!GetAtt` between resources, drop the defaults and local routes, and parameterize the CIDRs and AZs. The result rebuilds this network in any account in minutes, and the "doesn't match any existing route" defaults become reviewable code.

> [!warning] Account ID in the vault
> The template's metadata includes the lab account's ID. It's a temporary course account, so the risk is low. But this vault syncs to GitHub. If that repo is public, consider redacting account IDs from future exports.

---

## 6. Lessons From This Lab

- [ ] Specs name AZs, but **accounts map AZ names differently**. Design for "two AZs" and verify with **AZ IDs**.
- [ ] An IGW route alone doesn't make instances reachable. They also need a **public IP**.
- [ ] Leaving the **main route table** with only `local` routes makes new subnets **isolated by default** ([[#^main-table-safe]]).
- [ ] A VPC IPv6 block does nothing until **subnets get IPv6 CIDRs**.
- [ ] The S3 gateway endpoint's **default policy is full access**. Restricting it is a separate step.
- [ ] **IaC generator** exports are audit snapshots, not reusable templates.
