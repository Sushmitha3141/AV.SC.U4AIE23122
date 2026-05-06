from fastapi import FastAPI
from logging_middleware.logger import Log
from .api_client import fetch_notifications
from .priority_inbox import top_unread_notifications

app = FastAPI(title="Campus Notification Priority Inbox")


@app.get("/")
def home():
    Log("backend", "info", "route", "notification app home route opened")
    return {
        "message": "Campus Notification Priority Inbox is running",
        "endpoint": "/priority-inbox",
    }


@app.get("/priority-inbox")
def priority_inbox():
    Log("backend", "info", "route", "priority inbox api started")

    data = fetch_notifications()
    notifications = data.get("notifications", [])

    if len(notifications) == 0:
        Log("backend", "warn", "handler", "no notifications found while preparing priority inbox")
        return {"top10": [], "message": "No notifications found"}

    top_items = top_unread_notifications(notifications, 10)

    Log("backend", "info", "route", "priority inbox api returned top unread notifications")
    return {
        "approach": "Unread notifications are placed in a heap. Placement gets first priority, then Result, then Event. Newer notification comes first inside same type.",
        "top10": top_items,
    }

