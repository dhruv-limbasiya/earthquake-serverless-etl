import json


def parse_json(file_content):
    """
    Parse Earthquake JSON file.
    """

    data = json.loads(file_content)

    if "features" not in data:

        raise Exception(
            "Invalid Earthquake JSON."
        )

    return data["features"]