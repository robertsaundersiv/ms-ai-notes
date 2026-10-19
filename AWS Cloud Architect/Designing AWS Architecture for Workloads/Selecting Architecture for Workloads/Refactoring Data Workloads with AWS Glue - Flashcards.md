---
title: "Refactoring Data Workloads with AWS Glue – Flashcards"
course: AWS Cloud Architect – Designing AWS Architecture for Workloads
type: flashcards
source: "[[Refactoring Data Workloads with AWS Glue]]"
created: 2026-10-18
---

#flashcards/aws/workloads/glue

Flashcards for [[Refactoring Data Workloads with AWS Glue]].

What is AWS Glue?
?
A fully managed, serverless data integration service that automates much of ETL: discovering, preparing, moving, and integrating data. Its ETL jobs run on Apache Spark.

What does ETL stand for?
?
Extract, transform, load: read from sources, reshape or clean the data, and write it to a target for analysis.

In the Health Trend Analysis refactor, what replaces the on-prem Spark cluster, the NAS/SAN, and the Hive Metastore?
?
AWS Glue, Amazon S3, and the AWS Glue Data Catalog.

What is the Glue Data Catalog?
?
A centralized, managed metadata repository of data sources, schemas, and properties. It's the migration target for Hive metastores.

Why is S3 a natural fit for Glue jobs?
?
It's scalable, durable, low-cost object storage that Glue integrates with natively, as both source and target.

What problem with the on-prem cluster does Glue remove?
?
Manually managing scalability, resiliency, and hardware for an always-on cluster. Glue runs only when a job runs.

What three ways can you author a Glue job?
?
A visual editor, a notebook, or a script editor. The script editor suits porting existing Spark code.

Conceptually, what must change to run an existing Spark job in Glue?
?
Wrap it in Glue's context and job lifecycle (initialize at the start, commit at the end), import any Spark functions it uses, and point reads and writes at S3. The transformation logic barely changes.

Where does your own code go in a Glue script?
?
Between the job's initialization and its commit. The editor pre-fills the rest of the boilerplate.

What is an IAM service role?
?
A role that an AWS service assumes to call other AWS services on your behalf, using temporary credentials rather than stored keys.

Why does a Glue job need an IAM service role?
?
To read its input from S3, write its output to S3, and use logging and catalog services.

What is the instructor's approach to permissions, and its risk?
?
Start with broad AWS managed policies, then tighten to least privilege. The risk is that "full access" policies granted to start often never get tightened, leaving account-wide access.

What would a least-privilege policy for an S3-to-S3 Glue job allow?
?
Read on the input prefix, write on the output prefix, and the basic Glue service permissions (logs, catalog). Nothing account-wide.

How is Glue capacity specified?
?
By worker type and number of workers, which together give the job's DPUs. A job runs on a cluster of workers, not one instance.

What is a DPU?
?
A Data Processing Unit, Glue's unit of capacity and billing. A standard DPU is 4 vCPUs and 16 GB of memory.

How is a Glue job billed?
?
Per DPU-hour, by the second (with a short minimum), only while a run is active.

What is the minimum number of workers used in the course's Glue jobs?
?
Two, the smallest allowed. In real jobs you size workers to data volume and transform complexity.

For an S3 ETL job, which path must name an object and which a folder?
?
The input must name the object (the file itself). The output names a folder, because Spark writes one or more part files into it.

Why do the jobs write Parquet instead of CSV?
?
Parquet is columnar and compressed, so query engines read only the columns they need. Queries run faster and cost less per byte scanned.

How should you choose the Glue version?
?
Based on the Spark features you use. Best practice is the latest version.

Why can't you sum the `value` column of a long-format dataset like the IEA EV data?
?
Each row's value has a different meaning and unit (vehicles, percent, GWh, oil displacement), and regional aggregates sit beside their member countries. Filter by parameter and unit first.

When might EMR or EMR Serverless beat Glue for a Spark workload?
?
When the job needs heavy tuning, specific Spark versions, custom libraries, or long-running execution that Glue's managed constraints limit.

When can per-run Glue pricing cost more than a cluster?
?
When the workload is busy around the clock. A committed or Spot-priced cluster can then be cheaper than per-DPU billing.
