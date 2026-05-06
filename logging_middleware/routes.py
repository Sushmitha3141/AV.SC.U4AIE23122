from fastapi import APIRouter
from .auth import register_student, get_access_token
from .logger import Log
from .models import RegisterRequest, AuthRequest, LogRequest

router = APIRouter()


@router.get("/")
def home():
    Log("backend", "info", "route", "logging middleware home route opened")
    return {
        "message": "Logging middleware app is running",
        "routes": ["/register", "/auth", "/test-log"],
    }


@router.post("/register")
def register_api(student: RegisterRequest):
    Log("backend", "info", "route", "registration route started for student client credentials")
    return register_student(student.dict())


@router.post("/auth")
def auth_api(student: AuthRequest):
    Log("backend", "info", "route", "auth route started for bearer token generation")
    return get_access_token(student.dict())


@router.post("/test-log")
def test_log(log_data: LogRequest):
    result = Log(log_data.stack, log_data.level, log_data.package, log_data.message)
    return {
        "message": "log request completed",
        "log_api_response": result,
    }
