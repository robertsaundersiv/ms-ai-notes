---
title: "Enhancing Data Processing with Redshift, EMR, and Athena – Flashcards"
course: AWS Cloud Architect – Designing AWS Architecture for Workloads
type: flashcards
source: "[[Enhancing Data Processing with Redshift, EMR, and Athena]]"
created: 2026-10-19
---

#flashcards/aws/workloads/data-processing

Flashcards for [[Enhancing Data Processing with Redshift, EMR, and Athena]].

What is Amazon Redshift?
?
A fully managed, petabyte-scale data warehouse optimized for analyzing large datasets with SQL-based tools.

Which two architectural features make Redshift an optimized data warehouse?
?
Massively parallel processing and columnar data storage.

When does the lecture recommend integrating Amazon Redshift?
?
To enable business intelligence on existing data warehouses, or to apply machine learning to data in existing data warehouses.

What benefits does Amazon Redshift bring to applications?
?
Low-latency analytics queries, and a serverless option where you pay only for what you use with auto scaling.

What is Amazon EMR?
?
A managed big-data platform that processes vast amounts of data with open-source tools such as Apache Spark, Hive, and Presto.

When does the lecture recommend integrating Amazon EMR?
?
To optimize existing ETL pipelines, especially those already using Spark and Hadoop, or to scale a pipeline to terabyte-scale big data.

What benefits does Amazon EMR provide over a self-managed cluster of EC2 instances?
?
Automated dynamic scaling up and back down, and minimal server management.

What is Amazon Athena?
?
A serverless query service that analyzes data stored in S3 using standard SQL, priced per query.

When does the lecture recommend Amazon Athena?
?
When vast datasets in S3 hold business value to extract, or to quickly analyze large volumes of logs stored in S3.

What are the steps to query data with Athena?
?
Point to the S3 data source, set an S3 location for query output, create the database and table, then run SQL queries.

What must you configure in Athena before running queries?
?
A query result location in S3 where Athena writes the query output.

Why can a CSV queried in Athena show values in the wrong columns?
?
Quoted fields that contain commas are split by a plain comma delimiter, shifting later columns. A CSV parser that handles quotes (OpenCSVSerDe) fixes this.

How do partitioning and columnar formats reduce Athena cost?
?
Athena charges per data scanned, so they reduce the bytes each query reads.

How do Amazon EMR and AWS Glue differ for Spark workloads?
?
Glue is serverless, with no cluster to manage. EMR provides a managed cluster with more control and more frameworks, such as Hive and Presto.
