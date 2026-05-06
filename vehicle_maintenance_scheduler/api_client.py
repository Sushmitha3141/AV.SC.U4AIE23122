import os
import requests
from dotenv import load_dotenv
from logging_middleware.logger import BASE_URL, Log

from pathlib import Path

load_dotenv(
    dotenv_path=Path(__file__).resolve().parent.parent / ".env"
)


def get_headers():
    token = os.getenv("ACCESS_TOKEN", "").strip()
    return {
        "Authorization": f"Bearer {token}"
    }

def fetch_depots():
    try:
        response = requests.get(
            BASE_URL + "/depots",
            headers=get_headers(),
            timeout=15
        )

        if response.status_code == 200:
            Log("backend", "info", "service", "depot api fetch success for mechanic hours")
        else:
            Log("backend", "warn", "service", "depot api returned non success status while fetching capacity")

        return response.json()

    except requests.exceptions.RequestException as error:
        Log("backend", "error", "service", "depot api failed while fetching mechanic hours")
        return {"depots": []}

def fetch_vehicles():
    try:
        response = requests.get(BASE_URL + "/vehicles", headers=get_headers(), timeout=15)
        if response.status_code == 200:
            Log("backend", "info", "service", "vehicles api fetch success for maintenance tasks")
        else:
            Log("backend", "warn", "service", "vehicles api returned non success status while fetching tasks")
        return response.json()
    except requests.exceptions.RequestException:
        Log("backend", "error", "service", "vehicles api failed while fetching maintenance tasks")
        return {"vehicles": []}
