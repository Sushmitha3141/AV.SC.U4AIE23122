import os
import requests
from dotenv import load_dotenv
from pathlib import Path
from logging_middleware.logger import BASE_URL, Log

load_dotenv(
    dotenv_path=Path(__file__).resolve().parent.parent / ".env"
)


def fetch_notifications():
    token = os.getenv("ACCESS_TOKEN", "").strip()
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(BASE_URL + "/notifications", headers=headers, timeout=15)
        if response.status_code == 200:
            Log("backend", "info", "service", "notifications api fetch success for priority inbox")
        else:
            Log("backend", "warn", "service", "notifications api returned non success status for priority inbox")
        return response.json()
    except requests.exceptions.RequestException:
        Log("backend", "error", "service", "notifications api failed while fetching priority inbox data")
        return {"notifications": []}
