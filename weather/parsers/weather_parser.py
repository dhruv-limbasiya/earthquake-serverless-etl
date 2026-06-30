import json


def parse_weather(file_content):

    data = json.loads(file_content)

    return {

        "timestamp": data["current"]["time"],

        "temperature": data["current"]["temperature_2m"],

        "wind_speed": data["current"]["wind_speed_10m"]

    }