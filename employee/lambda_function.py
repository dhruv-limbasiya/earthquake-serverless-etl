import json
import boto3

from employee.parsers.employee_parser import parse_employee
from employee.transform.employee_transformer import transform_record
from employee.loaders.employee_loader import save_record

s3 = boto3.client("s3")


def lambda_handler(event, context):

    bucket = event["Records"][0]["s3"]["bucket"]["name"]

    key = event["Records"][0]["s3"]["object"]["key"]

    print("=" * 60)
    print("EMPLOYEE ETL")
    print("=" * 60)

    print(f"Bucket : {bucket}")
    print(f"Key    : {key}")

    response = s3.get_object(
        Bucket=bucket,
        Key=key
    )

    file_content = response["Body"].read().decode("utf-8")

    records = parse_employee(file_content)

    total = len(records)

    inserted = 0

    rejected = 0

    for record in records:

        transformed = transform_record(record)

        if transformed is None:

            rejected += 1

            continue

        if save_record(transformed):

            inserted += 1

        else:

            rejected += 1

    print("=" * 60)
    print("EMPLOYEE SUMMARY")
    print("=" * 60)
    print(f"Total     : {total}")
    print(f"Inserted  : {inserted}")
    print(f"Rejected  : {rejected}")
    print("=" * 60)

    return {

        "statusCode": 200,

        "body": json.dumps({

            "message": "Employee ETL Completed",

            "total_records": total,

            "inserted_records": inserted,

            "rejected_records": rejected

        })

    }