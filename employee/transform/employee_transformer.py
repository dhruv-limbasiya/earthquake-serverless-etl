from decimal import Decimal


def transform_record(record):

    try:

        return {

            "employee_id": record["employee_id"],

            "name": record["name"],

            "department": record["department"],

            "salary": Decimal(str(record["salary"])),

            "city": record["city"]

        }

    except Exception as e:

        print(f"Employee Transform Error : {e}")

        return None