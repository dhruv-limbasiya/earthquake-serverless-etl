import boto3

dynamodb = boto3.resource("dynamodb")

table = dynamodb.Table("weather_records")


def save_record(record):

    try:

        table.put_item(
            Item=record
        )

        return True

    except Exception as e:

        print("=" * 50)
        print("Weather Loader Error")
        print(e)
        print("=" * 50)

        return False