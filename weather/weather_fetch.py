import requests
import json

URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=52.52"
    "&longitude=13.41"
    "&current=temperature_2m,wind_speed_10m"
    "&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
)

response = requests.get(URL)

response.raise_for_status()

data = response.json()

with open("./sampleData/weather.json", "w") as f:
    json.dump(data, f, indent=4)

print("Weather JSON downloaded successfully.")