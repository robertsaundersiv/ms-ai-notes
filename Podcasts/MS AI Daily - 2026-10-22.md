---
title: "MS AI Daily – 2026-10-22"
type: podcast
created: 2026-10-22
duration_min: 34.9
covers:
  - "[[AWS Cost and Usage Monitoring Tools]]"
  - "[[Tagging Strategies and Cost Allocation]]"
  - "[[Centralized Logging and Event Notification]]"
  - "[[Advanced VPC Connectivity]]"
  - "[[Data Validation and Synchronization]]"
  - "[[LLM Hallucinations]]"
  - "[[MCP Specification 2026 – Changes Since March 2025]]"
  - "[[Agentic AI Skills Scorecard - Study Guide]]"
tags:
  - podcast
  - review
---

# MS AI Daily – 2026-10-22

![[MS AI Daily - 2026-10-22.mp3]]

> [!abstract] In this episode
> The theme is evidence: what each tool can prove, and what it can't. The cold open is an untagged instance at four dollars an hour that nobody owns. Resolving it takes three answers from three different systems: who created it (CloudTrail), what it's for (tags), and who pays (cost allocation). The review segments carry the same idea into peering routes, checksums and migration validation. The blast from the past links it to faithfulness vs. factuality in hallucinations, integrity-protected `requestState` in MCP, and the "orchestrator is the control" idea from the skills scorecard.

## Segments
- **Cold open and agenda:** whose instance is this? Six hundred seventy-two dollars of not knowing. From [[Tagging Strategies and Cost Allocation]]
- **Deep dive: visibility, attribution, control**
  - *What did we spend on, and was it worth it; Cost Explorer enabled on first visit (13 months of history, a 12-month forecast, as defaults); visibility isn't value; the day-12 forecast drill ($5,200 → 130%); forecasts lag regime changes, so pair them with anomaly detection; utilization budgets; budget actions stop instances, they don't terminate them; Lambda timeouts mean paying full price for failure; full Trusted Advisor checks need a Business support plan:* [[AWS Cost and Usage Monitoring Tools]]
  - *The five tag rules; case sensitivity and the note's two inconsistencies; a tag policy validates values but doesn't require the tag (an SCP `Null` condition does); prevent, standardize, detect, plus IaC and Service Catalog; quarantine before delete; activation isn't retroactive; CUR 2.0; the proportional allocation drill ($60k → $40k / $20k) and why it's only a fallback; accounts for the coarse split, tags for the fine split; ABAC makes tag edits security permissions:* [[Tagging Strategies and Cost Allocation]]
  - *Everything is an API call; CloudTrail vs. the stolen-credentials database query (control plane vs. data plane); CloudTrail vs. Config; why a separate Log Archive account; Logs Insights reads log groups, not S3; Athena cost depends on storage layout (about $2 → about 10¢); natural-language queries as drafts, since zero results looks like innocence:* [[Centralized Logging and Event Notification]]
- **Rapid review:** [[Advanced VPC Connectivity]] (peering rules recalled; the lab's missing return route; the VGW's 1.25 Gbps is usable bandwidth, not 2.5; the 5 TB drill, about 8.9 hours; on-premises single point of failure; an unsegmented TGW is a flat network; org-wide CIDR planning), [[Data Validation and Synchronization]] (TechCorp vs. DataSafe; 99.99% of 10M still leaves 1,000 records; the lecture's "number of bits" error; avalanche is a property of cryptographic hashes, not of all checksums; plain hashes don't prove tampering; sameness ≠ correctness; normalize data before hashing in heterogeneous migrations; Direct Connect is a link, not a validator)
- **Blast from the past:** [[LLM Hallucinations]] (faithfulness vs. factuality mirrors sameness vs. correctness; intrinsic vs. extrinsic corrected), [[MCP Specification 2026 – Changes Since March 2025]] (MRTR recalled; `requestState` needs an HMAC for the same reason Transfer Family files do; a handle is a name, not a capability, just like ABAC tags; trace context in `_meta`), [[Agentic AI Skills Scorecard - Study Guide]] (the orchestrator is the control, just like SCPs; p to the n, about 0.66 for 8 steps; a phased migration is a gated chain, but deterministic steps don't benefit from retries)

> [!warning] Corrections and gaps flagged in this episode
> - [[Tagging Strategies and Cost Allocation]]: the key appears as both `SVP:CostCenter` (schema) and `svp:costcenter` (Exercise 2 sheet). Because tags are case-sensitive, those are two different keys and two different billing columns. The allowed values also disagree: the schema says `0001`/`0002`/`0003`, but self-test Q8's tag policy allows `1`/`2`/`3`. Pick one canonical key and one value format, and use them everywhere.
> - [[Centralized Logging and Event Notification]]: the Log Archive diagram shows the S3 buckets feeding CloudWatch Logs Insights. Logs Insights queries CloudWatch Logs **log groups**, not objects in S3. To use Insights on CloudTrail, the trail must also deliver to a log group, which has its own ingestion cost. Athena is the tool that reads S3 directly.
> - [[Data Validation and Synchronization]]: "any change produces a completely different value" is true of cryptographic hashes like SHA-256 (the avalanche effect), not of checksums in general. A simple additive checksum misses swapped bytes. Also, a plain hash only shows tampering if the attacker can't replace the checksum too. Tamper evidence needs an HMAC, a signed manifest, or a separately trusted channel.
> - [[LLM Hallucinations]]: in the standard taxonomy (Ji et al., listed in the note's own Further Reading), **intrinsic** means the output *contradicts* the source, and **extrinsic** means the source can't verify it (it neither supports nor contradicts it). So self-test Q1, a date that isn't in the source, is extrinsic. The definition table should also say that extrinsic is about the *source*, not the world. An extrinsic addition can even be true.
> - [[AWS Cost and Usage Monitoring Tools]]: 13 months of history and a 12-month forecast are the lecture's defaults. AWS has added options over time, such as longer history you can opt into, so check the current docs before quoting limits in a design.

## Think about it
Your team runs an agent platform in one shared AWS account. The agents call an external LLM provider's API and a set of MCP tool servers. Finance wants per-team chargeback for both compute and token spend. Security wants an audit trail of which agent did what, on whose behalf. Resource tags won't capture per-request token costs, and CloudTrail won't see calls to an outside model API. Where do you put the attribution point: one account per team, a team identifier carried in every request's metadata (like MCP trace context), or a ledger kept by the orchestrator? For whichever you choose, what is the failure mode, and who could forge or lose that attribution?

> [!quote]- Transcript
> **Marcus:** Picture this. You're doing a cost review and you find a single E C 2 instance costing four dollars an hour. No name tag. Nobody in the channel claims it. Someone says, "I think it's Ed's, but Ed's on vacation. It might be production for that big new client, so maybe just leave it." Jess, what does that week of not knowing cost?
>
> **Jess:** Four dollars, times twenty-four hours, times seven days. Six hundred seventy-two dollars.
>
> **Marcus:** Six hundred seventy-two dollars to protect yourself from a question you couldn't answer. Now here's the more interesting part. To actually resolve that mystery, you need three different answers. Who created it? What is it for? And who pays for it? Those three answers come from three completely different systems in A W S.
>
> **Jess:** Let me guess. Who created it is a logging question, what it's for is a tagging question, and who pays is a billing question.
>
> **Marcus:** Exactly right, and that's today's whole episode in one sentence. Welcome to MS AI Daily for Thursday, October twenty-second, twenty twenty-six. I'm Marcus.
>
> **Jess:** And I'm Jess. So the theme today is something like, can you actually prove it?
>
> **Marcus:** That's the theme. Evidence. What each tool can prove, and just as important, what it can't. Here's the plan. The deep dive covers three notes from your cost and governance lessons. First, the cost and usage monitoring tools, meaning Cost Explorer, Budgets, and Trusted Advisor. Second, tagging strategies and cost allocation, where your note has a small inconsistency we need to fix. Third, centralized logging with CloudTrail and Config, including one diagram in your note that implies something A W S doesn't actually do.
>
> **Jess:** Then the rapid review?
>
> **Marcus:** Advanced V P C connectivity, and data validation for migrations. That second one has a correction from the lecture that I want to push one step further. Then, for the blast from the past, we'll revisit LLM hallucinations, the MCP specification changes, and your Agentic AI skills scorecard. One of those has a definition I'm going to argue with.
>
> **Jess:** Arguing with my notes. Love it. Let's go.
>
> **Marcus:** So let's start with visibility. The lecture frames cost management around two questions. What are we paying for, and is it worth it? And it makes a point I really like. When the bill is bigger than expected, the bill is almost always right. People's first instinct is to suspect A W S made a mistake.
>
> **Jess:** Which is the cloud equivalent of saying the scale must be broken.
>
> **Marcus:** The scale is fine. Put down the cookie. So the first stop is Cost Explorer. From your notes: it's enabled the first time you open the console, data shows up within about twenty-four hours, you get thirteen months of history, and a twelve-month forecast. You can filter by service, Region, Availability Zone, instance type, platform, and account. Quick question before I go further. Why does it matter that it's enabled on first visit, rather than always on?
>
> **Jess:** Because if nobody's opened it, then on the day the C F O asks, you've got nothing for the first twenty-four hours?
>
> **Marcus:** Right. It's a small operational trap, and it's why the note lists "opening Cost Explorer too late" as a failure mode. Enable it on day one of a new organization. One small caveat on the numbers. Thirteen months of history and a twelve-month forecast are the defaults the lecture teaches, and they're the right exam answers. A W S has added options over time, like opting into longer monthly history, so if you're designing for a real finance team, check the current docs before promising them a number.
>
> **Jess:** Okay. And filtering is about finding outliers. You slice by account or Region and the expensive thing jumps out.
>
> **Marcus:** Yes. And notice what Cost Explorer answers. It answers "what did we spend on." It does not answer "was it worth it." That's what your critical analysis section calls out. Visibility isn't optimization. If the market prediction team's G P U spend funds a model that makes money, cutting it isn't a saving, it's a loss.
>
> **Jess:** So Cost Explorer gives you the numerator, but not the denominator. You know the cost, but not the value.
>
> **Marcus:** That's a sharp way to say it. The value side needs business context the tool simply doesn't have. Now, Budgets. We spent a lot of time yesterday on budget actions for the capstone, so I won't repeat all of that. I want to focus on the forecast side, because it's the most underused feature. Let me give you one from your self-test. A ten thousand dollar monthly budget. Actual-spend alerts at eighty and ninety-five percent. Forecast alerts at one hundred and one hundred fifty percent. It's day twelve of a thirty-day month, and spend is fifty-two hundred dollars. Which alerts have fired?
>
> **Jess:** Actual is fifty-two hundred over ten thousand, so fifty-two percent. Neither actual alert. For the forecast, if I go linear, it's fifty-two hundred times thirty over twelve. That's thirteen thousand. So a hundred thirty percent. The one hundred percent forecast alert fires, the one fifty doesn't.
>
> **Marcus:** Perfect. And here's why that matters. On day twelve, the actual alerts are silent. If you only had actual-spend alerts, you'd find out around day nineteen or twenty, when there's no time left to change anything. The forecast alert gives you two and a half weeks of runway.
>
> **Jess:** But wait. Isn't a forecast only as good as the trend it's built on? What if spend jumps suddenly?
>
> **Marcus:** That's exactly the weakness your note identifies. Forecasts lag regime changes. If the data science team kicks off a big training run on day twenty, the trend from days one to nineteen says nothing about it. That's why the next lesson pairs forecasts with anomaly detection, which looks for deviations rather than trends. Forecasts catch slow creep. Anomaly detection catches sudden jumps. You want both.
>
> **Jess:** And AWS's real forecast isn't linear, right? The note says that.
>
> **Marcus:** Correct. The linear version is a teaching model. The real one is more sophisticated, but the principle holds. The other half of Budgets people forget is that it watches in both directions. Overspend, and under-use of commitments. If you bought a Savings Plan or Reserved Instances, a utilization budget tells you when you're not using what you paid for.
>
> **Jess:** The drink-subscription analogy from the lecture. You've already paid, so you should drink the drinks.
>
> **Marcus:** Exactly. And one correction your note already makes, which I'll just reinforce. The lecture says a budget action can "terminate" E C 2 or R D S instances. The documented action is stopping them, not terminating. That's a big difference. Stopping is reversible. Terminating destroys the instance and possibly its storage. If someone hears "terminate" on an exam and picks that answer, they've misunderstood how cautious A W S designed this to be.
>
> **Jess:** Good. And then Trusted Advisor is the waste detector.
>
> **Marcus:** Right. Idle or under-used E C 2, E B S, Redshift, and R D S. Idle NAT gateways. S3 buckets with no lifecycle policy. And my favorite: Lambda functions that keep hitting their timeout. Jess, why is a Lambda timeout a cost problem and not just a reliability problem?
>
> **Jess:** Because you pay for the duration. If it runs for the full timeout and then fails, you paid for the whole run and got nothing back. And if something retries it, you pay again.
>
> **Marcus:** Exactly. You're paying full price for failure, sometimes several times. In agent terms, it's like an agent loop that runs to its step cap without finishing. You paid for every step and got no answer. Last Trusted Advisor detail: the full set of checks requires a Business support plan or higher. On a basic account, you see a limited set. So if a client says "Trusted Advisor didn't flag anything," the first question is which support plan they're on.
>
> **Jess:** Okay, so that's visibility. Cost Explorer tells you what, Budgets tells you when you're drifting, Trusted Advisor tells you where the waste is. But none of them tell you whose it is.
>
> **Marcus:** Which brings us back to Ed's mystery instance, and to tagging. A tag is a key-value pair. Key is the name, value is the data. Most resources allow up to fifty. And here are the rules from the lecture. Jess, you've got these in your note. Give me as many as you can.
>
> **Jess:** Tags are case-sensitive. A W S reserves the lowercase "aws colon" prefix for tags it applies itself. Never put secrets in tags, because they aren't encrypted. Never put personal information in them. And use your own prefix, like S V P colon, for Steady Volatility Partners.
>
> **Marcus:** All five. And case sensitivity sounds trivial until you look at a billing report with three columns called CostCenter, costcenter, and Cost dash Center, each holding a third of your spend.
>
> **Jess:** That's the spreadsheet version of three people each thinking someone else paid the bill.
>
> **Marcus:** Ha. Yes. And speaking of case sensitivity, your note has an example of exactly this problem, so let's use it as a teaching moment. Your tag schema table uses the key S V P colon CostCenter, capital S V P, capital C, capital C. But in parentheses it notes that the Exercise 2 sheet spells it all lowercase, s v p colon costcenter. Those are two different tags. If half the team follows the schema and half follows the exercise sheet, you get two billing columns.
>
> **Jess:** Oh. And I just copied both into the same note without thinking about it.
>
> **Marcus:** Which is an honest mistake, and exactly how it happens in real organizations. There's a second inconsistency too. The schema says the allowed values are zero zero zero one, zero zero zero two, and zero zero zero three. But self-test question eight says the tag policy should allow only one, two, and three. To a tag policy, the string "one" and the string "zero zero zero one" are completely different values. If you build the policy from the self-test, every resource tagged according to the schema gets rejected.
>
> **Jess:** So I should pick one canonical form for both the key and the values, and fix the note to match.
>
> **Marcus:** Pick one, write it down, and enforce it. Which brings us to enforcement, and I want you to walk into a trap first. If I want every new E C 2 instance to have a cost center tag, what's the tool for that?
>
> **Jess:** A tag policy. That's what tag policies are for, right? You define the allowed key and values, and it enforces them.
>
> **Marcus:** That's what most people assume, and it's the most important gotcha in this note. A tag policy standardizes. It can block a wrong value, like cost center equals nine, or the wrong capitalization. But on its own, it does not stop someone from creating a resource with no cost center tag at all. It validates the tag if it's present. It doesn't require it to be present.
>
> **Jess:** Huh. So it's like a form field that checks your phone number format, but lets you leave the field blank.
>
> **Marcus:** That's a perfect analogy. To make the tag required, you use a service control policy. A deny on run instances when the request tag for cost center is null. Null meaning the tag wasn't supplied. And one caution: tag policy features do get updated, so check the current documentation before you put this in a design doc. But as your note describes it, and as the course teaches it, the layering is the point. The S C P requires the tag. The tag policy validates the value. And AWS Config catches anything that slipped in through some other path.
>
> **Jess:** Prevent, standardize, detect. Three layers.
>
> **Marcus:** And the fourth layer is making the right thing the easy thing. Infrastructure as code, CloudFormation or Terraform, with the tags baked into the template, served through Service Catalog so people can launch approved products without ever touching the template. If the tag is in the template, nobody has to remember it.
>
> **Jess:** What about resources that already exist with bad tags?
>
> **Marcus:** Tag Editor for batch fixes, and the Resource Groups Tagging A P I for scripted scans. And the lecture mentions something some enterprises do: automatically quarantine or delete resources that aren't tagged properly.
>
> **Jess:** That sounds great until it deletes the trading database.
>
> **Marcus:** That's exactly the concern in your critical analysis. Automatic deletion needs a sequence. Notify the owner, then quarantine, meaning stop it or isolate it, and only delete after a grace period. Plus exemptions for resources in protected organizational units. A policy that deletes a mis-tagged production database on a Friday night is how you meet your company's lawyers.
>
> **Jess:** Okay, here's where I get confused. I can tag everything perfectly, but the bill still doesn't show my tags?
>
> **Marcus:** Right, and that's the activation step. Tags don't appear in billing data until you activate them as cost allocation tags in the Billing console. There are A W S-generated ones, like aws colon createdBy, and user-defined ones, like your cost center. And the note flags something beyond the lecture: activation isn't retroactive. Billing data only carries the tag from roughly when you activate it.
>
> **Jess:** So if I activate it on the last day of the quarter, the whole quarter is untagged in the report.
>
> **Marcus:** Exactly. Activate early. Then the payoff is the Cost and Usage Report, version two point oh, created through Data Exports. It's the most detailed billing dataset A W S provides, and once your tags are activated, they show up as columns. That's what lets finance do chargeback.
>
> **Jess:** Can we do the allocation math? That one feels like an exam question.
>
> **Marcus:** Let's do your self-test version. A sixty thousand dollar bill. Forty-five thousand is tagged. Team A has thirty thousand, Team B has fifteen thousand. Allocate the untagged amount proportionally.
>
> **Jess:** Untagged is fifteen thousand. Team A is two-thirds of the tagged spend, so it gets two-thirds of fifteen thousand, which is ten thousand. Total forty thousand. Team B gets one-third, five thousand, so twenty thousand total. And coverage was forty-five over sixty, seventy-five percent.
>
> **Marcus:** Spot on. Now the critical question. Is proportional allocation fair?
>
> **Jess:** It's fair if the untagged spend is distributed like the tagged spend. But if most of the untagged spend is, say, a NAT gateway that only the trading team uses, then the H R team is subsidizing trading.
>
> **Marcus:** Exactly. Proportional spreading is a fallback, not a fix. The real fix is raising coverage toward ninety-five percent or more through enforcement. And here's an architectural point that ties back to your earlier lessons. If you already have an account per workload, the account boundary gives you clean cost separation for free. Tags matter most inside shared accounts, and for cross-cutting dimensions like environment.
>
> **Jess:** Accounts for the coarse split, tags for the fine split.
>
> **Marcus:** That's the line from your note, and it's the right one. One more thing about tags that people underestimate. The lecture lists access control as a use, which beyond the lecture is called attribute-based access control. An I A M policy can say you can only stop instances whose project tag matches your own project tag. Jess, what's the security consequence of that?
>
> **Jess:** Then the ability to change a tag is basically the ability to change permissions. If I can retag someone else's instance with my project, I can suddenly manage it.
>
> **Marcus:** Exactly. Once tags drive access, tagging permissions are security permissions. So the people who can edit tags need to be controlled as carefully as the people who can edit I A M policies. It's the same pattern you'll see later with MCP handles. A label is not a capability unless you decide to make it one, and then you have to protect it like one.
>
> **Jess:** Okay. So far we know what we spent and whose it is. The third question from the cold open was who created it.
>
> **Marcus:** And that's centralized logging. The foundational idea from this lecture is short: in A W S, everything is an A P I call. You click a button in the console, it becomes an A P I call. You run a C L I script, A P I call. Your Java app uses the S D K, A P I call.
>
> **Jess:** Which is why CloudTrail can audit almost everything. It sits on the A P I.
>
> **Marcus:** Right. CloudTrail records A P I reads and writes, plus console sign-ins, and stores them in S3. It's also why service control policies can control almost everything, since they evaluate those same A P I calls. Same chokepoint, two uses. Now, scenario. Someone used stolen credentials to connect to your trading database and ran queries that pulled customer records. You open CloudTrail. What do you find?
>
> **Jess:** I'd find the queries, right? They're actions against an A W S service. R D S is an A W S service.
>
> **Marcus:** That's the misconception the note calls the biggest one in this lesson, and it's a very reasonable guess. CloudTrail records calls to the R D S A P I, like create a database, modify it, delete a snapshot. Those are control-plane actions. But a S Q L query sent over the network to the database engine isn't an R D S A P I call. It's data-plane traffic. CloudTrail never sees it.
>
> **Jess:** So CloudTrail sees someone building the house, but not who walks through the front door.
>
> **Marcus:** I like that. And for the front door, you need database audit logs, V P C flow logs for connection metadata, and application logs. Same with S3. Reading objects is a data event, and data events are optional and billed separately. If you didn't turn them on for the sensitive bucket, you can't say who read the file.
>
> **Jess:** And Config is the other half?
>
> **Marcus:** Config is the other half. CloudTrail records who did what. Config records what things look like over time. CloudTrail answers "who deleted the bucket policy." Config answers "which buckets are public right now, and when did this one become public." And Config can notify and auto-remediate when something drifts. That's also what powers Control Tower's detective controls.
>
> **Jess:** And all of these logs go to the Log Archive account.
>
> **Marcus:** Right. Why a separate account, instead of keeping each account's logs at home?
>
> **Jess:** Two reasons, I think. One place to search. And if an attacker compromises a workload account, they can't delete the evidence, because the logs aren't there.
>
> **Marcus:** Both correct, and the second one is the important one. A burglar shouldn't be able to edit the security camera footage. Now, analytics. Once the logs are centralized, the lecture gives four options. CloudWatch Logs Insights, which is cheap and simple and even accepts natural-language questions. Athena, which runs S Q L directly over S3 and charges per terabyte scanned. OpenSearch, which is an always-on cluster with dashboards. Or a third-party tool like Datadog or Splunk.
>
> **Jess:** And the note has a nice diagram with the Log Archive bucket feeding all four.
>
> **Marcus:** That's the diagram I want to correct. Your diagram draws the Log Archive S3 buckets feeding CloudWatch Logs Insights. But Logs Insights doesn't query files sitting in an S3 bucket. It queries CloudWatch Logs log groups. Athena is the one that reads S3 directly. So if you want to use Logs Insights on CloudTrail, the trail also has to deliver to a CloudWatch Logs log group. That's a separate destination with its own ingestion cost.
>
> **Jess:** So the S3 archive and the CloudWatch log group are two separate copies, and each analytics tool reads from a different one.
>
> **Marcus:** Exactly. Many organizations do both: CloudWatch Logs for recent operational data, and S3 for the long-term archive, queried with Athena. Which leads to the most practical number in the note. At about five dollars per terabyte scanned, a query over four hundred gigabytes of raw J S O N CloudTrail logs costs about two dollars. Convert to Parquet, partition by date, and the same question might scan twenty gigabytes, about ten cents.
>
> **Jess:** So your bill depends on how you store the data, not how clever your query is.
>
> **Marcus:** That's exactly it. Storage layout drives Athena cost. And one last point that's right in your wheelhouse. Logs Insights can translate a natural-language question into a query. Jess, put on your Agentic AI hat. What's the risk?
>
> **Jess:** It's an LLM generating a query, so it can be wrong while looking confident. If it filters on the wrong field during a forensic investigation, you get zero results, and you conclude nothing happened.
>
> **Marcus:** A false all clear. And notice: zero results looks exactly like innocence. The generated query is a draft, not evidence. The analyst has to read it. That's a gate check with a human as the gate, and we'll come back to that idea in the blast from the past.
>
> **Jess:** Okay, rapid review. You said V P C connectivity first.
>
> **Marcus:** Let's make it active recall. Give me the rules of V P C peering.
>
> **Jess:** One peering connects exactly two V P Cs. Same account or different accounts. No overlapping CIDR ranges. It's not transitive, so if A peers with B and B peers with C, A can't reach C. Someone requests, someone accepts. And then you need routes on both sides.
>
> **Marcus:** Complete. And that last point is where your lab got interesting. In the demo, the instructor only added a route on the trading V P C side. Your note caught that. What happens?
>
> **Jess:** Traffic goes out, but the replies have no route back. So connections just time out.
>
> **Marcus:** Which is the most frustrating failure in networking, because everything looks configured. Now the virtual private gateway. Two I P sec tunnels at one point two five gigabits per second each. What's the usable bandwidth?
>
> **Jess:** One point two five. Not two point five. They're active-passive, so only one carries traffic at a time.
>
> **Marcus:** Right. The second tunnel is resilience, not capacity. And there's a subtle point in your note: that redundancy only covers the A W S side. If you have one on-premises router on one internet circuit, that's still a single point of failure. Quick math: how long to move five terabytes at full speed?
>
> **Jess:** Five terabytes is forty terabits. Divided by one point two five gigabits per second, that's thirty-two thousand seconds. A bit under nine hours.
>
> **Marcus:** About eight point nine hours, before I P sec overhead and the internet being the internet. If you need more, the note mentions transit gateway with equal-cost multipath across multiple tunnels, or Direct Connect. And we did the mesh math yesterday, so I'll skip it.
>
> **Jess:** And the critical-analysis point I liked is that non-transitivity is actually a security feature.
>
> **Marcus:** Yes. Every path has to be explicit. A transit gateway makes connectivity easy, which means if you don't segment its route tables, you've built a flat network with a very expensive name. One last gotcha: plan CIDR ranges across the whole organization. Your self-test has a new research V P C proposed with the same range as the trading V P C. If you allow that, you've quietly ruled out ever peering them.
>
> **Jess:** Okay. Data validation.
>
> **Marcus:** This one has my favorite correction. Give me the tale of two migrations in thirty seconds.
>
> **Jess:** TechCorp rushed, skipped testing, didn't turn on D M S validation, and didn't verify afterward. They ended up with orders mismatched to shipping addresses, missing customer records, and financial discrepancies. DataSafe planned, tested, turned on D M S validation, added custom checksums for critical data, and migrated in phases. They got ninety-nine point nine nine percent accuracy and kept compliance.
>
> **Marcus:** Good. And what's the problem with celebrating ninety-nine point nine nine percent?
>
> **Jess:** At ten million records, that's still a thousand bad records. For a bank, every one of those needs to be found and reconciled.
>
> **Marcus:** Exactly. "Ninety-nine point nine nine percent accurate" is a statistic. "Every discrepancy explained" is a control. Now, checksums. Your note already corrects the lecture. The lecture says a checksum indicates the number of bits in the transmission. That's wrong. A checksum is computed from the content. Two files of the same size with different content produce different checksums. That's the whole point.
>
> **Jess:** And the note shows S H A two fifty-six of "hello world" versus "hello world" with an exclamation point. The whole hash changes.
>
> **Marcus:** Right. Now I want to tighten two more claims in that note. First, the T L D R says that with a checksum, any change produces a completely different value. That's true of cryptographic hashes like S H A two fifty-six, because of what's called the avalanche effect. It's not true of every checksum. A simple additive checksum just sums the bytes. Swap two bytes and the sum doesn't change. Cyclic redundancy checks are great for random transmission errors, but they don't scramble the output the way a cryptographic hash does. So the claim holds for the hash your note recommends, not for checksums in general.
>
> **Jess:** Okay, so "checksum" is the category, and S H A two fifty-six is the strong version that has the property I wrote down.
>
> **Marcus:** Exactly. The second point matters more. The note says a changed checksum reveals errors or tampering. For accidental errors, yes. For tampering, only if the attacker can't also replace the checksum. If the file and its checksum travel together on the same channel, someone who can modify the file can just recompute the hash and swap it too.
>
> **Jess:** So detecting tampering needs something the attacker can't forge. Like a key.
>
> **Marcus:** Right. A keyed hash, which is called an H MAC, or a digital signature on the manifest, or a checksum delivered through a separate trusted channel. A plain hash proves the copy matches what you were given. It doesn't prove who gave it to you. Hold onto that, because it shows up again in the MCP note.
>
> **Jess:** And the other big idea is that a checksum proves sameness, not correctness.
>
> **Marcus:** Yes. A perfect copy of bad source data passes every checksum. And for heterogeneous migrations, say Oracle to PostgreSQL, the same value can be stored differently, with different precision, encoding, or time zone handling. A naive row hash will report false mismatches unless you normalize first. Last gotcha from the services table. D M S, MGN, and DataSync have built-in validation. Transfer Family and Direct Connect need manual checksums. And your note correctly points out that Direct Connect is a network link, not a transfer tool. Whatever sends data over it is responsible for validating it. Also, MGN's "validation" is really launching test instances and confirming the application works, which is a different kind of check from comparing rows.
>
> **Jess:** Okay. Blast from the past. You said you're going to argue with one of my definitions.
>
> **Marcus:** I am. Let's start with LLM Hallucinations, from about a month ago. And I want to connect it to what we just said. Checksums prove sameness, not correctness. What's the hallucination version of that distinction?
>
> **Jess:** Faithfulness versus factuality. Faithfulness is whether the output is supported by the source you gave it. Factuality is whether it's true in the world. You can be perfectly faithful to a wrong source.
>
> **Marcus:** Exactly the same shape. A RAG system that quotes an outdated policy document perfectly is faithful and wrong. Now, your self-test question one. A summary adds a date that isn't in the source document, and the date is also wrong. Intrinsic or extrinsic?
>
> **Jess:** My note says intrinsic, because it's unsupported by the source.
>
> **Marcus:** And this is where I disagree with the note. In the standard taxonomy, from the Ji and colleagues survey that your note lists as further reading, intrinsic means the output contradicts the source. Extrinsic means the output can't be verified from the source. The source neither supports nor contradicts it. A date that simply isn't in the document is the textbook example of extrinsic. If the source had said the meeting was on the fourth and the summary said the fifth, that would be intrinsic.
>
> **Jess:** So my definition table blurred them. It says intrinsic is "unsupported by, or contradicts" the context. And it describes extrinsic as contradicting the world.
>
> **Marcus:** Right. Under the standard definitions, unsupported-but-not-contradicted is extrinsic, and extrinsic is about the source, not the world. An extrinsic addition might even be true. It's just not verifiable from what you gave the model. Some papers use the terms a bit loosely, so you'll see variation. But the survey your note cites draws the line at contradicts versus can't verify.
>
> **Jess:** Why does the distinction matter in practice, though? Either way it's a bad output.
>
> **Marcus:** Because the detectors are different. An intrinsic error can be caught by checking the output against the source, using something like an entailment check, which asks whether the source implies the claim, or flags a contradiction. An extrinsic addition needs a citation gate. Every claim has to point to a line, and anything without a citation fails. Your note's own worked example does exactly that: the summary invents a disk failure, there's no source line for it, and the citation gate catches it. That invented disk failure is extrinsic.
>
> **Jess:** Okay. I'll fix that in the note. What about MCP?
>
> **Marcus:** Your MCP specification note, from about two weeks ago, covers the move to a stateless protocol in the July twenty twenty-six revision. I'll trust your note's reading of the spec, since you went to the source pages. The piece I want to recall is Multi Round-Trip Requests. Remind me how it works.
>
> **Jess:** Instead of the server calling back to the client in the middle of a tool call, the server returns an input-required result with a list of what it needs, plus an opaque string called request state. The client gathers the input, then sends a brand-new request with the answers and the same request state echoed back. The server rebuilds its context from that state.
>
> **Marcus:** Good. And why does the note insist that request state be integrity-protected?
>
> **Jess:** Because it passes through the client, so a malicious client could tamper with it. Oh, this is the checksum thing. A plain hash wouldn't help, because the client could change the state and recompute the hash.
>
> **Marcus:** That's the connection. The spec's guidance is an H MAC or authenticated encryption, with a key only the server holds. It's the same lesson as the Transfer Family files, just in a different place. And the note's other phrase, that a handle is a name and not a capability, is the same lesson as tag-based access control. A basket I D or a project tag is a label. Authorization still has to be checked on every use.
>
> **Jess:** And the logging connection? The note mentions OpenTelemetry trace context in the request metadata.
>
> **Marcus:** Right. Since every request is self-contained, it can carry its own trace context, so you can follow an agent's tool calls across services. It's the agent-world version of "everything is an A P I call." If every action is a request, every action can be logged at a chokepoint.
>
> **Jess:** And the skills scorecard?
>
> **Marcus:** Quickly, from about a month ago. One idea from the scorecard ties this whole episode together. The interview line in your note: the LLM is only the policy, and the orchestrator decides what it's allowed to do. It executes the tools, holds the memory, and enforces stop conditions and budgets. Compare that to today. Where did control actually live in A W S?
>
> **Jess:** Not in asking people nicely. It lived in S C Ps, budget actions, Config rules. Code at a chokepoint. Same as the orchestrator.
>
> **Marcus:** Exactly. A persona that says "please be frugal" is the equivalent of a wiki page asking engineers to tag their resources. Nice to have. Not a control. And the reliability math from the scorecard applies to migrations too. With n steps that each succeed with probability p, end-to-end success is roughly p to the n. Your note's eight-stage example at ninety-five percent per step comes out to about sixty-six percent end to end. That's the case for DataSafe's phased migration with validation gates. Each gate raises the per-step reliability before errors compound.
>
> **Jess:** So a phased migration with validation at each stage is basically a prompt chain with gate checks.
>
> **Marcus:** Structurally, yes. Where the analogy breaks is that migration steps are mostly deterministic, and if you rerun them you get the same result. LLM steps are stochastic, so a retry can actually fix the problem. Rerunning a broken migration script just reproduces the same broken output.
>
> **Jess:** Okay, wrap it up for me.
>
> **Marcus:** Three takeaways. One. Visibility, attribution, and control are separate layers, and each has its own tools. Cost Explorer tells you what you spent. Accounts and activated tags tell you whose it is. Budgets, S C Ps, and Config are what actually act. If one layer is missing, the others can't make up for it.
>
> **Jess:** Two?
>
> **Marcus:** Two. Know exactly what your evidence covers. CloudTrail covers the control plane, not queries to your database. A checksum proves sameness, not correctness. A tag policy validates values, but it doesn't require that the tag exists. A citation gate catches unsupported claims, but not faithful copies of wrong sources. Most real incidents happen in the gap between what a tool covers and what people assume it covers.
>
> **Jess:** And three?
>
> **Marcus:** Three. Integrity needs a trust anchor. A hash proves nothing if the attacker can rewrite it too. Logs prove nothing if the compromised account can delete them. Request state proves nothing without a server-held key. Every time you rely on evidence, ask who could forge it, and put the anchor somewhere they can't reach.
>
> **Jess:** And the think-about-it question?
>
> **Marcus:** Here it is. Imagine your team runs an agent platform in one shared A W S account. The agents call an external LLM provider's A P I and a set of MCP tool servers. Finance wants per-team chargeback for both compute and token spend. Security wants an audit trail of which agent did what, on whose behalf. Resource tags won't capture per-request token costs, and CloudTrail won't see calls to an outside model A P I. So where do you put the attribution point? One account per team? A team identifier carried in every request's metadata, like the trace context in MCP? Or a ledger kept by the orchestrator itself? And for whichever you choose, what's the failure mode, and who could forge or lose that attribution?
>
> **Jess:** My first instinct is the orchestrator, but I'm already wondering what happens when an agent calls a tool that calls another model.
>
> **Marcus:** Good. Keep pulling that thread, but don't answer it yet. And go fix those two inconsistencies in your tagging note before they become two billing columns. Thanks for listening to MS AI Daily.
>
> **Jess:** See you tomorrow.
