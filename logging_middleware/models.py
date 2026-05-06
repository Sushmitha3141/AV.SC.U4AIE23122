from pydantic import BaseModel


class RegisterRequest(BaseModel):
    email: str
    name: str
    mobileNo: str
    githubUsername: str
    rollNo: str
    accessCode: str


class AuthRequest(BaseModel):
    email: str
    name: str
    rollNo: str
    accessCode: str
    clientID: str
    clientSecret: str


class LogRequest(BaseModel):
    stack: str
    level: str
    package: str
    message: str

