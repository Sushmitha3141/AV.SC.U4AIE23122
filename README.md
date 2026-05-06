# AV.SC.U4AIE23122

Backend Track Campus Hiring Assessment using FastAPI.

## Project Structure

* logging_middleware
* vehicle_maintenance_scheduler
* notification_app_be
* notification_system_design.md

## Install Requirements

```bash
pip install -r requirements.txt
```

## Create .env File

Copy values from `.env.example` to `.env`

Fill:

* email
* name
* mobile number
* GitHub username
* roll number
* access code
* client ID
* client secret
* access token

## Logging Middleware

Run:

```bash
python -m uvicorn logging_middleware.main:app --reload --port 8000
```

Used for:

* registration
* authentication
* logging API testing

Main endpoints:

* /register
* /auth
* /test-log

## Vehicle Maintenance Scheduler

Run:

```bash
python -m uvicorn vehicle_maintenance_scheduler.main:app --reload --port 8001
```

Main endpoint:

* /schedule-maintenance

This fetches depot and vehicle data and selects the best maintenance tasks using 0/1 knapsack logic.

## Notification Priority Inbox

Run:

```bash
python -m uvicorn notification_app_be.main:app --reload --port 8002
```

Main endpoint:

* /priority-inbox

This fetches notifications and returns top 10 unread notifications using heap priority logic.

## System Design

Written in:

```text
notification_system_design.md
```
