import json
import boto3

from weather.parsers.weather_parser import parse_weather
from weather.transform.weather_transformer import transform_record
from weather.loaders.weather_loader import save_record

s3 = boto3.client("s3")


def lambda_handler(event, context):

    bucket = event["Records"][0]["s3"]["bucket"]["name"]

    key = event["Records"][0]["s3"]["object"]["key"]

    print("=" * 60)
    print("WEATHER ETL")
    print("=" * 60)

    print(f"Bucket : {bucket}")
    print(f"Key    : {key}")

    response = s3.get_object(

        Bucket=bucket,

        Key=key

    )

    file_content = response["Body"].read().decode("utf-8")

    record = parse_weather(file_content)

    transformed = transform_record(record)

    if transformed is None:

        raise Exception("Transformation Failed")

    if not save_record(transformed):

        raise Exception("DynamoDB Insert Failed")

    print("=" * 60)
    print("Weather Record Saved")
    print("=" * 60)
    print(transformed)

    return {

        "statusCode": 200,

        "body": json.dumps({

            "message": "Weather ETL Completed"

        })

    }