from decimal import Decimal


def transform_record(record):

    try:

        return {

            "timestamp": record["timestamp"],

            "temperature": Decimal(str(record["temperature"])),

            "wind_speed": Decimal(str(record["wind_speed"]))

        }

    except Exception as e:

        print(e)

        return None