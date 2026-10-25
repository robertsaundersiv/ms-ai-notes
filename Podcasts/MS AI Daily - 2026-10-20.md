---
title: "MS AI Daily – 2026-10-20"
type: podcast
created: 2026-10-20
duration_min: 34.6
covers:
  - "[[Application and Container Orchestration]]"
  - "[[Serverless Modernization]]"
  - "[[Enhancing Data Processing with Redshift, EMR, and Athena]]"
  - "[[AWS Well-Architected Tool]]"
  - "[[AWS Migration Services Overview]]"
  - "[[AWS Data Transfer Services]]"
  - "[[Orchestrating Agent Activities]]"
  - "[[Multi-Agent State Coordination]]"
  - "[[Exercise 1 - Build the Network - How To]]"
  - "[[Step 2 - Network Connectivity - How To]]"
  - "[[Financial Controller Prompt Library]]"
  - "[[Structured Outputs]]"
  - "[[Tool Descriptions in Agentic Systems]]"
  - "[[Agentic RAG]]"
tags:
  - podcast
  - review
---

# MS AI Daily – 2026-10-20

![[MS AI Daily - 2026-10-20.mp3]]

> [!abstract] In this episode
> Yesterday's episode mapped the AWS modernization services. Today's tests them with one question: what happens when a step runs twice? The cold open copies a retry block onto the finance step of the Step Functions example, and the finance database ends up holding four copies of Tuesday's orders. From there, Marcus and Jess follow the retry through ECS reconciliation, Lambda's automatic async retries, pay-per-scan Athena refreshes, append versus overwrite in Glue, Well-Architected evidence, live-database migration with DMS, and the 60 TB shared-link transfer problem. The agent segments connect the same rule to rollback-and-retry, correlated failures in structured outputs, retry-safe tool design, and reviewers who check their own work.

## Segments
- **Cold open and agenda:** a retry policy that quadruples revenue, from [[Application and Container Orchestration]]
- **Deep dive: follow the retry**
  - *MaxAttempts counts retries, not tries (4 runs; waits of 5, 10, 20 s); "exactly-once" describes the workflow, not your side effects; idempotency keys (S3 key plus version or ETag); retry vs catch vs soft failures; choreography means at-least-once, unordered events; an ECS service as a reconciliation loop, so tasks must be disposable; quick recall of the launch-type and EFS corrections:* [[Application and Container Orchestration]]
  - *Lambda retries async invocations twice by default; the 3M-invocation cost (about $5.60) and what retries add; chunking the 40-minute job with checkpoints; cold starts and provisioned concurrency; what not to move to serverless:* [[Serverless Modernization]]
  - *Health Metrics design: Athena for raw logs, Redshift for dashboards, Glue or EMR in between; $45 vs $2.25 a month; every refresh is a new scan; overwrite-by-partition is idempotent and append isn't:* [[Enhancing Data Processing with Redshift, EMR, and Athena]]
  - *Answering the note's question on optimistic self-assessment: evidence links, outside reviewers, Config and Trusted Advisor, milestones, game days; "none of these" counts as a risk:* [[AWS Well-Architected Tool]]
  - *Discovery before migration; live databases go through DMS (full load plus change data capture), not DataSync; DataSync re-runs copy only changes; Transfer Family partners can resend files; the 60 TB shared-link calculation (about 7 days at full use, about 12 days off-peak only); chain of custody and long retry times for physical transfer; DataSync throttling:* [[AWS Migration Services Overview]], [[AWS Data Transfer Services]]
- **Rapid review:** [[Orchestrating Agent Activities]] (travel-booking design; reads can be retried freely, irreversible writes need gates; the demo's fake parallelism), [[Multi-Agent State Coordination]] (rollback redoes the whole operation; livelock, backoff and jitter; 1.7% vs 39% conflict odds; MBCC means MVCC), [[Exercise 1 - Build the Network - How To]] (59 and 1,019 usable addresses; /22 alignment; isolation by routing; gateway vs interface endpoints; a VGW alone is not a VPN), [[Step 2 - Network Connectivity - How To]] (no cross-Region SG references; create flow logs before testing; a Region inconsistency), [[Financial Controller Prompt Library]] (operations-gate break-even; plan-then-solve as a human checkpoint; segregation of duties)
- **Blast from the past:** [[Structured Outputs]] (shape, not truth; 0.999 only if failures are independent), [[Tool Descriptions in Agentic Systems]] (declare retry safety; the runtime enforces it; instructive errors turn blind retries into corrected ones), [[Agentic RAG]] (every retry must change something; stop conditions; the reflector as self-assessment; self-reinforcing loops)

> [!warning] Corrections and clarifications flagged in this episode
> - [[Step 2 - Network Connectivity - How To]] is internally inconsistent. The scenario and route tables put Account B in **us-west-2**, but section 8a ("Your Regions") says Account B is **us-west-1** (`vpc-04409d739c492c202`) and creates the flow log and log group there. Log groups are Regional, so use whichever Region you actually built in and make the note match.
> - [[AWS Data Transfer Services]] lists S3, EFS and FSx for Windows File Server as DataSync targets. That's from the lecture and is **incomplete, not wrong**: DataSync also supports other FSx file systems, such as FSx for Lustre and FSx for NetApp ONTAP.
> - [[AWS Migration Services Overview]] maps same-engine DMS moves to replatform and engine changes to refactor. That's **ambiguous, not wrong**. AWS guidance often calls an engine change (e.g. Oracle to Aurora PostgreSQL) a replatform. Plan for schema conversion and code changes whichever label you use.
> - Clarification for [[Application and Container Orchestration]]: in the Amazon States Language, `MaxAttempts: 3` means up to **three retries after the first attempt**, so four runs in total. Step Functions' exactly-once guarantee for Standard workflows covers state transitions, not your Lambda's side effects when it's retried.
> - The episode briefly repeats corrections your notes already make: six Well-Architected pillars, not five; launch type picks compute, not the OS; Fargate doesn't require EFS; "purely one pattern" should read "rarely purely one pattern" ([[Orchestrating Agent Activities]]); "MBCC" means MVCC ([[Multi-Agent State Coordination]]); plain function calling doesn't guarantee format, only strict mode does ([[Structured Outputs]]).

## Think about it
You're building a customer-support agent on AWS. It has an `issue_refund` tool backed by a Lambda function, and a Step Functions workflow runs the agent's approved actions with a retry policy. One night the Lambda calls the payment provider, the provider accepts the refund, and the Lambda times out before the response comes back. Step Functions retries. Where should idempotency live: the agent's prompt, the tool description, the Lambda, the state machine, the database, or the call to the payment provider? What breaks if it lives in only one of those places? And what would you log so a human reviewing the incident can tell "refunded once" from "refunded twice"?

> [!quote]- Transcript
> **Marcus:** Jess, picture this. You take the Step Functions workflow from your notes, the one where sales processes the order logs first and then finance loads them into the database. The sales step already has a nice retry block. Three attempts, exponential backoff. So, being a responsible engineer, you copy that same retry block onto the finance step.
>
> **Jess:** Sounds responsible. Retries are good. Transient failures happen.
>
> **Marcus:** Tuesday night, the finance Lambda writes all of Tuesday's orders into the database. Then, on its last line, it tries to post a "done" message to a chat channel, and that call fails. The function throws an error. What does Step Functions do?
>
> **Jess:** It sees a failed task, so it waits a few seconds and runs the finance Lambda again.
>
> **Marcus:** And what does the finance Lambda do the second time?
>
> **Jess:** Oh no. It inserts all of Tuesday's orders again. And if the chat service is still down, it fails again, and the workflow retries again.
>
> **Marcus:** Wednesday morning, the finance team discovers that revenue roughly quadrupled overnight. Champagne for about eleven minutes, and then an incident review.
>
> **Jess:** So the retry policy did exactly what it was told. The bug is that the step wasn't safe to repeat.
>
> **Marcus:** That's today's whole episode in one sentence. A retry is a promise that doing something twice is harmless. And that promise shows up everywhere in your notes, in cloud migration, in serverless design, in multi-agent coordination, in retrieval, in structured outputs. So today we're going to follow the retry.
>
> **Marcus:** Welcome to MS AI Daily. It's Tuesday, October twentieth, twenty twenty-six. I'm Marcus.
>
> **Jess:** And I'm Jess. We did a big tour of this AWS material yesterday, so what's different today?
>
> **Marcus:** Yesterday was the map. Which service answers which question. Today is the stress test. For each piece of the architecture, we ask what happens when something fails and gets tried again, and where the single source of truth lives. We'll start with Step Functions and ECS, then serverless, then the data services, the Well-Architected review, and finish the deep dive with migration and data transfer.
>
> **Jess:** Then rapid review?
>
> **Marcus:** Rapid review covers agent orchestration, multi-agent state coordination, two of your networking labs, and the Financial Controller prompt library. Blast from the past brings back structured outputs, tool descriptions, and agentic RAG, and every one of them has a retry story hiding in it.
>
> **Marcus:** Let's start with the cold open. Your notes have the state machine written in the Amazon States Language. The sales step has a retry block with an interval of five seconds, a max attempts of three, and a backoff rate of two. Jess, how many times can the sales Lambda run, in total, for one order log?
>
> **Jess:** Max attempts three. So three times.
>
> **Marcus:** That's the natural reading, and it's off by one. Max attempts counts retries, not tries. So the original attempt, plus up to three retries. Four runs. And the waits between them?
>
> **Jess:** Five seconds, then the backoff rate doubles it, so ten, then twenty. So the last attempt starts about thirty-five seconds after the first failure, plus however long each run took.
>
> **Marcus:** Right. That off-by-one matters when the step costs money or has side effects. Now, here's a question I want you to reason through. Step Functions standard workflows advertise exactly-once execution. Doesn't that mean the duplicate inserts in the cold open can't happen?
>
> **Jess:** I would have said yes. If it's exactly once, it's exactly once.
>
> **Marcus:** The exactly-once promise is about the workflow itself. Each state transition is recorded once and the execution history is consistent. It is not a promise about the side effects of your code once you've told the workflow to retry. You asked for a second invocation, and you got one. The state machine is honest. Your Lambda wasn't idempotent.
>
> **Jess:** Idempotent meaning running it twice leaves the world in the same state as running it once.
>
> **Marcus:** Exactly. So how would you fix the finance step?
>
> **Jess:** A few options. Split the chat notification into its own state, so a chat failure retries only the notification. And make the database load safe to repeat. Maybe use the S3 object key of the order log as an idempotency key, with a unique constraint, so a second insert for the same log is rejected or turned into an update.
>
> **Marcus:** Both good. The first one is the orchestration fix: give each side effect its own state, so failures are scoped. The second is the data fix, and it's the one that actually protects you, because there are other ways to get a duplicate invocation. One refinement. If order logs can be rewritten, use the object key plus its version or its entity tag, so a corrected file counts as new work, not a duplicate.
>
> **Jess:** This feels very close to what we did in the multi-agent coordination lesson. A conditional write that only succeeds if the world is still what you expected.
>
> **Marcus:** Hold that thought, because it comes back in rapid review. Now, one more Step Functions idea. Retry handles errors that are thrown. The catch block handles errors that survive the retries, and routes them to an alert. What kind of failure does neither of those catch?
>
> **Jess:** A Lambda that doesn't throw. It finishes successfully, but its output is wrong.
>
> **Marcus:** Right. If the sales Lambda misparses a log and returns well-formed garbage, Step Functions marks the step green and hands the garbage to finance. Your agent notes call that a soft failure. Retries are for hard failures. Soft failures need validation, a check on the content, not the exit code.
>
> **Jess:** So the green checkmark in the console means the step ran, not that it was right.
>
> **Marcus:** Put that on a sticky note. Now, your notes also contrast orchestration with choreography. In orchestration, one controller decides the order. In choreography, services react to events, for example through EventBridge. When you move from orchestration to choreography, what happens to our retry problem?
>
> **Jess:** I'd guess it gets worse, because there's no single controller tracking what already happened.
>
> **Marcus:** It does. Event delivery in those systems is typically at least once, and ordering isn't guaranteed. So every subscriber has to tolerate seeing the same event twice, or seeing an old event after a newer one. Your multi-agent coordination note says the same thing about state broadcasting: subscribers should be idempotent, and events should carry versions. Choreography doesn't remove the coordination problem. It distributes it to every consumer.
>
> **Jess:** Okay, containers. The ECS piece. Where's the retry in that?
>
> **Marcus:** It's hiding in the word service. When you declare an ECS service, you say: this image, this much CPU and memory, this many tasks, this scaling policy. If a task dies, what does ECS do?
>
> **Jess:** It starts a replacement to get back to the desired count.
>
> **Marcus:** So ECS is a reconciliation loop. It keeps retrying reality until reality matches your declaration. Which means every task must be?
>
> **Jess:** Disposable. Nothing important can live only inside the task, because the replacement starts fresh.
>
> **Marcus:** Right. Your notes list the pitfall: assuming containers keep local data. A Fargate task has ephemeral storage, and when it stops, that storage goes with it. Persistent or shared files go to EFS, or better, state goes into a real data store. Quick one, since you heard the correction yesterday. Does Fargate require EFS?
>
> **Jess:** No. Fargate has its own ephemeral storage. EFS is for when you need persistence or sharing. The lecture overstated it.
>
> **Marcus:** Good. And the launch type?
>
> **Jess:** Chooses the compute the task runs on, EC2 that you manage or Fargate. Not the operating system.
>
> **Marcus:** Perfect. Let's move to serverless, because Lambda has its own retry behavior that surprises people. When something invokes a Lambda function asynchronously, say an S3 event, and the function throws an error, Lambda itself retries. By default, twice.
>
> **Jess:** Wait. So in the cold open, if S3 events were invoking the finance Lambda directly, instead of going through Step Functions, I could get duplicates without writing any retry policy at all?
>
> **Marcus:** Yes. The platform retries for you, which is helpful right up until it isn't. This is why the serverless world says: assume at-least-once, design for idempotency. Event-driven architecture, which the lecture lists as one of the three benefits of serverless, comes with that obligation attached.
>
> **Jess:** The lecture's three benefits were automatic scaling with load, paying only for what you use, and event-driven workflows without always-on servers.
>
> **Marcus:** Right. Now let's do your self-test cost question, because it connects to something important about retries. A function runs three million times a month, a hundred milliseconds each, with one gigabyte of memory. Walk me through it.
>
> **Jess:** Three million times a tenth of a second times one gigabyte is three hundred thousand gigabyte-seconds. At about one point six seven times ten to the minus five dollars per gigabyte-second, that's about five dollars. Plus three million requests at twenty cents per million, sixty cents. About five sixty a month.
>
> **Marcus:** Good. Now suppose ten percent of invocations fail transiently and get retried once. What's the new bill?
>
> **Jess:** Roughly ten percent more. About six dollars.
>
> **Marcus:** Fine at this scale. But notice the shape. In serverless, cost is per request, so every retry is a line item. Your notes make the same point about chatty function-to-function calls. Architecture now directly sets the bill. A retry storm in a pay-per-request system is a billing event as well as a reliability event.
>
> **Jess:** What about the fifteen-minute limit? The note's design question had a forty-minute nightly cleanup script.
>
> **Marcus:** Right. Not a fit for one Lambda. You split it into steps with Step Functions, or run it as a scheduled Fargate task or a Glue job. Here's the retry angle. If you split it into, say, four ten-minute chunks, what do you need between chunks?
>
> **Jess:** Checkpoints. Some record of which chunk finished, so if chunk three fails, a retry restarts chunk three, not the whole forty minutes.
>
> **Marcus:** That's durable state, which your orchestrating-agents note brings up too. A long workflow should resume after a crash, not restart. And it only works if each chunk is idempotent, because chunk three might have half-finished before it failed.
>
> **Jess:** And cold starts? The pitfalls table mentions them.
>
> **Marcus:** When a function hasn't run for a while, the first invocation pays extra latency to initialize. For a reminder job, nobody notices. For a latency-sensitive API path, you can use provisioned concurrency, which keeps instances warm, and which you pay for whether or not they're used. That's a nice irony. The fix for serverless's cold start is a little bit of server.
>
> **Jess:** Your notes ask which Health Metrics component I would not move to serverless. I'd say anything steady and compute-heavy. And maybe the main database, at least not without load testing.
>
> **Marcus:** That's what I'd say too. Steady, dense work is cheaper on right-sized instances with a Savings Plan. And your note calls Aurora Serverless the hardest swap: connections, scaling latency, engine-version support. A database is where the confident slide deck meets the load test.
>
> **Marcus:** Now the data services. Instead of definitions, let's do the design question from your notes. Health Metrics wants daily dashboards, plus occasional deep dives into raw device logs. Which services, and why?
>
> **Jess:** Raw device logs land in S3. The deep dives are occasional and ad hoc, so Athena, directly on S3, pay per query. The dashboards run every day, repeatedly, and need to be fast, so Redshift, over curated tables.
>
> **Marcus:** And how does the data get from raw logs to curated tables?
>
> **Jess:** A transformation job. Glue if it's simple managed Spark, EMR if they have an existing Spark or Hadoop pipeline or need more control.
>
> **Marcus:** Good. That's a classic lake-plus-warehouse design. And it avoids one of the pitfalls in your notes. What happens if you skip Athena and load everything into Redshift?
>
> **Jess:** You pay to load and store data that might be queried once. Redshift is for repeated low-latency queries over curated data.
>
> **Marcus:** Right. Now the cost question from your self-test. A daily Athena query scans three hundred gigabytes of raw JSON, at an illustrative five dollars per terabyte scanned.
>
> **Jess:** Point three terabytes times five dollars is a dollar fifty per day. Times thirty, forty-five dollars a month. And if converting to Parquet and partitioning cuts the scan to fifteen gigabytes, it's seven and a half cents a day, two dollars twenty-five a month. A ninety-five percent reduction.
>
> **Marcus:** Now the retry angle. A dashboard tile times out in the browser, and a frustrated analyst hits refresh five times. On Athena, what did that cost?
>
> **Jess:** Five more scans. Each refresh is a new query, so it's billed again. Unless something caches the result.
>
> **Marcus:** Right. Athena does have an option to reuse recent results for identical queries, and dashboards usually sit behind a cache anyway. But the principle holds. In a pay-per-scan system, a retry isn't free, and the cost of the retry depends on your data layout. Which is why partitioning and columnar formats are a reliability concern as well as a cost concern. Smaller scans finish faster and time out less.
>
> **Jess:** Here's something I'm not sure about. Is the Glue job that builds the curated tables safe to retry?
>
> **Marcus:** Great question. What do you think?
>
> **Jess:** It depends how it writes. If it appends to the curated table, a retry could double-count a day. If it overwrites the partition for that day, re-running it gives the same result.
>
> **Marcus:** That's exactly the distinction. Overwrite-by-partition is idempotent. Append is not, unless you deduplicate. Data engineers learned this lesson so many times that it's practically a rite of passage. And it's the same lesson as the cold open, in a different costume.
>
> **Jess:** And I suppose MPP and columnar storage aren't changed by any of this. Redshift is still fast because work is split across nodes and it reads only the columns a query needs.
>
> **Marcus:** Right, and columns compress well. Those are still the two features to remember. The retry lens just tells you where the hazards are in the pipeline that feeds it.
>
> **Marcus:** So where would a team discover that their pipelines aren't idempotent, before the incident review?
>
> **Jess:** In theory, the Well-Architected review. The reliability pillar.
>
> **Marcus:** In theory. Yesterday we established the Well-Architected Tool is a structured questionnaire, not a scanner. Your notes end with a discussion question I want to actually answer today. How would you prevent optimistic self-assessment across fifty teams?
>
> **Jess:** First thought: require evidence for answers. If a team ticks "we handle failures with retries and idempotency," they link to the design doc or a test that proves it.
>
> **Marcus:** Good. What else?
>
> **Jess:** Have someone outside the team run or review the answers. And compare the answers against things that are measured, like AWS Config rules or Trusted Advisor findings.
>
> **Marcus:** All three are right. I'd add two. Saved milestones, so a team's answers are compared to their own previous review, and a sudden jump from many high-risk issues to none prompts a question. And game days, which the Cox Automotive case study mentions. You don't ask whether the finance step is safe to retry. You kill it mid-run on purpose and look at the database.
>
> **Jess:** So the review tells you where to look, and the game day tells you what's true.
>
> **Marcus:** Exactly. And one detail from the console walkthrough in your notes that people miss: answering "none of these" on a question counts as a risk. The tool rewards honesty, if you let it. Oh, and the current framework has six pillars, including sustainability. Retry storms, by the way, show up under that one too. Burning compute on duplicate work is waste.
>
> **Jess:** Okay, I want to apply the retry lens to the migration material, because that seems like the place where repeating something could really hurt.
>
> **Marcus:** It is. Let's start with the first service in the map. Application Discovery Service. Why does the course put assessment before everything else?
>
> **Jess:** Because it maps dependencies. If you migrate a server without knowing what calls it, the cutover breaks things you didn't know existed.
>
> **Marcus:** Right. And in our retry language, discovery tells you which workloads are safe to move, test, roll back, and move again, and which ones have hidden partners that will notice. Now, here's a scenario. Your team needs to move a live on-premises database that's still taking writes. Someone suggests DataSync, because it's fast and it validates data. What's wrong with that?
>
> **Jess:** DataSync moves files. If you copy a live database's files, you get an inconsistent snapshot, and the writes that happen during the copy are lost. Your notes list that exact pitfall. Use DMS for databases.
>
> **Marcus:** And DMS handles a live database how?
>
> **Jess:** It does a full load, and then ongoing replication, capturing changes as they happen, until you're ready to cut over.
>
> **Marcus:** Right. Change data capture. The source keeps running, the target catches up, and the cutover window shrinks to the final sync. Now, DataSync. If you run the same DataSync task twice on a file share, do you get two copies of everything?
>
> **Jess:** I'd assume you'd at least re-copy everything.
>
> **Marcus:** It's smarter than that. On later runs, DataSync compares the source and destination and transfers what changed, and it verifies the data. That's what makes it good for one-time migration followed by ongoing sync. Re-running it is designed to be safe. That's idempotency as a product feature.
>
> **Jess:** And Transfer Family? Partners push files over SFTP.
>
> **Marcus:** Which means the partner decides when to retry. If their upload script times out and resends, you get the same file twice in S3. Transfer Family doesn't validate your data automatically, so you add checksums, and your downstream processing has to recognize a file it already processed. Same idempotency key idea as the cold open.
>
> **Jess:** Let me try the open discussion question from the data transfer note. Health Metrics has sixty terabytes of imaging archives and a one gigabit per second link that's shared with clinics during business hours.
>
> **Marcus:** Go.
>
> **Jess:** Sixty terabytes is four hundred eighty terabits. At eighty percent of one gigabit, that's six hundred thousand seconds, almost seven days, if I could use the link around the clock.
>
> **Marcus:** But?
>
> **Jess:** But I can't, because clinics need it during the day. If I only get, say, fourteen off-peak hours a day, that's about fifty thousand seconds a day, so roughly twelve days. And a Snowball Edge job is about a week end to end. So Snow looks better, if the device is still orderable.
>
> **Marcus:** Nicely done. And notice the variable that changed the answer. Not the data size, the usable bandwidth. That's why the lecture's size thresholds, eight terabytes in one video and two terabytes in another, can't be the real rule. Now, what does physical transfer add that online transfer doesn't, for healthcare data specifically?
>
> **Jess:** Chain of custody. Someone has to document who handled the device and when. The devices are encrypted and tamper resistant, but the process still has to be auditable.
>
> **Marcus:** Right. And if a device is lost or damaged in shipping, what's your retry?
>
> **Jess:** Order another one and copy again. Which costs another week.
>
> **Marcus:** So the offline option has a long retry time. That's a real input to the decision. One more refinement. DataSync can throttle its bandwidth, so a middle path is DataSync running at full speed overnight and throttled during clinic hours. The math tells you whether that finishes before your deadline.
>
> **Jess:** Two small things I noticed while reading. The DataSync section lists S3, EFS, and FSx for Windows File Server as targets.
>
> **Marcus:** That's what the lecture said, and it's incomplete rather than wrong. DataSync supports the other FSx file systems too, like FSx for Lustre and FSx for NetApp ONTAP. And the second?
>
> **Jess:** The migration overview maps replatform to DMS for same-engine moves, and refactor to DMS for engine changes.
>
> **Marcus:** That one's genuinely ambiguous. Changing database engines, say Oracle to Aurora PostgreSQL, gets called replatforming in a lot of AWS guidance, and refactoring in other places, depending on how much application code changes. The table in your note is a reasonable convention, not a rule. What matters is the work: same-engine moves are mostly a data move, while engine changes need schema conversion and application changes. Label it whichever way your course expects, but plan for the work.
>
> **Jess:** And service names change. Server Migration Service was replaced by the Application Migration Service, which came from CloudEndure.
>
> **Marcus:** Which is why your notes keep saying learn the decision logic. Product names have a shorter half-life than the arithmetic.
>
> **Marcus:** Rapid review. Let's switch to agents and see how much of this carries over. Orchestrating agent activities. Jess, the three execution patterns, one line each.
>
> **Jess:** Sequential when each step depends on the last, like the Wi-Fi support flow, diagnose, then solve, then verify. Parallel when tasks are independent, like the market report pulling news, stock data, and competitor filings at once. And conditional branching when the path depends on an output, like the returns example: eligible goes to inventory and refund, ineligible goes to a denial notice.
>
> **Marcus:** And your notes flag a transcript slip.
>
> **Jess:** The transcript says most real workflows are purely one pattern, and the very next sentence says you'll often see combinations. It should say rarely purely one pattern.
>
> **Marcus:** Right. Now your design question: a travel booking agent. It needs flight search, hotel search, and visa requirements, then payment only if the total is under budget. Lay it out.
>
> **Jess:** Sequential first, parse the request into structured trip details. Then parallel, flight, hotel, and visa agents, since they're independent. Fan in to combine options and total the price. Then branch. Under budget goes to the payment agent behind a confirmation gate. Over budget goes to an agent that proposes cheaper options. And one state object for the whole trip.
>
> **Marcus:** Now apply today's lens. Which of those agents can you retry freely?
>
> **Jess:** The searches. Flight search, hotel search, visa lookup, they're all reads. Retrying them costs time and tokens but doesn't change the world. Payment is the dangerous one.
>
> **Marcus:** Exactly. Reads are retry-friendly. Writes need idempotency keys, and irreversible writes need a gate before them. Your notes say the same about the content creation demo. Publishing is irreversible, so it goes at the end, behind a review. And remember the demo's other flaw?
>
> **Jess:** It labels editing and publishing as parallel, but publishing needs the edited text. The truly parallel tasks would be things like image generation and SEO analysis on the draft.
>
> **Marcus:** Good. Multi-agent state coordination. Your notes list four conflict-resolution strategies.
>
> **Jess:** Predefined rules, negotiation, rollback and retry, and human escalation.
>
> **Marcus:** Rollback and retry has a subtle requirement. What has to be retried?
>
> **Jess:** The whole operation, not just the final write. If the record changed from version five to version six, the agent has to re-read and re-decide, because its original edit might not make sense anymore.
>
> **Marcus:** Right. This is the agent version of the Glue job question. You don't replay the old write, you recompute from the new truth. And if two agents keep colliding?
>
> **Jess:** Livelock. They retry forever and nothing progresses. So you cap retries, add backoff with jitter, and escalate.
>
> **Marcus:** Jitter meaning a bit of randomness in the wait, so the two agents stop retrying in lockstep. Now your self-test math. A record gets about two writes a minute from other actors. Conflict probability for a half-second tool update versus a fifteen-second LLM-mediated update?
>
> **Jess:** The rate is one thirtieth per second. For half a second, one minus e to the minus one sixtieth, about one point seven percent. For fifteen seconds, one minus e to the minus a half, about thirty-nine percent.
>
> **Marcus:** Over twenty times worse. So when an agent's write might conflict, decide first, outside the critical section, then do a fast conditional write. And one transcript fix in that note: the summary mentions "MBCC," which is almost certainly MVCC, multi-version concurrency control, the way databases like PostgreSQL handle concurrency internally, or shorthand for the optimistic concurrency the lesson actually teaches.
>
> **Marcus:** Now the networking labs. Exercise one, building the trading system network. Quick fire. A slash twenty-six subnet. How many usable addresses does AWS give you?
>
> **Jess:** Sixty-four minus the five AWS reserves. Fifty-nine. And a slash twenty-two is a thousand twenty-four minus five, a thousand nineteen.
>
> **Marcus:** Why can't Private Subnet One be one seventy-two dot nineteen dot two dot zero slash twenty-two?
>
> **Jess:** Because a slash twenty-two block has to start on a multiple of four in the third octet. Two dot zero isn't aligned. That's why the guide uses four dot zero and eight dot zero.
>
> **Marcus:** And what keeps the private subnets private?
>
> **Jess:** Routing. The private route table has no default route, no zero dot zero dot zero dot zero slash zero, so there's no path to the internet. It only has the local routes, the route to corporate headquarters through the virtual private gateway, and the S3 gateway endpoint's prefix list route.
>
> **Marcus:** And the gateway endpoint versus interface endpoint gotcha?
>
> **Jess:** For S3, pick the gateway type. It works through the route table and has no hourly charge. The interface type is billed and works differently.
>
> **Marcus:** And the virtual private gateway you attached is not a working VPN. Without a customer gateway and a site-to-site VPN connection, it's a door with no hallway behind it. Now Step Two of the Excipient project, the cross-Region peering lab. Why does the guide use CIDR ranges instead of referencing the other VPC's security group?
>
> **Jess:** Because security group references across a peering connection only work within the same Region. Across Regions, you use the peer's CIDR.
>
> **Marcus:** And why create the flow logs before running the ping and curl tests?
>
> **Jess:** Flow logs only capture traffic after they exist, and records arrive in batches, so you wait a few minutes before querying.
>
> **Marcus:** One more thing to fix in that note, since it's still there. The tables say Account B is in us-west-two, but the flow log section says us-west-one, with a specific VPC ID. Yesterday's episode flagged a similar mismatch between your report and the project overview. Whichever Region you actually built in, the flow log and its log group have to be in that same Region, because log groups are regional. Make the note consistent so future you doesn't query the wrong Region and conclude the logs are broken.
>
> **Jess:** Last one, the Financial Controller prompt library.
>
> **Marcus:** You covered compute-don't-ask and the closed-list mapping yesterday. Let's do two different prompts. Prompt four, operations-safe expense reduction. What's the gate?
>
> **Jess:** For each cost-cutting idea, ask whether it touches uptime, repair time, field capacity, support staffing, or billing accuracy. If it does, name the failure mode, compute the break-even, how much churn would erase the savings, and give a verdict. Green, yellow with a guardrail metric and an owner who can reverse it, or red.
>
> **Marcus:** Let's make the break-even concrete, with a made-up number. Say a tenth of a point of churn is worth sixty thousand dollars a year, and cutting spare radios saves forty thousand. What does that tell you?
>
> **Jess:** If cutting spares raises churn by even about a fifteenth of a point, the savings are gone. That's a small enough effect that it's probably a red, or at least a yellow with very close monitoring.
>
> **Marcus:** Right. And notice "an owner who can reverse it." That's a rollback plan for a business decision. And prompt ten, budget versus actual?
>
> **Jess:** Plan-then-solve. The model proposes how it will separate timing variances from permanent ones, and then it stops and shows me before doing the forecast.
>
> **Marcus:** A human checkpoint before the expensive, consequential step. Same structure as the confirmation gate before payment in the travel agent. And prompt one's compensating controls, like making sure the preparer and the reviewer of a reconciliation are different people, is segregation of duties. Hold onto that one for blast from the past.
>
> **Marcus:** Blast from the past. Structured outputs. Jess, the reliability ladder, bottom to top.
>
> **Jess:** Prompting for JSON. Then an output parser with schema validation. Then function calling. Then strict mode, which is constrained decoding. Then semantic validators with retries and escalation.
>
> **Marcus:** And the one-liner?
>
> **Jess:** A schema guarantees shape, not truth.
>
> **Marcus:** Your note corrects the course reading on something. What?
>
> **Jess:** The reading says function calling guarantees correct format and types. That's only true with strict mode. Plain function calling treats the schema as a strong hint. The model usually complies, but it can still produce a wrong enum value or skip a field.
>
> **Marcus:** Good. Now the retry connection. Your self-test has a model that produces valid JSON ninety percent of the time. With three independent attempts, what's the pass rate?
>
> **Jess:** One minus point one cubed. Ninety-nine point nine percent.
>
> **Marcus:** And why is reality worse?
>
> **Jess:** Because the failures aren't independent. The same confusing input tends to fail the same way each time.
>
> **Marcus:** Correlated failures. Which is exactly why your agentic RAG note says retrying the same query on the same index is pointless. And notice the parallel with the Step Functions discussion earlier. Strict mode is like the green checkmark. It tells you the step produced the right shape, not that it was correct. Content and logic validators are the soft-failure detectors.
>
> **Jess:** Tool descriptions. The model only knows a tool through its name, its description, and its input schema. And the description should state purpose, when to use it, when not to, what it returns, and side effects.
>
> **Marcus:** Side effects. Here's where today's theme gives you a design rule your note doesn't state explicitly. If an agent's runtime is going to retry tool calls, the tool should declare whether it's safe to retry. Read-only? Idempotent? Irreversible? The Model Context Protocol even has optional hints along those lines for tool authors. But your note's critical analysis has the key caveat.
>
> **Jess:** The description can tell the model a tool is destructive, but only the runtime can enforce it. So the retry policy and the confirmation gate have to live in code, not in the description.
>
> **Marcus:** Exactly. And the other connection. Your note says an error message is the next prompt the model reads. An instructive error like "unknown device ID, call search devices first" turns a blind retry into a corrected retry. An opaque error produces the same bad call over and over. That's a livelock with extra tokens.
>
> **Jess:** Last, agentic RAG. Retrieve, reflect, retry.
>
> **Marcus:** And the rule about retries?
>
> **Jess:** Every retry must change something. The query, the retriever, or the source. Otherwise you get the same chunks back.
>
> **Marcus:** And the stop conditions?
>
> **Jess:** Every sub-question answered with a source. A round cap. A round that adds no new relevant passages. Or all tools tried, in which case you answer with stated gaps.
>
> **Marcus:** Now the connection I promised you, segregation of duties. Your note says the reflector is the weak link. The same agent that gathered the evidence judges whether the evidence is enough. And one of your discussion questions asks whether the reflector should be the same model as the generator. What do the Financial Controller's controls and the Well-Architected review suggest?
>
> **Jess:** That the person who prepares something shouldn't be the only one who reviews it. A self-assessment, whether it's a team answering Well-Architected questions or an agent judging its own evidence, tends to be optimistic. So use a separate reviewer, or at least a separate check with different information, like an entity match or a citation-per-claim rule.
>
> **Marcus:** That's the thread. And one more pitfall from that note fits today perfectly: the self-reinforcing loop, where the agent's own earlier summaries get retrieved as evidence on the next round.
>
> **Jess:** Which is the Zillow problem again. A system acting on data that its own previous actions shaped.
>
> **Marcus:** And the cold open problem, in a way. A retry that reads its own previous output as if it were new information. Alright, let's wrap up.
>
> **Marcus:** Three takeaways. First: a retry policy is only as safe as the step it repeats. Before you add retries to anything, a Lambda, an ECS task, a Glue job, an agent tool, ask what happens if it runs twice, and make it idempotent with keys, conditional writes, unique constraints, or overwrite-by-partition.
>
> **Jess:** Second: retries fix hard failures, not soft ones. A green checkmark, a valid schema, or a successful query means the step ran and produced the right shape. It doesn't mean the answer is right. And because failures are correlated, repeating the same thing rarely helps. Change something, validate content, or escalate.
>
> **Marcus:** Third: put the truth in one place and make everything else check against it. The database row and its version, the ledger, the Step Functions execution history, the S3 object key. Reviews, agents, and pipelines that grade their own work drift toward optimism, so the checks should come from somewhere else.
>
> **Jess:** And the think-about-it question?
>
> **Marcus:** Here it is. You're building a customer-support agent on AWS. It has an issue-refund tool backed by a Lambda function, and a Step Functions workflow runs the agent's approved actions with a retry policy. One night, the Lambda calls the payment provider, the provider accepts the refund, and then the Lambda times out before it gets the response. Step Functions retries. Where should idempotency live? In the agent's prompt, the tool description, the Lambda, the state machine, the database, or the call to the payment provider? What breaks if it lives in only one of those places? And what would you log so a human reviewing the incident can tell "refunded once" from "refunded twice"?
>
> **Jess:** I'm going to want a whiteboard for that one.
>
> **Marcus:** That's the point. Thanks for listening to MS AI Daily. Go make something idempotent.
>
> **Jess:** See you tomorrow.
