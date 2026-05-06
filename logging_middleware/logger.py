import os
import requests
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(
    dotenv_path=Path(__file__).resolve().parent.parent / ".env"
)
BASE_URL = os.getenv("BASE_URL", "http://20.207.122.201/evaluation-service")

valid_stacks = ["backend", "frontend"]
valid_levels = ["debug", "info", "warn", "error", "fatal"]
valid_backend_packages = [
    "cache",
    "controller",
    "cron_job",
    "db",
    "domain",
    "handler",
    "repository",
    "route",
    "service",
    "auth",
    "config",
    "middleware",
    "utils",
]


def Log(stack, level, package, message):
    if stack not in valid_stacks:
        return {"error": "invalid stack value"}

    if level not in valid_levels:
        return {"error": "invalid level value"}

    if stack == "backend" and package not in valid_backend_packages:
        return {"error": "invalid backend package value"}

    token = os.getenv("ACCESS_TOKEN", "").strip()
    if token == "":
        return {"error": "ACCESS_TOKEN not found in .env"}

    body = {
        "stack": stack,
        "level": level,
        "package": package,
        "message": message,
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(BASE_URL + "/logs", json=body, headers=headers, timeout=10)
        return response.json()
    except requests.exceptions.RequestException as error:
        return {"error": "log api call failed", "details": str(error)}
