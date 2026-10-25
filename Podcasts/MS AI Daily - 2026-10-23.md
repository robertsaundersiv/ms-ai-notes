---
title: "MS AI Daily – 2026-10-23"
type: podcast
created: 2026-10-23
duration_min: 30.0
covers:
  - "[[AWS Cloud Architect/Designing AWS Architecture for Workloads/Project/Migrating-a-Credit-Card-Fraud-Pipeline-to-AWS/README|Fraud Pipeline Project README]]"
  - "[[AWS Cloud Architect/Designing AWS Architecture for Workloads/Project/Migrating-a-Credit-Card-Fraud-Pipeline-to-AWS/starter/fraud_detection_pipeline/README|Fraud Pipeline – Glue Job README]]"
  - "[[AWS Cloud Architect/Designing AWS Architecture for Workloads/Project/Migrating-a-Credit-Card-Fraud-Pipeline-to-AWS/starter/refresh_function/README|Fraud Pipeline – Refresh Function README]]"
  - "[[Optimized Architectures and the Migration Lens]]"
  - "[[Re-platforming to Serverless with AWS Lambda]]"
  - "[[Application and Container Orchestration]]"
  - "[[Secure and Private Connectivity]]"
  - "[[Project Overview]]"
  - "[[Directed Acyclic Graph (DAG)]]"
  - "[[Implementing Evaluator-Optimizer Workflow]]"
  - "[[Exercise 1 - Build the Network - How To]]"
tags:
  - podcast
  - review
---

# MS AI Daily – 2026-10-23

![[MS AI Daily - 2026-10-23.mp3]]

> [!abstract] In this episode
> A teardown of the credit card fraud pipeline migration: Glue for training, ECS on Fargate for serving, and Lambda plus EventBridge for retraining. The theme is that "the job succeeded" isn't the same as "the model is better." The pipeline auto-promotes whatever trained last. That's the same bug as the evaluator-optimizer lab's "last, not best." The fix is a champion-challenger gate, ideally run by an orchestrator. Rapid review and the blast from the past connect the design to the migration lens, Lambda triggers, VPC endpoints, and DAG scheduling.

## Segments
- **Cold open and agenda:** a new CSV lands, and by lunch production is serving a model nobody evaluated. From [[AWS Cloud Architect/Designing AWS Architecture for Workloads/Project/Migrating-a-Credit-Card-Fraud-Pipeline-to-AWS/README|Fraud Pipeline Project README]]
- **Deep dive: migrating the fraud pipeline**
  - *Which R? Mostly replatform, with the refresh function an ambiguous small refactor; Glue vs. EMR; the six-cent training run (2 G.1X DPUs × 4 min); why removing the swallowing `try/except` matters once "succeeded" triggers a deploy:* [[AWS Cloud Architect/Designing AWS Architecture for Workloads/Project/Migrating-a-Credit-Card-Fraud-Pipeline-to-AWS/README|Fraud Pipeline Project README]], [[AWS Cloud Architect/Designing AWS Architecture for Workloads/Project/Migrating-a-Credit-Card-Fraud-Pipeline-to-AWS/starter/fraud_detection_pipeline/README|Glue Job README]], [[Optimized Architectures and the Migration Lens]]
  - *ECS on Fargate: launch type picks compute, not the OS; Fargate doesn't need EFS (the API's `/tmp` model download proves it); execution role vs. task role; the zero-task bootstrap order; `/health` should mean "ready to serve"; Spark for single-row scoring; the Spark 3.5 (Glue 5.0) to PySpark 4.2 version boundary:* [[AWS Cloud Architect/Designing AWS Architecture for Workloads/Project/Migrating-a-Credit-Card-Fraud-Pipeline-to-AWS/README|Fraud Pipeline Project README]], [[Application and Container Orchestration]]
  - *Retraining: the `incoming/` vs. `archive/` prefixes prevent recursive invocation; why Lambda can't run the Spark job; one function with two event shapes, which merges two blast radiuses; at-least-once S3 events and Glue's default limit of one concurrent run; no evaluation gate; class imbalance (492 frauds out of about 285k, so the all-"not fraud" model scores 99.8% accuracy); champion vs. challenger; choreography vs. Step Functions orchestration; infrastructure alarms vs. model monitoring:* [[AWS Cloud Architect/Designing AWS Architecture for Workloads/Project/Migrating-a-Credit-Card-Fraud-Pipeline-to-AWS/starter/refresh_function/README|Refresh Function README]], [[Re-platforming to Serverless with AWS Lambda]], [[Application and Container Orchestration]]
- **Rapid review:** [[Optimized Architectures and the Migration Lens]] (six pillars and three phases recalled; 10% utilization at a 10× peak; sticker shock; unsourced stats), [[Re-platforming to Serverless with AWS Lambda]] (the three conversion changes; least privilege means what *this* function's code does, so the refresh Lambda does need S3 permissions; URL-encoded keys), [[Application and Container Orchestration]] (the 13-task drill; ECS vs. EKS; Fargate removes servers, not architecture work), [[Secure and Private Connectivity]] (stateful SGs vs. stateless NACLs; the ephemeral-port trap; S3 and DynamoDB now also have interface endpoints; ECR, S3 and Logs endpoints for private Fargate tasks), [[Project Overview]] (only Step 2 touches AWS; cross-Region peering because there's one account; $25 budget; no personal data in tags)
- **Blast from the past:** [[Directed Acyclic Graph (DAG)]] (critical path vs. product reliability, 35 s vs. 26 s at about 75% either way; each pipeline run is a DAG, and the monthly loop lives in the trigger; side-effecting retries), [[Implementing Evaluator-Optimizer Workflow]] (the three defects; "NOT APPROVED" contains "APPROVED"; structured output plus code overrides; refine from the best attempt, not the newest), [[Exercise 1 - Build the Network - How To]] (59 and 1,019 usable addresses; privacy by missing default route; the gateway endpoint as a route)

> [!warning] Corrections and gaps flagged in this episode
> - [[AWS Cloud Architect/Designing AWS Architecture for Workloads/Project/Migrating-a-Credit-Card-Fraud-Pipeline-to-AWS/README|Fraud Pipeline Project README]]: the **Dependencies** section lists Python 3.14 with PySpark 3.3.1 and FastAPI 0.89.1. That's stale from the starter repo. PySpark 3.3.1 doesn't support Python 3.14, and `fraud_detection_api/requirements.txt` actually pins PySpark 4.2.0 and FastAPI 0.161.1. Update the section to match the real pins.
> - Same README, a design risk rather than an error: the Glue job runs **Glue 5.0 (Spark 3.5)**, but the API loads the model with **PySpark 4.2**. Spark ML persistence only promises best-effort compatibility across major versions. Either align the versions, or add a load test of each new model in the serving image before promotion.
> - Same README, a design gap: the EventBridge "Glue job succeeded" rule redeploys the API with whatever was just written to `models/fraud_detection_model_latest`. Nothing compares it to the current model. Consider an evaluate, compare and promote step, for example in a Step Functions state machine.
> - [[Secure and Private Connectivity]]: "gateway endpoints are S3 and DynamoDB only" is correct, but S3 and DynamoDB **also** offer interface (PrivateLink) endpoints now. You use those when you need to reach them from on-premises or across a peering connection, because gateway endpoints only work from inside their VPC.
> - [[Application and Container Orchestration]]: the note's own corrections stand (launch type selects compute, not the OS; Fargate doesn't require EFS). The fraud API's `/tmp` model download is a working example of the second point.

## Think about it
Real fraud labels arrive late. A transaction is only confirmed as fraud when a chargeback comes in, often 30–60 days later. So each month's retraining data contains recent fraud mislabeled as legitimate, and any evaluation set built from last month is wrong in the same way. Design the promotion gate for your pipeline under that constraint. What data do you compare challenger and champion on, and what metric and margin do you require? What new failure mode does the gate itself introduce? For example, does it lock in a stale champion while fraudsters change tactics?

> [!quote]- Transcript
> **Marcus:** It's the first of the month. Someone drops a new C S V of labeled transactions into an S 3 folder. Nobody touches anything else. By lunchtime, the production fraud A P I is answering with a brand-new model. Nobody has looked at that model. No test compared it to last month's. Jess, is that a well-automated pipeline, or a liability with excellent uptime?
>
> **Jess:** My gut says well-automated. No manual steps, no tickets, nobody copying model files at midnight. That's the dream, right?
>
> **Marcus:** It's half the dream. The other half is knowing the new thing is better than the old thing before customers meet it. Hold that thought, because it's the thread running through today's whole episode.
>
> **Jess:** Welcome to MS AI Daily. It's Friday, October twenty-third, twenty twenty-six. I'm Jess.
>
> **Marcus:** And I'm Marcus. Today we take your credit card fraud pipeline migration apart piece by piece, and then we ask what it's missing.
>
> **Jess:** So, the agenda. The deep dive is the fraud pipeline project you just wrote up: training on Glue, serving on E C S with Fargate, and retraining with Lambda and EventBridge. Then a rapid review of the migration lens, the Lambda re-platforming lesson, container orchestration, VPC firewalls and endpoints, and the Excipient Technologies project.
>
> **Marcus:** And in Blast from the Past we go back to the Agentic A I course: directed acyclic graphs, the evaluator-optimizer exercise, and one network build from a few weeks ago. Spoiler: the evaluator-optimizer lab had the same bug the fraud pipeline has. Different course, same mistake.
>
> **Jess:** I love it when the courses gang up on me. Okay, set the scene. What did the data scientists actually hand over?
>
> **Marcus:** Three on-premises pieces. One, a Py Spark pipeline on a Hadoop cluster that transforms the transaction data and trains the model. Two, a containerized Fast A P I service on a server that takes a transaction and says fraud or not fraud. Three, a refresh script that watches a folder for new data and kicks off retraining. Before we pick services, let's use the framework from the migration lens. Which of the R's is this?
>
> **Jess:** I'd say refactor. You rewrote the training script, you rewrote the refresh function. Lots of code changed.
>
> **Marcus:** Reasonable, but I'd push back on most of it. The test isn't how many lines changed. It's whether the architecture changed. The training logic is still the same Py Spark pipeline. You just swapped a self-managed Hadoop cluster for a managed Spark runtime. The A P I is still the same container. You just swapped your own server for Fargate. That's replatforming: same design, managed platform underneath.
>
> **Jess:** And the refresh script?
>
> **Marcus:** That one's honestly ambiguous. Going from an infinite polling loop to an event-driven function is a real change in how it works, so you could call it a small refactor. I wouldn't fight anyone over that label. What matters is that you can explain why each piece got the treatment it got.
>
> **Jess:** Fair. So the training job. The requirements were fully managed, no infrastructure experience, trained only monthly so no ongoing cost, and eventually a data catalog. And you picked Glue.
>
> **Marcus:** Glue fits almost word for word. It runs Spark as a serverless job, so there's no cluster to babysit. It bills only while the job runs. And it comes with the Glue Data Catalog and crawlers, which covers the "eventually catalog all our datasets" wish. Your write-up says a training run takes about four minutes on two G one X workers. Quick math, Jess. Each G one X worker is one D P U, a data processing unit, and list price is roughly forty-four cents per D P U hour. What does a run cost?
>
> **Jess:** Two D P Us for four minutes. Four minutes is a fifteenth of an hour, so that's two times forty-four cents divided by fifteen. About six cents?
>
> **Marcus:** About six cents. Check current pricing before quoting it in a design doc, but compare that with a Hadoop cluster sitting there all month waiting for one job. That's the overprovisioning failure mode from the migration lens in its purest form.
>
> **Jess:** Why not E M R, though? That's Amazon's Hadoop and Spark service. Wouldn't that be the more literal lift?
>
> **Marcus:** It would, and for a heavy, daily Spark shop E M R can be the right call. But the team said they have no experience managing infrastructure, and even serverless E M R makes you think in clusters, releases, and capacity. Glue packages that up as "here's my script, run it." When the requirements say "we don't want to manage this," take them at their word.
>
> **Jess:** Okay, what actually changed in the training code?
>
> **Marcus:** The local Spark session became a Glue entry point. The job reads its arguments, the job name, the data location, and the model save path, from Glue's job parameters instead of hard-coded paths. The input is read from S 3 as a dynamic frame, which is Glue's wrapper around a Spark data frame, then converted to a regular data frame for training. The model gets saved twice: once as models slash fraud detection model latest, which the A P I loads, and once as a dated copy in an archive folder.
>
> **Jess:** There was also a line in your notes about removing a try except block.
>
> **Marcus:** That's my favorite change in the whole project, and it's easy to skim past. The starter code wrapped training in a try except that printed the error and carried on. On a laptop, that's just sloppy. In this architecture it's dangerous. Why?
>
> **Jess:** Because the job would report success even when training failed?
>
> **Marcus:** Exactly. And what's listening for "success"?
>
> **Jess:** Oh. The EventBridge rule. When Glue reports that the job succeeded, the Lambda forces a new A P I deployment. So a swallowed error means you redeploy the A P I after a failed training run.
>
> **Marcus:** Right. In the best case the A P I reloads the old model and you've just wasted a deployment. In the worst case a half-written model folder is sitting at the latest path and the new tasks fail to start. Once success is an event other systems react to, lying about success becomes an architectural bug, not a style issue. Let it crash so Glue marks the run Failed and CloudWatch can alarm on it.
>
> **Jess:** That's a good rule in general. Errors that get printed and ignored turn into wrong events downstream.
>
> **Marcus:** Now the serving side. The requirements were a container service with no servers or Kubernetes to manage, automatic scaling, and CloudWatch and CloudTrail integration. That's E C S on Fargate, almost by definition. You've got an Application Load Balancer in front, images in E C R, which is the container registry, and auto scaling from one to four tasks when average C P U goes above sixty percent.
>
> **Jess:** And this is where the container orchestration note had those two corrections, right?
>
> **Marcus:** Yes, and your project proves both of them. The lecture said the launch type is "the configuration for the O S." It isn't. The launch type picks the compute the task runs on: E C 2 instances you manage, or Fargate. The lecture also said Fargate requires E F S, the shared file system. It doesn't. Fargate tasks get ephemeral storage, twenty gibibytes by default. And look at what your A P I does at startup.
>
> **Jess:** It downloads the model from S 3 into slash temp and loads it from there. No E F S at all.
>
> **Marcus:** No E F S at all. E F S is for data that has to persist or be shared across tasks. A model you can re-download on every start is neither. You've basically written the counterexample to the lecture's claim.
>
> **Jess:** Okay, permissions. There are four roles in the write-up, and two of them are E C S roles, the task execution role and the task role. I'll be honest, I think of the execution role as "the role the container runs as." Is that right?
>
> **Marcus:** That's the most common mix-up in E C S, and the name doesn't help. If they ever rename it I'll send flowers. The execution role is used by E C S itself, the agent that sets up your task. It pulls the image from E C R and sends container logs to CloudWatch. Your Python code never sees it. The task role is the one your application code gets. When boto three inside the container asks "who am I," it gets the task role's temporary credentials.
>
> **Jess:** So the execution role gets the container running, and the task role is what the code inside can do once it's up.
>
> **Marcus:** That's it. And that's why your task role has read-only access to the models prefix and nothing else. If the A P I gets compromised, the attacker can read models. They can't overwrite them, and they can't read the raw transaction data. Mix the two roles up and you end up granting S 3 access to the execution role, then wondering why boto three in the container gets access denied.
>
> **Jess:** And no access keys anywhere, because the credentials come from the role.
>
> **Marcus:** Right. Your write-up keeps a dot env file only for local development and keeps it out of the image with a docker ignore file. That's the right instinct.
>
> **Jess:** You also mentioned the deployment order thing. The CloudFormation script creates the service with zero tasks first?
>
> **Marcus:** It's a small detail that shows you've thought about it. The A P I can't start until a model exists, because it downloads the model at startup. If you create the service with one task on day one, the task starts, finds no model, crashes, and E C S keeps restarting it. So the script creates the stack with zero tasks, pushes the image, uploads data, runs the first training job, and only then scales to one. Bootstrapping order is real architecture. Plenty of templates are correct and still can't deploy from an empty account.
>
> **Jess:** Does that connect to the health endpoint you added?
>
> **Marcus:** It should, and here's the production nuance. The load balancer only sends traffic to tasks whose health check passes. If slash health returns okay before the Spark model has actually loaded, the load balancer sends real transactions to a task that can't score them yet. The health check should mean "ready to serve," not "the process is alive." And Spark startup isn't fast, so give the health check grace period enough time.
>
> **Jess:** Speaking of Spark. Is it weird to load a Spark model just to score one transaction per request?
>
> **Marcus:** It's a little like booking a symphony orchestra to play a doorbell. It works, and for this project it's the sensible choice because you're reusing the team's pipeline as-is. But it costs you memory, startup time, and latency per request. In production you'd often export the model to something lighter for online scoring, or pick a model library that doesn't need a J V M at all. That's a later optimization, not a flaw in your submission.
>
> **Jess:** Okay, there's something I want to flag. Your README's dependencies section says Python three point fourteen and Py Spark three point three point one. But the A P I's requirements file pins Py Spark four point two.
>
> **Marcus:** Good catch, and it's worth correcting in the note. Py Spark three point three predates Python three point fourteen by years. That old release doesn't support it, so that dependencies list is stale from the starter repo. The requirements file and the Dockerfile with Java twenty-one are the truth. But the bigger issue sits right next to it. Your Glue job is configured as Glue five point oh, which runs Spark three point five. Your A P I loads the model with Py Spark four point two.
>
> **Jess:** So the model is trained on one major version of Spark and loaded on another.
>
> **Marcus:** Exactly. Spark's M L persistence docs say compatibility across major versions is best effort, not guaranteed. It may load fine today. It may break on some pipeline stage after an upgrade. The fix is boring: run the same Spark version for training and serving, or add a test that loads a fresh model in the serving image before you promote it. That's a habit worth having. Write down every place a version boundary crosses your pipeline.
>
> **Jess:** Okay. The third piece, retraining. The old script was an infinite loop polling a folder on someone's laptop every ten seconds.
>
> **Marcus:** A hard-coded path to one developer's home folder, which is a classic. The new version is a Lambda function triggered by S 3 object created events on the data slash incoming prefix. It copies the file to data slash archive with a dated name, deletes the original, and calls the Glue A P I to start the training job on the archived file.
>
> **Jess:** Wait. A Lambda triggered by S 3 that writes to the same bucket. That's the recursive invocation warning from the Lambda lesson.
>
> **Marcus:** It is, and this is why the prefix layout matters. The trigger only watches incoming. The function writes to archive, which is outside the trigger's filter. So the copy doesn't fire the function again. Same bucket, different prefix, no loop. If someone later "simplifies" the trigger to the whole bucket, you get the infinite loop and the bill that comes with it.
>
> **Jess:** And why not just train inside the Lambda? It's already running.
>
> **Marcus:** In practice Lambda can't run this job. The standard Python runtime has no J V M for Spark. A function maxes out at fifteen minutes and ten gigabytes of memory. And it's the wrong tool even if you could squeeze it in. Lambda is great as the glue, small letter g, between events. Glue, capital G, does the heavy lifting.
>
> **Jess:** Ha. Okay, so the Lambda just starts the job. Then what?
>
> **Marcus:** Then a second trigger. An EventBridge rule matches the Glue event that says this job's state changed to succeeded, and it invokes the same Lambda. This time the function tells E C S to force a new deployment. E C S starts fresh tasks, they download the new latest model at startup, and the old tasks drain away.
>
> **Jess:** One function, two different kinds of events. Is that clean, or is it a shortcut?
>
> **Marcus:** It's a trade-off, and I'd want you to be able to defend either choice. One function means one deployment and one set of logs. But the function now has to branch on which event it got, and its role needs both Glue start-job permissions and E C S update-service permissions. Two small functions would each get a smaller role. For a monthly job, one function is defensible. Just know that you merged two blast radiuses into one.
>
> **Jess:** What about duplicates? The Lambda note said S 3 notifications are at least once.
>
> **Marcus:** Right, and that's the edge case to think about here. Say S 3 delivers the same object created event twice. Your function runs twice. The first run moves the file and starts Glue. The second run might find the file already gone, or it might try to start a second Glue run. By default a Glue job allows one concurrent run, so that second start call fails with a concurrent runs exception. That's actually a decent safety net, as long as your function treats "already running" as a normal outcome rather than an error that pages someone.
>
> **Jess:** So idempotency again. Running it twice should leave you in the same place as running it once.
>
> **Marcus:** Always idempotency. Now let's go back to the cold open. Map out the whole chain for me. What decides that the new model goes into production?
>
> **Jess:** New file lands, Lambda starts Glue, Glue trains and overwrites latest, Glue reports success, EventBridge fires, Lambda redeploys, new tasks load latest. So, what decides? Nothing, really. It's just that the training job didn't crash.
>
> **Marcus:** That's the gap. "Training succeeded" means the code ran. It doesn't mean the model is any good. And in fraud detection that gap is wide. The Kaggle dataset you're using has four hundred ninety-two frauds out of about two hundred eighty-five thousand transactions. That's about seventeen hundredths of one percent. If a model predicts "not fraud" for every transaction, what's its accuracy?
>
> **Jess:** About ninety-nine point eight percent. And it catches zero fraud.
>
> **Marcus:** Zero fraud, ninety-nine point eight percent accuracy, and a very confident dashboard. So the gate can't be accuracy. You'd compare the new model, the challenger, against the current one, the champion, on the same held-out data, using recall, precision, or the area under the precision-recall curve. Only promote if the challenger wins by some margin.
>
> **Jess:** And this is the evaluator-optimizer connection you teased. The recipe loop returned the last recipe, not the best one.
>
> **Marcus:** Same bug, different course. Your pipeline labels the newest model "latest" and deploys it. The recipe lab returned the last recipe. In both cases "most recent" stands in for "best," and nothing checks. The fix has the same shape too: keep the best so far, and only replace it when an evaluation says the new one is better.
>
> **Jess:** Where would that check live? Inside the Glue job?
>
> **Marcus:** You could put it there, but this is where the orchestration lesson comes in. Right now your pipeline is choreography. Each service reacts to events, and no single place knows the whole flow. That's elegant for two steps. Once you add evaluate, compare, promote, and then deploy, with branches and retries, you want orchestration. A Step Functions state machine would run train, then evaluate, then a choice state: if the challenger wins, copy it to latest and redeploy. If it loses, keep the champion and send an alert.
>
> **Jess:** That's the sales-before-finance example from the lecture, really. Ordering and error handling live in the state machine, not inside each function.
>
> **Marcus:** Exactly. And it's also a D A G, which we'll come back to in Blast from the Past. Last thing before we move on. Your monitoring design has alarms on Lambda errors, unhealthy tasks, server errors, and C P U. All good. But notice that every one of them is an infrastructure signal. None of them would fire if the model quietly started missing more fraud.
>
> **Jess:** Because nothing is measuring the model's predictions.
>
> **Marcus:** Right. A healthy container can serve a bad model all day long. Production M L monitoring adds things like the fraud rate the model is flagging and how inputs are drifting, and later, once real labels arrive, the actual precision and recall. The infrastructure being healthy and the model being healthy are two separate questions.
>
> **Jess:** Okay, I'm convinced it's a strong submission with a clear next step. Rapid review?
>
> **Marcus:** Rapid review. I'll ask, you answer. Migration lens. Six pillars, go.
>
> **Jess:** Operational excellence, security, reliability, performance efficiency, cost optimization, sustainability. Our Systems Rarely Perform Cheaply and Sustainably.
>
> **Marcus:** And the three phases?
>
> **Jess:** Assess, which produces the inventory of apps, dependencies, and usage. Mobilize, which picks the strategy. Then migrate and modernize, which is the pattern, the services, and the deployment.
>
> **Marcus:** Good. Now the utilization idea. A fleet sized for peak, where peak is ten times average demand. Utilization?
>
> **Jess:** Average over peak, so ten percent. Ninety percent of what you pay for is idle.
>
> **Marcus:** And the fraud project's Hadoop cluster, used for four minutes a month, is a far more extreme version of that. The gotcha from that note is sticker shock: bringing fixed-cost habits into a pay-per-use model. Moving to the cloud doesn't save money on its own. Elasticity plus cost controls is what saves money.
>
> **Jess:** And the note was skeptical of the opening statistics, the eighty-five percent of analytics projects fail number.
>
> **Marcus:** Rightly. No source given. Treat it as motivation, not evidence. Next, re-platforming with Lambda. What were the three changes that turned the polling script into a function?
>
> **Jess:** Remove the loop and make it a handler. Get the bucket and key from the event instead of the file system. And publish to S N S through boto three, with the topic A R N in an environment variable.
>
> **Marcus:** And here's a contrast worth noticing. In that lab, the least-privilege answer was that the function needs no S 3 permissions at all, because the event already carries the bucket and key and the function only sends a notification. Does the fraud refresh Lambda get away with that?
>
> **Jess:** No. It copies and deletes objects, so it needs real S 3 permissions, read on incoming, write on archive, delete on incoming. Plus starting the Glue job and updating the E C S service.
>
> **Marcus:** Right. Least privilege isn't "as few permissions as the last lab." It's exactly what this function's code does. One more gotcha from that note: object keys arrive U R L encoded, so a space shows up as a plus sign. Decode the key, or your copy call goes looking for a file that doesn't exist.
>
> **Jess:** Noted, especially since your archive names include dates and underscores.
>
> **Marcus:** Container orchestration. Quick numbers. Target tracking at eight hundred requests per task, peak of ten thousand requests. How many tasks?
>
> **Jess:** Ten thousand over eight hundred is twelve point five, round up, thirteen tasks.
>
> **Marcus:** Good. And E C S versus E K S in one sentence?
>
> **Jess:** E C S is Amazon's own orchestrator and simpler. E K S is managed Kubernetes, worth it when you already have Kubernetes skills and manifests, like the Health Metrics workload.
>
> **Marcus:** And a Fargate gotcha from the critical analysis: it removes servers, not architecture work. You still size tasks, design networking, and set health checks. Which brings us to networking. Secure and private connectivity. Security group versus network A C L, what's the key behavioral difference?
>
> **Jess:** Security groups are attached to network interfaces and don't check reply traffic. Stateful. Network A C Ls sit at the subnet boundary and check both directions, including replies. Stateless. And only network A C Ls can explicitly deny.
>
> **Marcus:** And the trap that follows from "checks replies"?
>
> **Jess:** Ephemeral ports. If a network A C L allows inbound four forty-three but doesn't allow outbound on ten twenty-four through sixty-five thousand five hundred thirty-five, the replies get dropped and the connection just times out.
>
> **Marcus:** Exactly. That's the one that burns hours, because the security group looks perfect. Now endpoints. Gateway versus interface?
>
> **Jess:** Gateway endpoints are route table entries, free, and only for S 3 and DynamoDB. Interface endpoints are network interfaces in your subnets, built on PrivateLink, billed hourly, for most other services.
>
> **Marcus:** All correct, and one small addition to your note. The table makes it sound like S 3 and DynamoDB only come as gateways. Both now also offer interface endpoints, which you'd use when you need to reach them from on-premises over a VPN or Direct Connect, since gateway endpoints only work from inside the VPC. So "gateway endpoints are S 3 and DynamoDB only" is true, but "S 3 and DynamoDB are gateway only" isn't anymore.
>
> **Jess:** That's a subtle one. Does that connect to the fraud project at all?
>
> **Marcus:** Directly. If you put those Fargate tasks in private subnets with no NAT gateway, how do they pull their image and download the model?
>
> **Jess:** They'd need endpoints. The S 3 gateway endpoint for the model. And E C R?
>
> **Marcus:** E C R needs two interface endpoints, one for its A P I and one for the Docker registry. And image layers are stored in S 3, so you still need the S 3 endpoint. Then add a CloudWatch Logs interface endpoint so the log driver works. Forget any one of those and the task fails at startup with an error that sounds like a permissions problem but is really a routing problem.
>
> **Jess:** Last one, the Excipient Technologies project overview.
>
> **Marcus:** What's the gotcha in how it's structured?
>
> **Jess:** Only step two, the network connectivity, actually touches AWS. Steps one, three, and four, the multi-account design, the tagging governance, and the cost controls, are done as scenarios in the report, with simulated outputs.
>
> **Marcus:** And why is the peering done across Regions instead of across accounts?
>
> **Jess:** Because the Cloud Lab gives you one account, and the rubric says separate accounts or Regions. So U S East one and U S West two. Also, twenty-five dollar budget, and blowing through it loses your work, so no NAT gateways, two micro instances, and tear everything down the same day.
>
> **Marcus:** And no personal information in tags. Owner equals cloud architecture, not your name. Good. Time for Blast from the Past.
>
> **Jess:** Directed acyclic graphs. This is from the Agentic A I course, about four weeks back.
>
> **Marcus:** Define it in one breath.
>
> **Jess:** Nodes joined by one-way edges, with no path that leads back to where it started. Because there are no cycles, there's always a topological order, so a runtime can schedule it, run independent branches in parallel, and know it will finish.
>
> **Marcus:** And the two numbers that matter for a D A G of agent steps?
>
> **Jess:** Latency is set by the critical path, the longest chain of dependent steps, not the sum of all steps. But reliability is still the product of every node's success probability. In the postmortem example the chain took thirty-five seconds and the D A G twenty-six, but reliability was about seventy-five percent either way.
>
> **Marcus:** Parallelism fixes latency, gates fix reliability. Now apply it. Is your fraud pipeline a D A G?
>
> **Jess:** Each run is. Ingest, train, evaluate, promote, deploy, all one direction. But the whole thing repeats every month, so it's a cycle?
>
> **Marcus:** Same answer as the note gives for agents. The plan for one run is acyclic. The loop lives outside the graph, in the runtime, which here is S 3 events bringing in next month's data. Keep each run analyzable and let the trigger do the repeating. And the note's warning about side-effecting nodes on retry, like duplicate tickets or emails, is exactly the duplicate S 3 event problem we just walked through.
>
> **Jess:** Everything keeps coming back to idempotency.
>
> **Marcus:** Because distributed systems are just computers repeating themselves at you. Next, the evaluator-optimizer exercise. The recipe optimizer. What were the three real defects?
>
> **Jess:** The refine step never saw the previous recipe, so at temperature one it wrote a whole new recipe every time and fixes didn't accumulate. Approval was detected with fragile string checks. And it returned the last recipe instead of the best.
>
> **Marcus:** And the nastiest of the string checks?
>
> **Jess:** The main block checked whether the word APPROVED appeared anywhere in the evaluation. And "NOT APPROVED" contains "APPROVED." So a rejected recipe for someone with severe allergies gets printed as all constraints satisfied.
>
> **Marcus:** Which is a substring check doing exactly what it was told. The fix in your note is structured output, a per-criterion passed flag decided in code, plus deterministic checks that override the L L M wherever something can be counted. Same lesson as the fraud gate. Don't let free text or a "success" status make a decision a real evaluation should make.
>
> **Jess:** I had a question about the improved version, actually. When a new attempt scores worse, it keeps the best one for returning, but it still refines from the newest, worse recipe.
>
> **Marcus:** Good eye. That's a design choice, not a bug, and the note doesn't discuss it. Refining from the regressed recipe can let you escape a local optimum. Refining from the best one keeps you from drifting further downhill. With a patience of two, you'll stop soon either way. But if I were extending it, I'd refine from the best so far. It's the same champion-challenger logic: the challenger always competes against the champion, not against the last loser.
>
> **Jess:** Last one. Exercise one, building the trading system VPC.
>
> **Marcus:** Quick recall. A slash twenty-six subnet. Usable addresses?
>
> **Jess:** Sixty-four minus the five AWS reserves, so fifty-nine. And a slash twenty-two is one thousand twenty-four minus five, one thousand nineteen.
>
> **Marcus:** And what keeps the private subnets private?
>
> **Jess:** No default route. The private route table only has the local routes, the route to headquarters through the virtual private gateway, and the S 3 prefix list route that the gateway endpoint adds automatically.
>
> **Marcus:** And notice that the gateway endpoint in that lab is exactly the mechanism we just used to keep the Fargate tasks off the internet. A route, not a firewall. You built that piece weeks before you needed it. That's how this course is designed. Let's wrap. Three takeaways.
>
> **Jess:** You first.
>
> **Marcus:** One. "The job succeeded" is not "the model is better." Once success is an event that triggers deployment, you need an evaluation gate between training and promotion. Compare challenger and champion on the same held-out data with metrics that respect class imbalance, because accuracy on fraud data is a trap.
>
> **Jess:** Two. Know exactly what each role and boundary does. The E C S execution role starts the task, and the task role is what your code can do. Gateway endpoints are routes, security groups trust replies, network A C Ls check them. And every place a version crosses a boundary, like Spark three point five training and Spark four point two serving, is a place your pipeline can break.
>
> **Marcus:** Three. Choreography is fine for two steps. Once ordering, branching, and retries matter, move the flow into an orchestrator and keep each run an acyclic graph, with the repetition living outside it. And make every step idempotent, because S 3 events, Lambda retries, and Glue reruns will all happen more than once eventually.
>
> **Jess:** And the think about it question?
>
> **Marcus:** Here it is. Real fraud labels arrive late. A transaction is only confirmed as fraud when a chargeback comes in, often thirty to sixty days later. So the data you retrain on each month has recent fraud mislabeled as legitimate, and any evaluation set built from last month will be wrong in the same way. Design the promotion gate for your pipeline under that constraint. What data do you compare challenger and champion on, what metric and margin do you require, and what new failure mode does your gate itself introduce? For example, does it get stuck on a stale champion while fraudsters change tactics?
>
> **Jess:** Ooh. So a stricter gate makes it safer and also slower to adapt. I'm not answering that today.
>
> **Marcus:** Good. Don't. Sit with it while you fix that stale dependencies list in your README. Thanks for listening to MS AI Daily.
>
> **Jess:** See you next time.
