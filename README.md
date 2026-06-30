# 🌍 Earthquake Serverless ETL Pipeline with CI/CD

## Project Overview

This project demonstrates a real-world Serverless ETL (Extract, Transform, Load) pipeline built on AWS using earthquake data from the United States Geological Survey (USGS).

The pipeline automatically processes earthquake events whenever a raw JSON file is uploaded to Amazon S3. AWS Lambda validates and transforms the data before loading clean records into Amazon DynamoDB. The project also includes GitHub Actions and AWS CodePipeline for Continuous Integration (CI).

---

# Dataset Source

USGS Earthquake API

https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson

Dataset Type:

- Earthquake Events
- GeoJSON Format
- Updated continuously

---

# Scenario

Emergency management systems require recent earthquake information for monitoring and analytics.

This project automatically:

- Collects earthquake data
- Stores raw data in Amazon S3
- Cleans and validates records
- Classifies earthquake severity
- Stores clean records inside DynamoDB
- Logs ETL execution details in CloudWatch

---

# Architecture

```
                   USGS Earthquake API
                           │
                           ▼
                  earthquake.json
                           │
                           ▼
                 Amazon S3 (raw/)
                           │
                     S3 Event Trigger
                           │
                           ▼
                   AWS Lambda ETL
                           │
        ┌──────────────────┴──────────────────┐
        │                                     │
        ▼                                     ▼
 Amazon DynamoDB                    CloudWatch Logs
 Clean Records                       Audit Summary
```

---

# AWS Services Used

- Amazon S3
- AWS Lambda
- Amazon DynamoDB
- Amazon CloudWatch
- AWS IAM
- GitHub
- GitHub Actions
- AWS CodeBuild
- AWS CodePipeline

---

# ETL Rules

## Extract

- Read raw GeoJSON file from Amazon S3.
- Parse earthquake features.

## Transform

Validation

- Reject records without ID.
- Reject records without magnitude.
- Reject records without place.
- Reject records without timestamp.
- Reject records with invalid coordinates.

Standardization

- Trim place names.
- Convert status to lowercase.
- Convert numeric values to Decimal.
- Format timestamps into UTC.

Derived Field

Severity is generated automatically.

| Magnitude | Severity |
|-----------|----------|
| <2 | Micro |
| 2-3.9 | Minor |
| 4-4.9 | Light |
| 5-5.9 | Moderate |
| 6-6.9 | Strong |
| ≥7 | Major |

---

# DynamoDB Table Design

Table Name

```
earthquake_records
```

Partition Key

```
record_id (String)
```

Attributes

- record_id
- magnitude
- place
- status
- tsunami
- latitude
- longitude
- depth
- severity
- event_time

Capacity Mode

```
On Demand
```

---

# Testing Steps

## Test 1

Upload earthquake.json to

```
s3://earthquake--etl--bucket/raw/
```

Expected Result

Lambda is triggered automatically.

---

## Test 2

Open CloudWatch Logs.

Expected Result

Audit summary should appear.

---

## Test 3

Open DynamoDB.

Expected Result

Clean earthquake records should be inserted.

---

## Test 4

Push code to GitHub.

```
git add .
git commit -m "Test CI"
git push origin master
```

Expected Result

GitHub Actions executes successfully.

---

## Test 5

Open AWS CodePipeline.

Expected Result

Source stage succeeds.

Build stage succeeds.

---

# GitHub Actions Summary

GitHub Actions automatically runs on every Push and Pull Request.

Workflow Steps

- Checkout Repository
- Setup Python 3.11
- Install Dependencies
- Validate Lambda Syntax

---

# AWS CodePipeline Summary

Pipeline Name

```
earthquake-serverless-pipeline
```

Stages

- GitHub Source
- AWS CodeBuild Build

Whenever code is pushed to GitHub:

GitHub

↓

AWS CodePipeline

↓

AWS CodeBuild

↓

Python Validation

↓

Build Success

---

# ETL Flow

1. Fetch earthquake data from the USGS Earthquake API.

2. Save the raw GeoJSON file.

3. Upload the file into the Amazon S3 `raw/` folder.

4. Amazon S3 automatically triggers the Lambda function.

5. Lambda reads the uploaded JSON file.

6. Lambda validates every earthquake record.

7. Invalid records are rejected.

8. Valid records are standardized.

9. Severity is calculated from earthquake magnitude.

10. Clean records are written into Amazon DynamoDB.

11. Lambda logs ETL statistics to Amazon CloudWatch.

---

# Repository Structure

```
earthquake-serverless-etl
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── screenshots/
│
├── sampleData/
│   └── earthquake.json
│
├── lambda_function.py
├── requirements.txt
├── buildspec.yml
├── fetch_data.py
├── README.md
└── .gitignore
```

---

# Screenshots

- Amazon S3 Bucket
- Lambda Success
- CloudWatch Logs
- DynamoDB Records
- GitHub Actions
- AWS CodePipeline
