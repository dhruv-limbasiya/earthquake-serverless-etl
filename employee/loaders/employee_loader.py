import boto3

# DynamoDB
dynamodb = boto3.resource("dynamodb")

table = dynamodb.Table("employee_records")


def save_record(record):
    """
    Save one employee record into DynamoDB.
    """

    try:

        table.put_item(
            Item=record
        )

        return True

    except Exception as e:

        print("=" * 50)
        print("Employee Loader Error")
        print(e)
        print("=" * 50)

        return False