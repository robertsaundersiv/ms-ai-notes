---
title: "MS AI Daily – 2026-10-19"
type: podcast
created: 2026-10-19
duration_min: 32.9
covers:
  - "[[AWS Migration Services Overview]]"
  - "[[AWS Data Transfer Services]]"
  - "[[AWS Well-Architected Tool]]"
  - "[[Enhancing Data Processing with Redshift, EMR, and Athena]]"
  - "[[Serverless Modernization]]"
  - "[[Application and Container Orchestration]]"
  - "[[Multi-Agent RAG]]"
  - "[[Penguin and Scientist Agents]]"
  - "[[Smolagents Framework]]"
  - "[[Marketing Director Prompt Library]]"
  - "[[Financial Controller Prompt Library]]"
  - "[[Large Language Models]]"
  - "[[Chain-of-Thought and ReAct]]"
  - "[[Task Decomposition]]"
tags:
  - podcast
  - review
---

# MS AI Daily – 2026-10-19

![[MS AI Daily - 2026-10-19.mp3]]

> [!abstract] In this episode
> The theme is the confident wrong answer. The episode opens with an Athena query that says Netflix's TV-PG catalog averages a release year of 1944. That's a CSV parsing bug, not dirty data. From there, Marcus and Jess cover the back half of the AWS architecture course: picking migration and transfer tools by doing the bandwidth math, why the Well-Architected Tool is a questionnaire and not a scanner, choosing between Redshift, EMR and Athena by workload shape, and when serverless, Step Functions and ECS on Fargate actually pay off. The review segments link Step Functions and the "LLM proposes, Python disposes" penguin design to the same rule: keep order and limits in deterministic layers.

## Segments
- **Cold open and agenda:** the 1944 Athena result, from [[Enhancing Data Processing with Redshift, EMR, and Athena]]
- **Deep dive: from migration to modernization**
  - *The three service groups; "built-in validation" means DMS validation and MGN test launches are available, not automatic; Emirates' low-risk-first phasing; 4 Rs vs AWS's current 7 Rs:* [[AWS Migration Services Overview]]
  - *Online vs offline math (100 TB: about 12 days at 1 Gbps, about 1 day at 10 Gbps); the conflicting 8 TB / 2 TB thresholds; Snow retirements; Direct Connect is a path rather than a tool, has lead time, and isn't encrypted by default; who validates and who doesn't:* [[AWS Data Transfer Services]]
  - *Six pillars, not five; the tool scores self-reported answers, so pair it with Config and Trusted Advisor evidence; Cox's alignment and buy-in, and what the $700K figure really compares:* [[AWS Well-Architected Tool]]
  - *Workload shapes (repeated BI, heavy ETL, ad hoc S3 SQL); MPP and columnar storage; EMR vs Glue; Athena cost depends on data layout (2 TB raw vs 50 GB Parquet); OpenCSVSerDe and sanity-checking implausible results:* [[Enhancing Data Processing with Redshift, EMR, and Athena]]
  - *Three serverless swaps; the Lambda GB-second worked example and when it flips; the 15-minute limit; why Aurora Serverless is the hardest swap:* [[Serverless Modernization]]
  - *Step Functions vs hand-chained Lambdas; static workflow vs agent; orchestration vs choreography; the two lecture corrections (launch type picks compute, not the OS; Fargate doesn't require EFS); the ceil(10,000/800) = 13 tasks example; ECS vs EKS:* [[Application and Container Orchestration]]
- **Rapid review:** [[Multi-Agent RAG]] (four roles, coverage 1 − 0.4³ = 0.936 vs correctness, the telephone game, surfacing conflicts), [[Penguin and Scientist Agents]] (LLM proposes, Python disposes; history logs intent rather than actual; the inverted rule table), [[Smolagents Framework]] (the framework owns the ReAct loop; docstrings are prompts; quadratic token cost), [[Marketing Director Prompt Library]] and [[Financial Controller Prompt Library]] (compute, don't ask; capacity gates; closed-list mapping gates; Tree-of-Thought budgeting)
- **Blast from the past:** [[Large Language Models]] (every answer is a sample, so deterministic layers enforce order; temperature 0 isn't a guarantee), [[Chain-of-Thought and ReAct]] (closed book vs open book; unfaithful CoT), [[Task Decomposition]] (product of step reliabilities; one verb, one output, one test; decompose where you can check, orchestrate where you need order)

> [!warning] Corrections and clarifications flagged in this episode
> - [[Chain-of-Thought and ReAct]] says CoT's "reasoning path is fixed once generation starts". More precisely, CoT can revise course as it generates, especially in reasoning models. What's fixed is the *information*: no new evidence enters. ReAct differs because outside observations can change the next step.
> - [[AWS Migration Services Overview]] (from the lecture) says migration services include "built-in validation". DMS has an optional data-validation feature that you must turn on. MGN's equivalent is test launches. Neither validates your data automatically.
> - [[AWS Migration Services Overview]] uses the course's "4 Rs". That's a simplification. AWS guidance currently lists seven (retire, retain, rehost, relocate, repurchase, replatform, refactor).
> - The episode repeats corrections your notes already make: the WA Tool has six pillars, not the video's five ([[AWS Well-Architected Tool]]); an ECS launch type picks compute, not the OS, and Fargate doesn't require EFS ([[Application and Container Orchestration]]); the 8 TB vs 2 TB transfer thresholds conflict and stand in for transfer time ([[AWS Data Transfer Services]]).

## Think about it
You're building a multi-agent RAG research assistant on AWS. Some specialists answer in two seconds, but the literature agent sometimes takes twenty minutes. Synthesis should run only after every required specialist finishes or times out. Should the coordination live in an LLM coordinator agent, in a Step Functions workflow, or be split between them? For each choice, what happens to retries, to cost, to the fifteen-minute Lambda limit, and to your ability to audit why the final answer said what it said?

> [!quote]- Transcript
> **Marcus:** Quick question to start the day, Jess. According to a SQL query in an official AWS course demo, what's the average release year of everything Netflix rates TV-PG?
>
> **Jess:** I'd guess something like twenty fifteen? Netflix's catalog skews pretty recent.
>
> **Marcus:** Nineteen forty-four.
>
> **Jess:** Nineteen forty-four. So Netflix is secretly a newsreel archive.
>
> **Marcus:** That's the answer Amazon Athena handed back, with full confidence, in the exercise solution. And the instructor's explanation was that the data was dirty, because people's names were showing up in the country column.
>
> **Jess:** Which sounds reasonable. Public datasets are messy.
>
> **Marcus:** It sounds reasonable, and it's probably wrong. Your own notes caught it. That CSV file has quoted fields with commas inside them, like cast lists and lists of countries. If you define the table with a plain comma delimiter, every one of those inner commas splits a field, and every column after it slides over by one. The data is fine. The parser is lying to you.
>
> **Jess:** So the query worked perfectly. It just averaged the wrong column.
>
> **Marcus:** Exactly. And that's today's theme. Across cloud migration, serverless design, and agents, systems rarely fail by throwing a nice clear error. They fail by giving you a confident, well-formatted, wrong answer. The professional skill is noticing.
>
> **Marcus:** Welcome to MS AI Daily. It's Monday, October nineteenth, twenty twenty-six. I'm Marcus.
>
> **Jess:** And I'm Jess. So what's on the board today?
>
> **Marcus:** Big AWS day. Your newest notes cover the back half of the architecture course. We'll start with the migration service map and the data transfer tools. Then the Well-Architected Tool, and the two modernization strategies it leads to: better data processing with Redshift, EMR, and Athena, and better application architecture with serverless, Step Functions, and containers on ECS and Fargate.
>
> **Jess:** And then back to agents?
>
> **Marcus:** Rapid review swings back to multi-agent RAG, your penguin simulation, smolagents, and two of your prompt libraries. Then blast from the past covers LLM fundamentals, chain-of-thought and ReAct, and task decomposition. That's a lot of services, so we won't do a catalog. We'll do decisions. Every service today answers a question like how big, how fast, how often, or who controls the order.
>
> **Marcus:** Let's start where the course does. Lesson one decided what to do with each workload, the R strategies like rehost and replatform. Lesson two is the toolbox that carries those decisions out. Jess, can you sort the toolbox into its three groups from memory?
>
> **Jess:** Assessment, migration, and data transfer. Assessment is Application Discovery Service, which figures out what you have and what depends on what. Migration is Migration Hub for tracking, DMS, the Database Migration Service, for databases, and MGN, the Application Migration Service, for lifting and shifting servers. And data transfer is DataSync, Transfer Family, the Snow devices, and Direct Connect.
>
> **Marcus:** Clean. Now what's the real difference between a migration service and a data transfer service? Not the list. The principle.
>
> **Jess:** Migration services move workloads, things that run. Transfer services move data, files and objects, and they're tuned for different sizes.
>
> **Marcus:** Right. And the lecture adds that migration services come with built-in validation. I want to put a small asterisk on that. DMS does have a data validation feature that compares rows between source and target, but you have to turn it on, and it adds time and load. MGN's version of validation is really test launches. You boot a test copy of the replicated server and check it works before cutover. That's valuable, but it isn't checksumming your data. So read built-in validation as validation tooling is available, not validation happens to you.
>
> **Jess:** So if I wrote DMS guarantees data integrity in a design doc...
>
> **Marcus:** Your reviewer should circle it in red. DMS gives you the means. You still own the proof. Which brings us to the Emirates case study. What was the headline?
>
> **Jess:** More than thirty business-critical apps from over two hundred fifty servers, in under a year, during COVID, with zero unplanned downtime. And they went region by region, starting with low-risk services.
>
> **Marcus:** The low-risk-first part is the lesson that transfers, and it's an organizational decision, not a product feature. Your notes also point out that zero unplanned downtime says nothing about planned downtime. It's an AWS case study. Good evidence the approach works, weak evidence about how painful it was.
>
> **Jess:** One thing I wanted to check. The course talks about four Rs. I've seen seven Rs elsewhere.
>
> **Marcus:** Both exist. AWS's own guidance currently lists seven, adding things like retain, relocate, and repurchase. Your course uses a smaller subset. That's a simplification, not an error, but know the longer list exists.
>
> **Marcus:** Now the fun one. Data transfer. Jess, you've got a hundred terabytes of imaging archives and a one gigabit per second internet link. Rough guess. How long to send it online?
>
> **Jess:** Let me try. A hundred terabytes is eight hundred terabits. At one gigabit per second, that's eight hundred thousand seconds, which is a little over nine days.
>
> **Marcus:** Good arithmetic. Now add reality. You won't get the full line rate. Your notes assume eighty percent utilization, which pushes it to about a million seconds, roughly eleven and a half days. Call it twelve.
>
> **Jess:** And a Snowball Edge job is roughly a week end to end. Shipping, loading, shipping back, importing.
>
> **Marcus:** So at one gig, the truck wins. Now give the same hundred terabytes a ten gigabit link.
>
> **Jess:** Divide by ten. A bit over a day. Online wins easily.
>
> **Marcus:** That's the whole lesson in two calculations. Now, the lecture gives you size rules instead. One video says use the Snow Family above eight terabytes and DataSync below. Another video says virtual transfer services apply once datasets are under two terabytes. Those two thresholds don't agree, and your notes caught it.
>
> **Jess:** So which one is right?
>
> **Marcus:** Neither, in the sense you'd want. They're both proxies for time, with an assumed bandwidth hidden inside them. Eight terabytes is a quick job on a fat pipe and a multi-day slog on a congested office line. For a quiz built from the overview video, expect eight terabytes. For a real design, compute the transfer time against your deadline and the bandwidth you can actually dedicate.
>
> **Jess:** And the Snow devices themselves. Snowcone is the small rugged one for edge sites and disaster recovery. Snowball Edge is the big one, terabytes to petabytes, with real compute on board.
>
> **Marcus:** Right. And your notes added an important caveat. AWS has been retiring Snow devices. Snowcone stopped taking new orders in twenty twenty-four. So check what's actually orderable before you put Snow in a plan. Learn the decision logic, offline versus online, one-time versus ongoing, push versus pull. Spec sheets for discontinued hardware make terrible flashcards.
>
> **Jess:** Okay, then DataSync, Direct Connect, and Transfer Family. Here's my mental model. DataSync is the moving van. Direct Connect is a private highway. Transfer Family is the loading dock where outside partners drop things off.
>
> **Marcus:** I like that, and it's mostly right. Where does the analogy break?
>
> **Jess:** Hmm. Maybe that the van can drive on the highway?
>
> **Marcus:** Exactly that. Direct Connect isn't a migration tool at all. It's network infrastructure. DataSync and DMS can run over it. So the answer is often not DataSync or Direct Connect, it's DataSync on Direct Connect. Direct Connect earns its keep when the hybrid period is long, because it improves the path everything else uses. And it has lead time. You request it, then AWS or a partner physically provisions a circuit. Teams that order it the week before cutover get a crash course in telecom timelines.
>
> **Jess:** Here's one I would have gotten wrong. A dedicated private line is encrypted, right? It's private.
>
> **Marcus:** That's the trap. Private is not the same as encrypted. Direct Connect is a dedicated path, but traffic over it isn't encrypted by default. If you're moving healthcare data, like Health Metrics in your course scenario, you add encryption. That could be a VPN running over Direct Connect, MAC security on supported connections, or plain TLS at the application layer. It's in your pitfalls table, and it's a compliance finding waiting to happen.
>
> **Jess:** And the related gotcha. DataSync validates the data it moves, but Transfer Family and Direct Connect don't.
>
> **Marcus:** Right. Transfer Family is a managed SFTP endpoint that lands files in S3 or EFS. It's perfect for the external lab that has sent results over SFTP for fifteen years and has no intention of changing. But you add checksums yourself.
>
> **Marcus:** So the workloads are in. Lesson three asks the next question. Now that you're here, is it any good? Enter the Well-Architected Tool. Jess, what does it actually do?
>
> **Jess:** You define a workload, answer questions about its architecture pillar by pillar, and it reviews your answers against AWS best practices. You get videos and documentation for each risk, a workload report, and an organization-wide dashboard. Beyond the lecture, it flags high-risk and medium-risk issues, you can save milestones to show progress, and you can add lenses, like the Migration Lens or the Serverless Lens.
>
> **Marcus:** Good. How many pillars?
>
> **Jess:** The lecture video says five. My notes say six.
>
> **Marcus:** Your notes are right and the video is out of date. Sustainability was added as the sixth pillar in late twenty twenty-one. The other five are operational excellence, security, reliability, performance efficiency, and cost optimization. If a quiz is built straight from that video, it might expect five. In the actual console, including the demo in your course repo, you'll see six.
>
> **Jess:** Here's what I assumed when I first read about it. The tool scans my account and finds the risks. Like a security scanner.
>
> **Marcus:** That's a very reasonable assumption from the name, and it's the most important thing to correct today. The Well-Architected Tool is fundamentally a structured questionnaire. It scores what you tell it. If a team answers optimistically, they get a clean report and keep every one of their risks.
>
> **Jess:** So it's a self-assessment with a nice dashboard.
>
> **Marcus:** A self-assessment with a nice dashboard and an excellent shared vocabulary. Which is why you pair it with evidence: Config rules, Trusted Advisor checks, real architecture diagrams. The questionnaire tells you where to look. Telemetry tells you what's there.
>
> **Jess:** Then why did Cox Automotive get so much out of it?
>
> **Marcus:** Because the value wasn't detection. It was alignment. They went from printed PDFs and spreadsheets to one process and one vocabulary across three hundred fifty engineering teams, and executives approved more investment in security and resilience. It's a communication instrument as much as a technical one.
>
> **Jess:** And the savings? Over seven hundred thousand dollars a year.
>
> **Marcus:** Read that one carefully. That's compared with running on-premises, and most of it came from migration and optimization work. The tool's contribution was prioritizing that work and getting it funded.
>
> **Jess:** And the logic of the lesson is review first, then modernize based on what the review finds.
>
> **Marcus:** Right. Adopting containers or Step Functions without a finding behind it isn't architecture. It's fashion with a monthly invoice.
>
> **Marcus:** Strategy one. Redshift, EMR, and Athena. I don't want you to memorize three definitions. I want you to think in workload shapes. Jess, give me the three shapes.
>
> **Jess:** Redshift is for repeated, low-latency business intelligence queries over curated warehouse data. EMR is for heavy transformation pipelines, especially existing Spark or Hadoop extract, transform, and load jobs at terabyte scale. And Athena is for ad hoc SQL over data that's already sitting in S3, like logs.
>
> **Marcus:** That's the framing. Why is Redshift fast at analytics?
>
> **Jess:** Two reasons. Massively parallel processing, so a query is split across many nodes, each working on a slice. And columnar storage, so if a query only touches three columns, you only read those three columns.
>
> **Marcus:** And columns compress well, because a column is full of similar values. Now, the overlap. Redshift Spectrum can query S3. Athena can run Spark. EMR has a serverless mode. The lines the lecture draws are fuzzier in practice, which is why thinking in workload shape outlasts thinking in product names.
>
> **Jess:** And EMR versus Glue, from lesson one?
>
> **Marcus:** Both run Spark. Glue is serverless. You submit a job and pay for processing time. EMR gives you a managed cluster with more frameworks, like Hive and Presto, and more tuning knobs. Simple managed ETL, Glue. An existing Hadoop estate that needs control and scale, EMR.
>
> **Jess:** Now Athena. It's serverless and you pay per query. So I don't really have to think about cost. It just scales.
>
> **Marcus:** Plausible, and it's exactly how teams get surprised by their bill. Athena charges by data scanned. Your notes use five dollars per terabyte as an illustrative price. So a two terabyte scan of raw logs costs what?
>
> **Jess:** Ten dollars per query.
>
> **Marcus:** Now store the same logs as Parquet, which is a columnar format, and partition them by date, so a query about last Tuesday only opens last Tuesday's files. Your notes estimate that scan drops to about fifty gigabytes.
>
> **Jess:** Which is about twenty-five cents. Forty times cheaper.
>
> **Marcus:** Same question, same answer, forty times cheaper. Serverless pricing means your data layout becomes a line item. So serverless doesn't mean you stop thinking about cost. It means cost moves from how many servers you run to how you shaped your data.
>
> **Jess:** And back to the cold open. The fix for nineteen forty-four is Athena's OpenCSV SerDe, short for serializer-deserializer, which understands quoted fields.
>
> **Marcus:** Or convert to Parquet and kill that whole class of problem. But the deeper lesson is about judgment. The instructor saw an implausible number and blamed the data. The better instinct is, implausible result, inspect the pipeline. TV-PG content averaging nineteen forty-four is a smoke alarm, not a fun fact. It's the same discipline as the data validation lesson from the migration module. You sanity-check results against what you know about the world.
>
> **Jess:** And the steps for Athena itself: point at the S3 data, set the query result location, also in S3, create the database and table, then query.
>
> **Marcus:** And the result location is the step the slide skipped and the demo tripped over. Forget it and nothing runs, which is honestly the friendliest failure we'll discuss today.
>
> **Marcus:** Strategy two. Improve the application architecture, with three techniques: serverless, application orchestration, and container orchestration. Serverless first. The lecture's analogy is wireless phones. You stop worrying about the wires.
>
> **Jess:** Which is cute, but the wires still exist. Somebody is still managing them.
>
> **Marcus:** Somebody else's pager goes off, yes. That's the deal. The lecture gives three swaps. An API served directly from EC2 becomes API Gateway. Short-lived functions running on EC2 become Lambda. And an RDS database with changing load becomes Aurora Serverless.
>
> **Jess:** What does API Gateway buy you beyond not running a server?
>
> **Marcus:** All the things people build by hand, badly. Throttling, authorization, caching, and monitoring become configuration.
>
> **Marcus:** Let's do your worked example, because it's a good one. Health Metrics has an appointment reminder job. It runs a million times a month, two hundred milliseconds each, with five hundred twelve megabytes of memory. Jess, walk me through the Lambda bill.
>
> **Jess:** Lambda bills compute in gigabyte-seconds, memory times duration. A million runs, times zero point two seconds, times half a gigabyte, is a hundred thousand gigabyte-seconds. At the illustrative rate, that's about a dollar sixty-seven. Plus twenty cents for the million requests. Call it a dollar eighty-seven a month.
>
> **Marcus:** Versus an always-on t3 medium instance at about thirty dollars a month. Roughly ninety-four percent cheaper. So, is serverless always cheaper?
>
> **Jess:** My gut says no, because you pay a premium per unit of compute. If the function were busy all the time...
>
> **Marcus:** Then you pay that premium around the clock, and a right-sized instance, maybe with a Savings Plan, wins. Serverless wins on spiky, event-driven work and loses on steady, compute-heavy work. The reminder job wins because it's idle almost all the time. Your notes call that the flip side of the worked example, and it's the part people forget.
>
> **Jess:** And there's the fifteen-minute limit.
>
> **Marcus:** A hard limit per invocation. If you have a forty-minute nightly cleanup script, Lambda isn't a drop-in. You break the job into steps coordinated by Step Functions, or run it as a scheduled Fargate task or a Glue job. Which is a nice bridge, because Step Functions is next.
>
> **Jess:** Before we move on, the Aurora Serverless swap seems like the easiest of the three. It's just a database that scales.
>
> **Marcus:** It's actually the hardest. Databases have connections, warm caches, scaling latency, and engine version support to worry about. And for a steady, flat load, provisioned capacity is often cheaper. Load test it before you commit. Databases are where the phrase drop-in replacement goes to retire.
>
> **Marcus:** Application orchestration. Step Functions. Jess, explain the lecture's example.
>
> **Jess:** A Lambda writes order logs to S3. The finance team wants to process them and load results into RDS, but the sales team has to process each log first and add its input. Step Functions guarantees the sales Lambda runs first, then the finance Lambda.
>
> **Marcus:** Now, why not just have the sales Lambda call the finance Lambda when it's done? Much less to set up.
>
> **Jess:** It would work... but the ordering is now hidden inside the sales team's code. And if finance fails, who retries? Does sales run again and duplicate its work?
>
> **Marcus:** Exactly. When you chain functions by hand, ordering, retries, and history get smeared across everyone's code. In Step Functions, the order, the retry policy with backoff, the catch-and-alert path, and the execution history all live in the state machine, defined in JSON using the Amazon States Language. Neither Lambda needs to know the other exists.
>
> **Jess:** This sounds a lot like the workflow versus agent distinction from the agentic course. Step Functions is basically a prompt chain where the steps are Lambdas.
>
> **Marcus:** That's a really good connection, and it mostly holds. A state machine is a fixed workflow. The developer decides the path at design time. That's the static decomposition from your task decomposition note. Where does the analogy break?
>
> **Jess:** Well, Step Functions has choice states, so it can branch. Doesn't that make it a bit agent-like?
>
> **Marcus:** It can branch, but only on rules you wrote. That's deterministic routing. An agent decides its own next step at runtime. And when order matters and has to be auditable, sales before finance, you don't want a model deciding. Your notes add a related distinction: orchestration, where one controller decides the order, versus choreography, where services just react to events, say through EventBridge. Orchestration wins when order and error handling matter. Choreography wins for loosely coupled fan-out.
>
> **Jess:** Okay, containers. The before picture is Docker on EC2, managed by hand. A registry on the instances, EBS volumes for storage, and a load balancer and auto scaling groups configured manually.
>
> **Marcus:** Effective and operationally exhausting. What's the after picture?
>
> **Jess:** Keep the load balancer. Images move into ECR, the Elastic Container Registry. ECS, the Elastic Container Service, runs the containers as tasks. Fargate provides serverless compute, so there are no instances to manage. And EFS, the Elastic File System, gives shared storage.
>
> **Marcus:** Good. Now, your notes flagged two lecture statements to correct, and I want to say them out loud, because they're exactly the kind of thing that ends up on a whiteboard in a design review. First, the lecture says the launch type is the configuration for the operating system. It isn't. The launch type chooses the compute infrastructure a task runs on: EC2 instances that you manage, or Fargate.
>
> **Jess:** And the second is that Fargate requires EFS.
>
> **Marcus:** It doesn't. Fargate tasks get ephemeral storage, twenty gibibytes by default, and you can expand it. You add EFS when containers need persistent or shared files, which happens to be true in the lecture's architecture. You can also attach EBS volumes to Fargate tasks now. Why does this correction matter in practice?
>
> **Jess:** Because if a team believes EFS is required, they'll bolt shared network storage onto everything, and pay for it, even where ephemeral storage or a real database is the right answer.
>
> **Marcus:** Exactly. And the opposite mistake is also in your pitfalls table: assuming a container's local storage persists. The task stops, the data's gone.
>
> **Jess:** So the ops team goes from configuring instances to declaring a service. This image, this much CPU and memory, this many tasks, this scaling policy. And ECS keeps that true.
>
> **Marcus:** That's the container version of the serverless shift. Declare the desired state and let the platform reconcile it. Quick math from your self-test. Target tracking at eight hundred requests per task, and a peak of ten thousand requests. How many tasks?
>
> **Jess:** Ten thousand over eight hundred is twelve point five. Round up, thirteen.
>
> **Marcus:** Always round up. And one more thing. Fargate removes servers, not architecture. You still size tasks, design subnets and security groups, and set health checks. A badly sized Fargate task can cost more than well-packed EC2 hosts.
>
> **Jess:** And ECS versus EKS?
>
> **Marcus:** ECS is AWS-native and simpler. EKS is managed Kubernetes, more portable, with a steeper learning curve. Health Metrics already ran Kubernetes, which is why lesson one moved them to EKS. Choosing Kubernetes for a three-container app is how you end up with more YAML than application code.
>
> **Marcus:** Alright, rapid review. Let's pivot to agents, and I'll keep asking you first. Multi-agent RAG. Four roles. Go.
>
> **Jess:** Specialized retrieval agents, each owning one data source and its tools, like a SQL agent or a PubMed agent. A retrieval coordinator that analyzes the query and delegates, often in parallel. A synthesis agent that merges the mixed results into one answer. And optional gap analysis that spots what's missing and sends a targeted follow-up to the right specialist.
>
> **Marcus:** Good. And it maps onto a pattern you already know.
>
> **Jess:** Orchestrator-workers. The coordinator is the orchestrator, the specialists are workers, and the synthesis agent is the synthesizer.
>
> **Marcus:** Now the gotcha. Your notes have the coverage math. If a fact lives in each of three independent sources with probability point six, querying all three finds it with probability one minus point four cubed.
>
> **Jess:** Point nine three six. Versus point six from a single source.
>
> **Marcus:** That's the real argument for multi-agent RAG. Here's the catch. Coverage isn't correctness. More sources means more chances to retrieve something wrong or contradictory. And each specialist adds interpretation before the synthesizer sees anything, which is an LLM transformation at every hop. It's the telephone game. So the synthesis agent should surface conflicts rather than average them, and every claim should carry its source ID all the way through.
>
> **Jess:** Like the CRISPR example. A press release claiming success, and a trial registry showing a Phase One trial with no published results. You don't blend those into promising results. You flag the press release as unverified.
>
> **Marcus:** Exactly. And notice the echo with today's AWS material. Fan out, wait, synthesize. That's also the shape of a parallel state in Step Functions. Hold that thought.
>
> **Marcus:** Penguins. Your penguin and scientist simulation. What's the one-line lesson?
>
> **Jess:** The LLM proposes and Python disposes. The model states an intent through a tool call. Then plain Python reads that intent from the step log, clamps it to the real limits, and applies the actual state change.
>
> **Marcus:** And the coordinator in that simulation isn't an LLM at all.
>
> **Jess:** Right, it's a plain Python loop. Hub and spoke, with code in the hub.
>
> **Marcus:** Which is the Step Functions philosophy in miniature. Deterministic control where order and limits matter. Now, your own code review found several bugs. Which one is sneakiest?
>
> **Jess:** I think the history log. It records what the scientist intended to give, not what was actually given after clamping. So if the scientist asks to give five food and only two remain, history says five, and every future decision reads a false history.
>
> **Marcus:** That's the one. It's the agent version of the Well-Architected problem: a record of what someone said, rather than what actually happened. Log both the intended and the actual. And my favorite bug: the penguin rule table is inverted. Hungry penguins fend for themselves, and well-fed penguins ask for help.
>
> **Jess:** Which is honestly a very realistic penguin economy.
>
> **Marcus:** And the model followed that prompt perfectly. The prompt was wrong. Agents behaving exactly as badly as their design predicts.
>
> **Marcus:** Smolagents. What does the framework actually do for you?
>
> **Jess:** It runs the reason, tool call, observe loop. You decorate Python functions as tools, hand them and a model to a ToolCallingAgent, and the framework parses the model's output, executes the tools, and feeds results back until it gets a final answer, with a step cap so it can't loop forever.
>
> **Marcus:** And the gotcha about docstrings?
>
> **Jess:** The docstring is part of the prompt. The framework builds the tool schema from the name, the type hints, and the docstring, so a vague docstring means wrong tool choices and malformed arguments. Same bug as the penguin find-food tool, whose docstring says it returns zero to five food when fishing actually returns two to seven.
>
> **Marcus:** Nice cross-reference. And the cost model: every step resends the whole history, so total input tokens grow quadratically with the number of steps. Step caps are a cost control, not just a safety net.
>
> **Marcus:** Last, your prompt libraries for Wi-Fiber, the Marketing Director and the Financial Controller. What design idea ties them together?
>
> **Jess:** Compute, don't ask. Do the math in the spreadsheet or the ledger, and give the model the results. The model classifies, structures, and writes. And gates everywhere. My favorite on the marketing side was capacity-aware acquisition targeting. You gate every tower sector as open, limited, closed, or opening soon before you spend money selling into it.
>
> **Marcus:** Because selling into a congested sector is buying churn on an installment plan. That's a logic gate turning a network constraint into a marketing constraint. And on the finance side?
>
> **Jess:** The category mapping prompt uses a closed-list gate. The model can only map to general ledger accounts and cost centers from your list, never invent one, and anything that might be capital versus operating expense goes to review. And budget prioritization uses tree-of-thought. Build three allocation approaches separately, prune the ones that break constraints, then recommend.
>
> **Marcus:** Notice the closed list is the same move as the scientist clamping food. Let the model choose, but only from a space you've already made safe.
>
> **Marcus:** Blast from the past. Let's go back to the start of the program. Large language models. Jess, give me the one-sentence mental model from your notes.
>
> **Jess:** An LLM is a probabilistic reasoning engine with no memory, no senses, and no hands. Agentic AI adds memory through stores, senses through retrieval and observations, hands through tools, plus a control loop.
>
> **Marcus:** And the property that explains half of today's material?
>
> **Jess:** Every answer is a sample. The model produces a probability distribution over the next token and samples from it. So the same prompt can give different outputs, and you evaluate across many runs.
>
> **Marcus:** Here's why I picked that one. Every deterministic layer we praised today, the Step Functions state machine, the Python clamp in the penguin simulation, the closed-list gate, exists because of that sentence. You don't put a sampler in charge of making sure sales runs before finance.
>
> **Jess:** And the one I always need reminding of. Temperature zero isn't a guarantee of determinism either. Batching and floating point behavior on GPUs can still change outputs.
>
> **Marcus:** Right. Design for variation either way. Chain-of-thought and ReAct. Quick contrast?
>
> **Jess:** Chain-of-thought reasons through intermediate steps using what the model already has. ReAct alternates reasoning with actions. Reason, act, observe, repeat. So it can gather new information as it goes.
>
> **Marcus:** There's one line in that note I want to sharpen. It says that with chain-of-thought, the reasoning path is fixed once generation starts. That's not quite the right way to put it. Chain-of-thought is generated token by token, and models can revise course in the middle of their reasoning, especially reasoning models. What's fixed is the information. No new evidence comes in. ReAct's real difference is that observations from the outside world can change the next step.
>
> **Jess:** So the distinction is closed book versus open book, not rigid versus flexible.
>
> **Marcus:** That's a great way to say it. And the other caveat in your note stands: chain-of-thought can be unfaithful. The visible reasoning isn't necessarily what produced the answer. Treat it as evidence, not as an audit log. Which echoes the Well-Architected lesson. A narrative is not telemetry.
>
> **Jess:** And smolagents' ToolCallingAgent is basically ReAct in a box.
>
> **Marcus:** It is. And the note's point that RAG can be one tool inside a ReAct loop is the seed of multi-agent RAG. Retrieval stops being a one-shot preprocessing step and becomes an action someone chooses to take.
>
> **Marcus:** Last one. Task decomposition. What's the key formula?
>
> **Jess:** End-to-end success for steps in series is the product of each step's success rate. So decomposition only helps if each step gets enough more reliable to pay for the extra steps. Three steps at point nine five beats a single prompt at point seven. Six steps at point nine three loses to it.
>
> **Marcus:** About point eight six versus about point six five. And the definition of a good subtask?
>
> **Jess:** One verb, one output, one success test.
>
> **Marcus:** Now look at the Step Functions example through that lens. Sales processes the log, finance loads the database. One verb, one output each, and each can be retried independently. Decomposition and orchestration are the same idea at two layers. Decompose where you can check, orchestrate where you need order.
>
> **Marcus:** Let's land it. Three takeaways.
>
> **Jess:** Number one?
>
> **Marcus:** Do the math before you pick the service. Transfer time is data over effective bandwidth. Athena cost is data scanned. Lambda cost is gigabyte-seconds. Agent reliability is the product of step reliabilities, and agent cost grows with every resent token. Size thresholds like eight terabytes are someone else's math with assumptions you can't see.
>
> **Jess:** Number two. Put order, limits, and enforcement in deterministic layers, and let the flexible components decide only what they have to. Step Functions owns the ordering, ECS owns the desired state, Python clamps the penguin food, and closed-list gates bound the model's choices.
>
> **Marcus:** And number three. A plausible output is not a verified output. An average release year of nineteen forty-four, a history log full of intentions, a self-reported architecture review, an unfaithful chain of thought, a private line mistaken for an encrypted one. They all look fine on the surface. Build the check that would catch them.
>
> **Marcus:** Here's your think-about-it question. You're building a multi-agent RAG research assistant on AWS. Some specialists answer in two seconds, but the literature agent sometimes takes twenty minutes, and synthesis should only run after every required specialist either finishes or times out. Do you put that coordination in an LLM coordinator agent, in a Step Functions workflow, or split it between them? And for each choice, what happens to retries, to cost, to the fifteen-minute Lambda limit, and to your ability to audit why the final answer said what it said?
>
> **Jess:** That's a good one. I already want to argue with myself about it.
>
> **Marcus:** Good. Argue on paper. That's it for today's MS AI Daily. I'm Marcus.
>
> **Jess:** And I'm Jess. Check your parsers, and we'll see you tomorrow.
