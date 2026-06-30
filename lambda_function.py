import json
import boto3
from datetime import datetime
from decimal import Decimal

# AWS Clients
s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")

# DynamoDB Table
table = dynamodb.Table("earthquake_records")


def transform_record(record):
    """
    Transform one raw earthquake record into a clean record.
    Returns None if the record is invalid.
    """

    try:
        properties = record.get("properties", {})
        geometry = record.get("geometry", {})
        coordinates = geometry.get("coordinates", [])

        # ----------------------------
        # Validation
        # ----------------------------
        if record.get("id") is None:
            return None

        if properties.get("mag") is None:
            return None

        if properties.get("place") is None:
            return None

        if properties.get("time") is None:
            return None

        if len(coordinates) < 3:
            return None

        # ----------------------------
        # Standardization
        # ----------------------------
        record_id = record["id"]

        magnitude = Decimal(str(properties["mag"]))

        place = properties["place"].strip()

        status = properties.get("status", "unknown").lower()

        tsunami = int(properties.get("tsunami", 0))

        longitude = Decimal(str(coordinates[0]))

        latitude = Decimal(str(coordinates[1]))

        depth = Decimal(str(coordinates[2]))

        event_time = datetime.utcfromtimestamp(
            properties["time"] / 1000
        ).strftime("%Y-%m-%d %H:%M:%S")

        # ----------------------------
        # Derived Field
        # ----------------------------
        if magnitude < Decimal("2"):
            severity = "Micro"

        elif magnitude < Decimal("4"):
            severity = "Minor"

        elif magnitude < Decimal("5"):
            severity = "Light"

        elif magnitude < Decimal("6"):
            severity = "Moderate"

        elif magnitude < Decimal("7"):
            severity = "Strong"

        else:
            severity = "Major"

        return {

            "record_id": record_id,
            "magnitude": magnitude,
            "place": place,
            "status": status,
            "tsunami": tsunami,
            "longitude": longitude,
            "latitude": latitude,
            "depth": depth,
            "event_time": event_time,
            "severity": severity

        }

    except Exception as e:

        print(f"Transformation Error: {e}")

        return None


def lambda_handler(event, context):

    # ----------------------------
    # Read S3 Event
    # ----------------------------
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]

    print(f"Bucket : {bucket}")
    print(f"File   : {key}")

    # ----------------------------
    # Extract
    # ----------------------------
    response = s3.get_object(
        Bucket=bucket,
        Key=key
    )

    file_content = response["Body"].read().decode("utf-8")

    data = json.loads(file_content)

    earthquakes = data["features"]

    # ----------------------------
    # Audit Counters
    # ----------------------------
    total_records = len(earthquakes)
    inserted_records = 0
    rejected_records = 0

    # ----------------------------
    # Transform + Load
    # ----------------------------
    for record in earthquakes:

        transformed = transform_record(record)

        if transformed is None:

            rejected_records += 1
            continue

        try:

            table.put_item(
                Item=transformed
            )

            inserted_records += 1

        except Exception as e:

            print(f"DynamoDB Insert Error : {e}")

            rejected_records += 1

    # ----------------------------
    # Audit Summary
    # ----------------------------
    print("=" * 50)
    print("ETL SUMMARY")
    print("=" * 50)
    print(f"Total Records     : {total_records}")
    print(f"Inserted Records  : {inserted_records}")
    print(f"Rejected Records  : {rejected_records}")
    print(f"Execution Time    : {datetime.utcnow()}")
    print("=" * 50)

    return {

        "statusCode": 200,

        "body": json.dumps({

            "message": "ETL Completed Successfully",

            "total_records": total_records,

            "inserted_records": inserted_records,

            "rejected_records": rejected_records

        })

    }