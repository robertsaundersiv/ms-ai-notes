---
title: "Exercise 2 – Query S3 Data with Amazon Athena – How To"
aliases:
  - L3 Exercise 2 How To
  - Athena Netflix Titles Exercise
course: AWS Cloud Architect – Designing AWS Architecture for Workloads
lessons:
  - C2-L3 Athena Demo (L2 D1)
  - C2-L3 Exercise Solution (L2 E1)
type: how-to
created: 2026-10-19
related:
  - "[[Enhancing Data Processing with Redshift, EMR, and Athena]]"
  - "[[Exercise 1 - Assessing and Optimizing Workloads - How To]]"
  - "[[Exercise 3 - Deploy FastAPI on Amazon ECS with Fargate - How To]]"
tags:
  - aws/athena
  - aws/s3
  - aws/lab
  - how-to
---

# Exercise 2 – Query S3 Data with Amazon Athena – How To

> [!abstract] Goal
> 1. Get the Kaggle **Netflix titles** dataset (`netflix_titles.csv`) into S3.
> 2. Configure **Amazon Athena**: source and output locations, database `movies`, the provided `netflix_titles` table.
> 3. Run the query for the ==average release year for each rating==.
>
> Your result must match the grader's test script on the **raw, uncleaned** data. It takes about 20 minutes and costs fractions of a cent.

**Concepts:** [[Enhancing Data Processing with Redshift, EMR, and Athena]] · **Other labs:** [[Exercise 1 - Assessing and Optimizing Workloads - How To|Exercise 1]] · [[Exercise 3 - Deploy FastAPI on Amazon ECS with Fargate - How To|Exercise 3]]
**Sources:** the course repo `lesson-3-managed-services/exercise 2/starter/`, which has `athena_exercise_instructions.md`, `athena_query.sql`, `athena-exercise-setup.yaml`, and `athena_exercise_setup_params.json`. Also the Athena demo and solution videos.

> [!danger] Don't run the repo's CloudFormation setup as-is
> `athena-exercise-setup.yaml` with `athena_exercise_setup_params.json` will fail or behave badly, for five reasons:
> 1. **Parameter mismatch:** the params file passes **`TimeStamp`**, which the template doesn't declare, so `create-stack` fails immediately. The `$(date …)` text in the JSON also isn't expanded.
> 2. **Deprecated runtime:** the dataset-download Lambda uses **`python3.8`**, which AWS no longer accepts for new functions.
> 3. **Public write access:** two bucket policies grant `s3:PutObject` to **`Principal: "*"`**, so anyone on the internet could upload. S3 Block Public Access rejects this by default, so the stack fails. If it didn't, it would be a security hole.
> 4. **Fragile download:** the Lambda pip-installs the Kaggle CLI at runtime and sends no failure response, so a failure can leave the stack **hanging for an hour**.
> 5. **Cloud9:** the instructions use it, but AWS has closed it to new customers. Use **CloudShell** for CLI work.
>
> The **manual path below** gets the same result, and your Kaggle API key never goes into AWS.

---

## 0. Before You Start

- [ ] A free **Kaggle** account. The dataset is **`shivamb/netflix-shows`** ("Netflix Movies and TV Shows").
- [ ] Region selector = **us-east-1** (Cloud Lab default) for S3 and Athena
- [ ] Cloud Lab rule: **no personal information** in bucket names or tags

The repo's layout is **one bucket** with two prefixes:

| Prefix | Use |
|---|---|
| `s3://athena-exercise-bucket-<suffix>/input/` | Source: `netflix_titles.csv` |
| `s3://athena-exercise-bucket-<suffix>/output/` | Athena query results |

---

## 1. Get the Data into S3 (Manual Path)

1. In a browser, sign in to Kaggle → dataset **Netflix Movies and TV Shows** (`shivamb/netflix-shows`) → **Download**. Unzip to get **`netflix_titles.csv`**.
2. **S3 → Create bucket** → `athena-exercise-bucket-<random digits>` (us-east-1). Keep **Block all public access** on. → **Create**.
3. Open the bucket → **Create folder** `input` → upload `netflix_titles.csv` into `input/`.
4. **Create folder** `output`.

> [!tip] If you prefer CloudShell
> Upload the CSV with **Actions → Upload file** in CloudShell, then run:
> ```bash
> aws s3 mb s3://athena-exercise-bucket-<random> --region us-east-1
> aws s3 cp netflix_titles.csv s3://athena-exercise-bucket-<random>/input/netflix_titles.csv
> ```

---

## 2. Set the Query Result Location

1. **Athena → Query editor** → **Settings** tab → **Manage**.
2. **Location of query result:** `s3://athena-exercise-bucket-<random>/output/` → **Save**.
3. Back to the **Editor** tab. The demo shows a warning about an old bucket that doesn't exist until this is set.

---

## 3. Create the Database and the Provided Table

```sql
CREATE DATABASE movies;
```

Select **Database: `movies`** in the left panel. Then run the repo's **`athena_query.sql`**, with only the `LOCATION` changed to your `input/` folder:

```sql
CREATE EXTERNAL TABLE netflix_titles (
    show_id STRING,
    type STRING,
    title STRING,
    director STRING,
    `cast` STRING,
    country STRING,
    date_added DATE,
    release_year INT,
    rating STRING,
    duration STRING,
    listed_in STRING,
    description STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LOCATION 's3://athena-exercise-bucket-<random>/input/'
TBLPROPERTIES ('skip.header.line.count'='1');
```

> [!note] Two small things about the provided DDL
> - **`cast`** is wrapped in backticks here. It can clash with the SQL `CAST` keyword, and the backticks are harmless if it doesn't.
> - **`LOCATION` must be the folder** (`…/input/`), not the file. Athena reads every file under the prefix.

> [!important] Why this table gives "messy" results, and why you should keep it anyway
> `FIELDS TERMINATED BY ','` doesn't understand **quoted fields** such as `"Kate Siegel, Zach Gilford"` or `"United States, India"`. Those rows split into extra columns, so later columns **shift**. That's why the demo showed names in the country column, and odd values (durations, dates) as "ratings". The grader's expected results come from **this exact table definition**, so use it for the graded query. Option B in section 5 shows the correct parse.

---

## 4. Run the Queries

**Demo checks:**

```sql
SELECT type, COUNT(*) AS title_count
FROM netflix_titles
GROUP BY type
ORDER BY title_count DESC;
```

Expect **6,131 Movie** and **2,676 TV Show**. `type` is the 2nd column, before any quoted fields, so it doesn't shift.

```sql
SELECT country, COUNT(*) AS content_count
FROM netflix_titles
GROUP BY country
ORDER BY content_count DESC
LIMIT 10;
```

**The exercise query: average release year for each rating:**

```sql
SELECT rating,
       AVG(release_year) AS avg_release_year
FROM netflix_titles
GROUP BY rating
ORDER BY rating;
```

> [!success] Matches the solution video if…
> …you see **TV-PG → 1944.0** among the results. Strange rating values are expected: ==the exercise doesn't expect you to clean the data==, only to match the test script on the raw table.

---

## 5. Optional – See What Correct Parsing Changes

```sql
CREATE EXTERNAL TABLE netflix_titles_clean (
  show_id string, type string, title string, director string, cast_list string,
  country string, date_added string, release_year string, rating string,
  duration string, listed_in string, description string
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES ('separatorChar' = ',', 'quoteChar' = '"')
LOCATION 's3://athena-exercise-bucket-<random>/input/'
TBLPROPERTIES ('skip.header.line.count'='1');

SELECT rating,
       ROUND(AVG(TRY_CAST(release_year AS double)), 1) AS avg_release_year
FROM netflix_titles_clean
GROUP BY rating
ORDER BY rating;
```

The ratings become the real set (TV-MA, TV-14, PG-13, …) and the averages become plausible. Comparing the two outputs is the practical lesson: **check parsing before trusting results** ([[Enhancing Data Processing with Redshift, EMR, and Athena#6. Lab Walkthrough – Exercise 2 Athena]]).

---

## 6. Verify the Whole Exercise

- [ ] Bucket with `input/netflix_titles.csv` and an `output/` prefix
- [ ] Athena **query result location** = `…/output/`
- [ ] Database **`movies`**; table **`netflix_titles`** from the provided DDL, `LOCATION …/input/`
- [ ] Counts: 6,131 movies, 2,676 TV shows
- [ ] Average release year by rating, including **TV-PG ≈ 1944.0**
- [ ] Result files appear under `output/`

---

## 7. Troubleshooting

| Problem | Likely cause | Fix |
|---|---|---|
| `create-stack` fails: parameter `TimeStamp` doesn't exist | Repo params file mismatch | Use the manual path (or delete that entry) |
| Stack fails on the bucket policy | Public `PutObject` blocked by S3 Block Public Access | Manual path. Don't make the bucket public. |
| Stack fails creating the Lambda | `python3.8` runtime no longer accepted | Manual path |
| "No output location provided" | Result location not set | **Settings → Manage** → `…/output/` |
| Table returns 0 rows | `LOCATION` is the file or a wrong prefix | Use `s3://…/input/` |
| Syntax error near `cast` | Reserved-word clash | Backticks: `` `cast` `` |
| `date_added` is all NULL | Values like "September 25, 2021" aren't DATE literals | Expected. Not used by the exercise query. |
| Results differ from the grader | Graded query run on the quote-aware table | Run it on **`netflix_titles`** |

---

## 8. Cleanup

1. `DROP TABLE netflix_titles;` (and `netflix_titles_clean`), then `DROP DATABASE movies;`
2. **Empty**, then **delete** the bucket.
3. If you did run the repo stack: **delete the stack**. If it's stuck in `CREATE_IN_PROGRESS`, it will time out after about an hour, then delete it.
