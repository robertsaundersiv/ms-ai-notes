---
title: "Exercise 2 – Convert a Spark ETL Job to AWS Glue – How To"
aliases:
  - C2 L1 Exercise 2 How To
  - Spark to Glue exercise
  - Global EV data Glue job
course: AWS Cloud Architect – Designing AWS Architecture for Workloads
lessons:
  - Demo – IAM Roles
  - Demo – The AWS Glue Console
  - Demo – Glue
  - Demo – Exercise 2 Solution
type: how-to
created: 2026-10-18
related:
  - "[[Refactoring Data Workloads with AWS Glue]]"
  - "[[Exercise 1 - Well-Architected Review and Migration Strategy - How To]]"
  - "[[Exercise 3 - Event-Driven Notifications with Lambda and SNS - How To]]"
tags:
  - aws/glue
  - aws/s3
  - aws/iam
  - aws/lab
  - how-to
---

# Exercise 2 – Convert a Spark ETL Job to AWS Glue – How To

> [!abstract] Goal
> Port an on-prem PySpark job that **reads `iea-global-ev-data-2024.csv`, drops a column, and writes Parquet** so it runs as an **AWS Glue** job, reading from one S3 location and writing to another.
> 1. Convert the script (GlueContext, job init/commit, S3 paths)
> 2. Create an IAM service role for Glue
> 3. Create, configure, and run the Glue job
> 4. Verify the Parquet output in S3
>
> It takes about 20–30 minutes.

**Concepts:** [[Refactoring Data Workloads with AWS Glue]] · **Previous lab:** [[Exercise 1 - Well-Architected Review and Migration Strategy - How To]] · **Next lab:** [[Exercise 3 - Event-Driven Notifications with Lambda and SNS - How To]]
**Source:** built from the Glue demo videos and the Exercise 2 solution video. The exercise sheet wasn't provided. **Use the sheet's values (column to drop, bucket names, job name) where they differ.**

> [!note] Works in the Udacity account
> The demo and solution both run in the Udacity-provided account. It limits Glue capacity, so use the **smallest worker type** and **2 workers**.
> **Cost:** a two-minute run on 2 small workers costs a few cents ([[Refactoring Data Workloads with AWS Glue#Cost of a Run|estimate]]). S3 storage of the output is negligible.

---

## 0. Before You Start

| Item | Value |
|---|---|
| Input data | `iea-global-ev-data-2024.csv` (12,654 rows; columns `region, category, parameter, mode, powertrain, year, unit, value`) |
| Input location | Udacity bucket, `input/` folder. The solution's bucket was "demo-bucket-architecting-workloads"; **yours will differ** |
| Output location | Same bucket, `output/` folder |
| IAM role | `AWS-Glue-S3Role` (any name, no spaces) |
| Job name | e.g. `glue-exercise-job` |
| Worker type / count | Smallest / **2** |
| Column to drop | **From the exercise sheet** |

> [!tip] If the CSV isn't already in S3
> Upload the copy in your Downloads folder: S3 → your bucket → `input/` → **Upload** → add `iea-global-ev-data-2024.csv` → **Upload**.

---

## 1. Convert the Script

Take the on-prem job and make four changes:

1. Add the Glue imports (the console pre-fills them) **and** any PySpark functions you use.
2. Replace the `SparkSession` with `GlueContext` + `Job.init`.
3. Replace local paths with **S3 URIs**.
4. Replace `spark.stop()` with `job.commit()`.

The finished script should look like this (replace the bucket and column):

```python
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# --- our code goes here ---
INPUT = "s3://<your-bucket>/input/iea-global-ev-data-2024.csv"   # the FILE
OUTPUT = "s3://<your-bucket>/output/"                            # a FOLDER
DROP_COLUMN = "<column from the sheet>"

df = spark.read.csv(INPUT, header=True, inferSchema=True)
df.drop(DROP_COLUMN).write.mode("overwrite").parquet(OUTPUT)

job.commit()
```

✅ **Check:** no `SparkSession.builder` and no `spark.stop()` left in the script.

---

## 2. Find the S3 URIs

1. **S3 → Buckets →** your bucket → `input/` → **click the CSV object itself** → **Copy S3 URI**. Paste it as `INPUT`.
2. Go back to the bucket → select the `output/` folder → **Copy S3 URI**. Paste it as `OUTPUT`.

> [!warning] The input must be the file
> The instructor nearly made this mistake live. Copying the folder URI for the *input* reads the wrong objects. The *output* is a folder because Spark writes `part-*.parquet` files into it.

✅ **Check:** `INPUT` ends in `.csv`; `OUTPUT` ends in `/`.

---

## 3. Create the IAM Service Role

1. **IAM → Roles → Create role**.
2. **Trusted entity type:** AWS service → **Use case:** **Glue** ("Allow Glue to call AWS services on your behalf") → **Next**.
3. **Permissions:** search for and tick **AmazonS3FullAccess** → **Next**.
4. **Role name:** `AWS-Glue-S3Role` → leave the defaults → **Create role**.

If the role already exists in your account (the solution video had one), skip this step.

✅ **Check:** the role appears in the list; its **Trust relationships** tab shows `glue.amazonaws.com`.

---

## 4. Create the Glue Job

1. **AWS Glue → ETL jobs** (left menu). Delete any leftover demo job if you want a clean slate.
2. Choose **Script editor** → **Spark** engine → **Start fresh** → **Create script**.
3. The editor pre-fills the imports, args, contexts, and `job.init` / `job.commit`. Paste **only your logic** (the `# --- our code goes here ---` block) **between `job.init(...)` and `job.commit()`**.
4. **Save**.

✅ **Check:** the script has exactly one `job.init` and one `job.commit`, with your code between them.

---

## 5. Configure Job Details

On the **Job details** tab:

| Field | Value |
|---|---|
| Name | `glue-exercise-job` |
| Description | (blank) |
| IAM role | `AWS-Glue-S3Role` |
| Glue version | Latest offered |
| Worker type | Smallest offered (e.g. G.1X) |
| Requested number of workers | **2** |
| Number of retries | 0 (fine for a test) |

Leave everything else as default → **Save** → "Successfully updated job".

✅ **Check:** the role field shows your role, not blank.

---

## 6. Run and Monitor

1. **Run**.
2. Open the **Runs** tab (or **Run details**). Status goes *Starting → Running → Succeeded*. The solution run took about a minute, since it's a larger dataset than the demo.
3. Refresh periodically. **Capacity** should show **2 DPUs**.

✅ **Check:** status **Succeeded**.

---

## 7. Verify

- [ ] S3 → your bucket → `output/` contains one or more `part-*.snappy.parquet` files (plus maybe a `_SUCCESS` marker).
- [ ] The run status is **Succeeded**, with no errors in the run's CloudWatch logs.
- [ ] *(Optional, stronger)* Query the output with **S3 Select** or **Athena**: the dropped column is absent and the row count is **12,654**.

---

## 8. Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `AccessDenied` reading or writing S3 | Wrong or missing IAM role on the job | Job details → IAM role = `AWS-Glue-S3Role`; the role has S3 access |
| `Path does not exist` | Input URI typo, or it points at a folder | Re-copy the **object's** S3 URI |
| `NameError` on a function | Missing PySpark import | Add `from pyspark.sql.functions import …` |
| Job fails at the end | Leftover `spark.stop()`, or output outside writable buckets | Use `job.commit()`; write within your bucket |
| Job won't start / capacity error | Too many workers for the sandbox | Smallest worker type, 2 workers |
| Output has a `value` column of strings | Schema inferred as string | Fine for this lab; for analysis, cast `value` to double |
| Column still present | Name mismatch (case-sensitive) | Match the header exactly (`unit`, not `Unit`) |

---

## 9. Cleanup

1. **Glue → ETL jobs →** select the job → **Actions → Delete job** (if you won't rerun it).
2. **S3 →** delete the `output/` files if the course doesn't need them.
3. Leave the IAM role if Lesson 2 might reuse it; otherwise **IAM → Roles →** delete `AWS-Glue-S3Role`.

There are no running resources after the job finishes. Glue only bills while a run is active.

---

## 10. Optional – CLI Equivalent

```bash
aws s3 cp glue_job.py s3://<your-bucket>/scripts/glue_job.py

aws glue create-job --name glue-exercise-job \
  --role AWS-Glue-S3Role \
  --command Name=glueetl,ScriptLocation=s3://<your-bucket>/scripts/glue_job.py,PythonVersion=3 \
  --glue-version 4.0 --worker-type G.1X --number-of-workers 2

aws glue start-job-run --job-name glue-exercise-job
aws glue get-job-runs --job-name glue-exercise-job --max-items 1
```

Use the latest Glue version your Region offers instead of `4.0` if it's newer.
