---
title: "Exercise 3 – Deploy FastAPI on Amazon ECS with Fargate – How To"
aliases:
  - L3 Exercise 3 How To
  - ECS FastAPI Exercise
course: AWS Cloud Architect – Designing AWS Architecture for Workloads
lessons:
  - C2-L3 Exercise 3 (ECS)
type: how-to
created: 2026-10-19
related:
  - "[[Application and Container Orchestration]]"
  - "[[Exercise 2 - Query S3 Data with Amazon Athena - How To]]"
tags:
  - aws/ecs
  - aws/fargate
  - aws/ecr
  - aws/lab
  - how-to
---

# Exercise 3 – Deploy FastAPI on Amazon ECS with Fargate – How To

> [!abstract] Goal
> Containerize a tiny **FastAPI** app, push it to **Amazon ECR**, and run it as an **ECS service on Fargate** behind an **Application Load Balancer**, inside a VPC created by CloudFormation. Success = `{"message": "Hello, World!"}` at the load balancer's URL.
>
> It takes about 60–90 minutes and costs **about $0.05/hour** while running, so clean up the same day.

**Concepts:** [[Application and Container Orchestration#3. Container Orchestration with Amazon ECS and Fargate]] · **Other labs:** [[Exercise 1 - Assessing and Optimizing Workloads - How To|Exercise 1]] · [[Exercise 2 - Query S3 Data with Amazon Athena - How To|Exercise 2]]
**Sources:** the course repo `lesson-3-managed-services/exercise 3/`: `starter/ecs_exercise_instructions.md`, `ecs-exercise-setup.yaml`, `ECS-Exercise.Dockerfile`, `fastapi_app.py`, `requirements.txt`, and `solution/solution_instructions.md`.

> [!warning] Fixes to the repo instructions
> 1. **Cloud9 is gone** for new customers, and **CloudShell can't run Docker**. Build the image on your PC with **Docker Desktop** (already installed), or on a small EC2 build host (section 3, option B).
> 2. **The repo's custom execution policy can't pull from ECR.** It has no `ecr:*` permissions, so tasks fail with `CannotPullContainerError`. Use the AWS-managed **`AmazonECSTaskExecutionRolePolicy`** (section 4).
> 3. **Inconsistent names:** the policy is created as `ECSExerciseExecutionPolicy` but attached as `ECSExecutionPolicy`. The image is tagged `ecs-exercise-app` but pushed as `ecs-exercise-app-<initials>`. Use **one** repository name throughout.
> 4. **Execution role vs. task role:** the repo puts the role in "Task Role". It belongs in **Task execution role** (used by ECS to pull images and write logs).
> 5. **No initials:** the Cloud Lab forbids personal info in resource names, so use `ecs-exercise-app` without initials.
> 6. The "Configure the Load Balancer" section is **redundant** if you create the ALB inside the service wizard, which is simpler.

---

## 0. Before You Start

- [ ] Cloud Lab console open; Region **us-east-1**
- [ ] On your PC: **Docker Desktop** running, and **AWS CLI v2** installed
- [ ] Your Cloud Lab **temporary credentials** set in your own terminal (Udacity **Cloud Resources** tab), for example as `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`. Never paste them into notes or chats.
- [ ] The repo's `exercise 3/starter/` folder downloaded locally

| Resource | Name |
|---|---|
| CloudFormation stack | `ecs-exercise-setup` (VPC `ECS-API-VPC`, 2 public subnets) |
| ECR repository | `ecs-exercise-app` |
| Execution role | `ecsTaskExecutionRole` |
| Cluster | `ECSExerciseCluster` |
| Task definition / container | `FastAPITask` / `fastapi-container` |
| Service | `ECSExerciseService` |
| Load balancer | `FastAPILoadBalancer` |

**Cost while running** (illustrative): ALB about \$0.0225/h + Fargate 0.25 vCPU / 0.5 GB about \$0.012/h + public IPv4 addresses about \$0.005/h each ≈ **\$0.05/h**.

---

## 1. Create the VPC with CloudFormation

1. Open **CloudShell** → **Actions → Upload file** → `ecs-exercise-setup.yaml`.
2. Run:

```bash
aws cloudformation create-stack --stack-name ecs-exercise-setup \
  --template-body file://ecs-exercise-setup.yaml --region us-east-1
aws cloudformation wait stack-create-complete --stack-name ecs-exercise-setup --region us-east-1
aws cloudformation describe-stacks --stack-name ecs-exercise-setup \
  --query "Stacks[0].Outputs" --output table --region us-east-1
```

The template creates **`ECS-API-VPC` (10.0.0.0/16)**, an internet gateway, and **two public subnets** (10.0.1.0/24 and 10.0.2.0/24, in two AZs, auto-assigned public IPs) with a public route table. It creates no IAM resources, so `--capabilities` isn't needed.

---

## 2. (Optional) Run the App Locally

From the `starter/` folder, in PowerShell:

```bash
docker build -f ECS-Exercise.Dockerfile -t ecs-exercise-app .
docker run --rm -p 8080:80 ecs-exercise-app
```

Open `http://localhost:8080` → `{"message":"Hello, World!"}`. `http://localhost:8080/docs` shows FastAPI's interactive docs. Stop with Ctrl+C.

> [!note] The Dockerfile
> `python:3.8-slim` + `pip install fastapi uvicorn` + `uvicorn fastapi_app:app --host 0.0.0.0 --port 80`. Python 3.8 is end-of-life. It still builds, but `python:3.12-slim` is a safe swap if you want a current base.

---

## 3. Push the Image to ECR

### Option A – Docker Desktop on your PC (recommended)

```bash
aws sts get-caller-identity --query Account --output text   # note your account ID
aws ecr create-repository --repository-name ecs-exercise-app --region us-east-1
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com
docker build -f ECS-Exercise.Dockerfile -t ecs-exercise-app .
docker tag ecs-exercise-app:latest <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/ecs-exercise-app:latest
docker push <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/ecs-exercise-app:latest
```

> [!success] Check
> **ECR → Repositories → ecs-exercise-app** shows a `latest` image. Copy its **Image URI**.

### Option B – a small EC2 build host

If you can't use Docker locally:
1. Launch an Amazon Linux 2023 **t3.micro** with an instance role that has **`AmazonEC2ContainerRegistryPowerUser`**.
2. Connect with EC2 Instance Connect and run `sudo dnf install -y docker && sudo systemctl start docker`.
3. Copy the starter files over and run the Option A commands with `sudo docker`.
4. **Terminate** the instance afterwards.

---

## 4. Create the Task Execution Role

1. **IAM → Roles → Create role** → **AWS service** → **Elastic Container Service** → use case **Elastic Container Service Task** → **Next**.
2. Attach **`AmazonECSTaskExecutionRolePolicy`**. It grants ECR pull and CloudWatch Logs permissions.
3. Name it **`ecsTaskExecutionRole`** → **Create role**.

> [!note] If the grader looks for the repo's policy
> You can *also* create `ECSExerciseExecutionPolicy` from the repo JSON and attach it to the same role. Keep the managed policy, though: without it, the image pull fails.

*(The task definition form can also create this role for you: **Task execution role → Create new role**.)*

---

## 5. Create the ECS Cluster

**ECS → Clusters → Create cluster** → name **`ECSExerciseCluster`** → Infrastructure: **AWS Fargate (serverless)** → **Create**.

---

## 6. Create the Task Definition

**ECS → Task definitions → Create new task definition**:

| Setting | Value |
|---|---|
| Family | `FastAPITask` |
| Launch type | **AWS Fargate** |
| OS / architecture | Linux / **X86_64** (matches an image built on Windows/Intel) |
| Task size | **0.25 vCPU / 0.5 GB** |
| Task role | *(none needed)* |
| **Task execution role** | **`ecsTaskExecutionRole`** |
| Container name | `fastapi-container` |
| Image URI | `<ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/ecs-exercise-app:latest` |
| Port mapping | **80 / TCP**, app protocol HTTP |
| Logging | Leave **Use log collection** on (CloudWatch `awslogs`) |

→ **Create**.

---

## 7. Create the Service with an Application Load Balancer

**ECS → Clusters → ECSExerciseCluster → Services → Create**:

| Section | Setting |
|---|---|
| Compute | **Launch type → FARGATE** |
| Deployment | Task definition **`FastAPITask`** (latest) · Service name **`ECSExerciseService`** · Desired tasks **1** |
| Networking | VPC **`ECS-API-VPC`** · Subnets **both** `ECS-API-Public-Subnet-*` · Security group: **Create new**, inbound **HTTP 80** from anywhere (test only) · **Public IP: ON** |
| Load balancing | **Application Load Balancer** → **Create a new load balancer** → name **`FastAPILoadBalancer`** · Listener **HTTP : 80** · Target group **create new** (`fastapi-tg`), protocol HTTP, health check path **`/`** |

→ **Create**. Wait until the service shows **1/1 tasks running** and the target group shows **healthy** (a few minutes).

> [!important] Why "Public IP: ON" matters
> The subnets are public, with no NAT gateway or VPC endpoints. A Fargate task needs a **public IP** to reach ECR and pull its image. Without one, it fails with `CannotPullContainerError`.

---

## 8. Test the API

1. **EC2 → Load Balancers → FastAPILoadBalancer** → copy the **DNS name**.
2. Open `http://<DNS name>/` → **`{"message":"Hello, World!"}`**. Try `http://<DNS name>/docs` too.
3. Optional: **ECS → task → Logs** shows uvicorn's request lines in CloudWatch.

> [!tip] What this demonstrates
> You never configured an instance, a Docker daemon, or an Auto Scaling group. ECS keeps **1 task** running behind the ALB, and Fargate supplies the compute. That's the "after" architecture from [[Application and Container Orchestration#^ecs-declarative]].

---

## 9. Verify the Whole Exercise

- [ ] Stack `ecs-exercise-setup` is **CREATE_COMPLETE** (VPC + 2 public subnets)
- [ ] ECR `ecs-exercise-app` has the `latest` image
- [ ] Role `ecsTaskExecutionRole` with `AmazonECSTaskExecutionRolePolicy`
- [ ] Cluster `ECSExerciseCluster` (Fargate); task definition `FastAPITask` (port 80)
- [ ] Service `ECSExerciseService`: 1/1 running, target **healthy**
- [ ] ALB DNS returns `{"message":"Hello, World!"}`

---

## 10. Troubleshooting

| Problem | Likely cause | Fix |
|---|---|---|
| `CannotPullContainerError` | No public IP on the task, or an execution role without ECR permissions | Public IP **ON**; use `AmazonECSTaskExecutionRolePolicy` |
| `exec format error` in logs | Image built for ARM (e.g. Apple Silicon) | `docker build --platform linux/amd64 …` or set the task architecture to ARM64 |
| ALB returns **503** | No healthy targets | Check the task is running and the health check path is `/` on port 80 |
| Target unhealthy | Task security group blocks the ALB | Allow inbound 80 from the ALB's security group (or anywhere, for the test) |
| `docker login` fails | Expired Cloud Lab credentials or wrong Region | Refresh credentials; use `--region us-east-1` consistently |
| `create-repository` "already exists" | Ran it twice | Fine. Continue with tag and push. |
| Push denied | Repository name in the tag doesn't match | Tag with exactly `…/ecs-exercise-app:latest` |

---

## 11. Cleanup – Same Day

1. **ECS → ECSExerciseService → Update → Desired tasks 0**, then **Delete service**.
2. **EC2 → Load Balancers → delete `FastAPILoadBalancer`**; **Target groups → delete `fastapi-tg`**.
3. **ECS → delete cluster `ECSExerciseCluster`**; **Task definitions → deregister** `FastAPITask` revisions.
4. **ECR → delete repository `ecs-exercise-app`** (with its images).
5. **CloudFormation → delete stack `ecs-exercise-setup`**. It fails if the ALB or tasks still use the subnets, so do steps 1–2 first.
6. Delete the **security groups** the wizard created, `ecsTaskExecutionRole` (if not reused), and the CloudWatch log group `/ecs/FastAPITask`.
7. If you used Option B, terminate the build host.
