import requests
from datetime import datetime
import os

APP_ID = os.environ.get("APP_ID")
API_KEY = os.environ.get("API_KEY")
AGE = 24
GENDER = "Male"
WEIGHT_KG = 68.04
HEIGHT_CM = 178


exercise_endpoint = os.environ.get("EXERCISE_ENDPOINT")
sheet_endpoint = os.environ.get("SHEET_ENDPOINT")

exercise_text = input("Tell me what exercises you did: ")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

parameters = {
    "query": exercise_endpoint,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE,
}


response = requests.post(url=exercise_endpoint, json=parameters, headers=headers)
result = response.json()

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"],
        }
    }

    sheet_response = requests.post(url=sheet_endpoint, json=sheet_inputs, auth=(os.environ.get("AUTH_USER"), os.environ.get("AUTH_PASS")))
    print(sheet_response.text)
