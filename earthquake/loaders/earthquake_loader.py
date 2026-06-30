import boto3

from earthquake.config.settings import DYNAMODB_TABLE

# DynamoDB Client
dynamodb = boto3.resource("dynamodb")

table = dynamodb.Table(DYNAMODB_TABLE)


def save_record(record):
    """
    Save one transformed earthquake record into DynamoDB.
    """

    try:

        table.put_item(Item=record)

        return True

    except Exception as e:

        print("=" * 50)
        print("DynamoDB Insert Error")
        print(e)
        print("=" * 50)

        return False