from fastapi import FastAPI
from .routes import router

app = FastAPI(title="Logging Middleware")

app.include_router(router)

