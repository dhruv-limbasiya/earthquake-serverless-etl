import json
import boto3
from datetime import datetime

from earthquake.parsers.earthquake_parser import parse_json
from earthquake.transform.earthquake_transformer import transform_record
from earthquake.loaders.earthquake_loader import save_record

# AWS S3 Client
s3 = boto3.client("s3")


def lambda_handler(event, context):

    # ----------------------------
    # Read S3 Event
    # ----------------------------
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]

    print("=" * 60)
    print("EARTHQUAKE ETL PIPELINE")
    print("=" * 60)
    print(f"Bucket : {bucket}")
    print(f"Key    : {key}")

    # ----------------------------
    # Download File
    # ----------------------------
    response = s3.get_object(
        Bucket=bucket,
        Key=key
    )

    file_content = response["Body"].read().decode("utf-8")

    # ----------------------------
    # Parse JSON
    # ----------------------------
    records = parse_json(file_content)

    # ----------------------------
    # Audit Counters
    # ----------------------------
    total_records = len(records)

    inserted_records = 0

    rejected_records = 0

    # ----------------------------
    # Transform + Load
    # ----------------------------
    for record in records:

        transformed = transform_record(record)

        if transformed is None:

            rejected_records += 1
            continue

        if save_record(transformed):

            inserted_records += 1

        else:

            rejected_records += 1

    # ----------------------------
    # Audit Summary
    # ----------------------------
    print("=" * 60)
    print("EARTHQUAKE ETL SUMMARY")
    print("=" * 60)
    print(f"Total Records    : {total_records}")
    print(f"Inserted Records : {inserted_records}")
    print(f"Rejected Records : {rejected_records}")
    print(f"Execution Time   : {datetime.utcnow()}")
    print("=" * 60)

    return {

        "statusCode": 200,

        "body": json.dumps({

            "message": "Earthquake ETL Completed Successfully.",

            "total_records": total_records,

            "inserted_records": inserted_records,

            "rejected_records": rejected_records

        })

    }