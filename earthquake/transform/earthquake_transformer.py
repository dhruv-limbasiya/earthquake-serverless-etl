from datetime import datetime
from decimal import Decimal


def transform_record(record):
    """
    Transform one earthquake record into a clean record.
    Returns None if validation fails.
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
        # Severity
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

        print(f"Transformation Error : {e}")

        return None