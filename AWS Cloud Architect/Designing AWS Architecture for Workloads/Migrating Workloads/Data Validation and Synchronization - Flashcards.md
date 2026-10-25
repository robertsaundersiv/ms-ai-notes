---
title: "Data Validation and Synchronization – Flashcards"
course: AWS Cloud Architect – Designing AWS Architecture for Workloads
type: flashcards
source: "[[Data Validation and Synchronization]]"
created: 2026-10-19
---

#flashcards/aws/workloads/data-validation

Flashcards for [[Data Validation and Synchronization]].

Why is data validation described as the most crucial part of a data migration?
?
Because errors in migrated data directly damage customer trust and business operations, not just technical correctness.

What four mistakes did TechCorp make in its database migration?
?
It rushed without planning, skipped pre-migration testing, did not enable DMS data validation, and did no post-migration verification.

What problems did TechCorp suffer after its migration?
?
Orders mismatched with shipping addresses, missing or incomplete customer records, and financial discrepancies between source and target.

What did DataSafe do to make its migration succeed?
?
Planned carefully, tested beforehand, enabled DMS data validation, used custom checksums for critical data, and migrated in phases with validation at each stage.

What were the results of DataSafe's migration?
?
99.99% data accuracy, maintained data integrity and regulatory compliance, and enhanced customer trust through uninterrupted service.

What is a checksum?
?
A string of letters and numbers computed from data's content that acts as a fingerprint for verifying integrity.

Why does a checksum detect changes in data?
?
It's derived from the content, so any change, even one character, produces a completely different checksum.

Which AWS migration and transfer services include built-in validation?
?
AWS DMS, AWS MGN, and AWS DataSync.

Which AWS transfer services require manual checksum validation?
?
AWS Transfer Family and AWS Direct Connect.

Why did TechCorp's use of DMS still produce bad data?
?
DMS data validation is a task setting that must be enabled, and TechCorp never turned it on.

Why can a matching checksum fail to prove a migration was correct?
?
A checksum only proves the target matches the source, so a faithful copy of bad source data still passes.

How many records need reconciliation in a 10-million-record migration that's 99.99% accurate?
?
1,000 records.
