import os
import requests
from dotenv import load_dotenv
from pathlib import Path
from .logger import BASE_URL, Log

load_dotenv(
    dotenv_path=Path(__file__).resolve().parent.parent / ".env"
)


def register_student(data):
    try:
        response = requests.post(BASE_URL + "/register", json=data, timeout=15)
        result = response.json()

        if response.status_code == 200 or response.status_code == 201:
            Log("backend", "info", "auth", "student registration completed and client credentials received")
        else:
            Log("backend", "warn", "auth", "student registration failed or registration was already used")

        return result
    except requests.exceptions.RequestException as error:
        Log("backend", "error", "auth", "registration api failed while requesting client credentials")
        return {"error": str(error)}


def get_access_token(data):
    try:
        response = requests.post(BASE_URL + "/auth", json=data, timeout=15)
        result = response.json()

        if "access_token" in result:
            save_access_token(result["access_token"])
            Log("backend", "info", "auth", "authorization completed and access token received")
        else:
            Log("backend", "warn", "auth", "authorization response did not contain access token")

        return result
    except requests.exceptions.RequestException as error:
        Log("backend", "error", "auth", "authorization api failed while requesting bearer token")
        return {"error": str(error)}


def read_default_student_data():
    return {
        "email": os.getenv("STUDENT_EMAIL", ""),
        "name": os.getenv("STUDENT_NAME", ""),
        "mobileNo": os.getenv("STUDENT_MOBILE", ""),
        "githubUsername": os.getenv("GITHUB_USERNAME", ""),
        "rollNo": os.getenv("ROLL_NO", ""),
        "accessCode": os.getenv("ACCESS_CODE", ""),
    }


def save_access_token(token):
    env_path = Path(__file__).resolve().parent.parent / ".env"
    os.environ["ACCESS_TOKEN"] = token

    if env_path.exists():
        lines = env_path.read_text().splitlines()
    else:
        lines = []

    updated_lines = []
    token_saved = False

    for line in lines:
        if line.startswith("ACCESS_TOKEN="):
            updated_lines.append("ACCESS_TOKEN=" + token)
            token_saved = True
        else:
            updated_lines.append(line)

    if not token_saved:
        updated_lines.append("ACCESS_TOKEN=" + token)

    env_path.write_text("\n".join(updated_lines) + "\n")


def refresh_access_token():
    student_data = read_default_student_data()

    auth_data = {
        "email": student_data["email"],
        "name": student_data["name"],
        "rollNo": student_data["rollNo"],
        "accessCode": student_data["accessCode"],
        "clientID": os.getenv("CLIENT_ID", ""),
        "clientSecret": os.getenv("CLIENT_SECRET", ""),
    }

    result = get_access_token(auth_data)
    return result.get("access_token", "")

if __name__ == "__main__":
    student_data = read_default_student_data()

    auth_data = {
        "email": student_data["email"],
        "name": student_data["name"],
        "rollNo": student_data["rollNo"],
        "accessCode": student_data["accessCode"],
        "clientID": os.getenv("CLIENT_ID"),
        "clientSecret": os.getenv("CLIENT_SECRET")
    }

    print("Getting fresh access token...")
    token_result = get_access_token(auth_data)
    print(token_result)
