# Backend Track Campus Hiring Assessment

This is a simple FastAPI based backend project for the campus hiring assessment.

## Setup

Install packages:

```bash
pip install -r requirements.txt
```

Create `.env` from `.env.example` and fill the details.

First run registration only once:

```bash
uvicorn logging_middleware.main:app --reload --port 8000
```

Postman:

```http
POST http://127.0.0.1:8000/register
POST http://127.0.0.1:8000/auth
POST http://127.0.0.1:8000/test-log
```

After auth, paste the received access token in `.env` as `ACCESS_TOKEN`.

## Vehicle Maintenance Scheduler

Run:

```bash
uvicorn vehicle_maintenance_scheduler.main:app --reload --port 8001
```

Postman:

```http
GET http://127.0.0.1:8001/schedule-maintenance
```

This fetches depot and vehicle data from the protected APIs and solves the 0/1 knapsack problem.

## Notification Priority Inbox

Run:

```bash
uvicorn notification_app_be.main:app --reload --port 8002
```

Postman:

```http
GET http://127.0.0.1:8002/priority-inbox
```

This fetches notifications from the protected API and returns top 10 unread notifications using heap logic.

## Design Answer

The system design answer is written in:

```text
notification_system_design.md
```

"# AV.SC.U4AIE23122" 
