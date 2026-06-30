import os

from earthquake.config.settings import (
    EARTHQUAKE_FOLDER,
    WEATHER_FOLDER,
    EMPLOYEE_FOLDER
)


def detect_file_type(key):

    key = key.lower()

    # Folder Based Detection

    if key.startswith(EARTHQUAKE_FOLDER):
        return "earthquake"

    if key.startswith(WEATHER_FOLDER):
        return "weather"

    if key.startswith(EMPLOYEE_FOLDER):
        return "employee"

    # Extension Fallback

    extension = os.path.splitext(key)[1].lower()

    if extension == ".json":
        return "earthquake"

    elif extension == ".csv":
        return "weather"

    elif extension in [".xlsx", ".xls"]:
        return "employee"

    raise Exception(f"Unsupported File : {key}")