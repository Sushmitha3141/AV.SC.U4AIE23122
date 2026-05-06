from fastapi import FastAPI
from logging_middleware.logger import Log
from .api_client import fetch_depots, fetch_vehicles
from .optimizer import choose_tasks

app = FastAPI(title="Vehicle Maintenance Scheduler")


@app.get("/")
def home():
    Log("backend", "info", "route", "vehicle scheduler home route opened")
    return {
        "message": "Vehicle Maintenance Scheduler is running",
        "endpoint": "/schedule-maintenance",
    }


@app.get("/schedule-maintenance")
def schedule_maintenance():
    Log("backend", "info", "route", "schedule maintenance api started")

    depot_data = fetch_depots()
    print("DEPOT DATA =", depot_data)

    vehicle_data = fetch_vehicles()
    print("VEHICLE DATA =", vehicle_data)

    depots = depot_data.get("depots", [])
    vehicles = vehicle_data.get("vehicles", [])

    if len(depots) == 0:
        Log("backend", "error", "handler", "no depot data found while scheduling maintenance tasks")
        return {"error": "No depot data found"}

    if len(vehicles) == 0:
        Log("backend", "error", "handler", "no vehicle task data found while scheduling maintenance tasks")
        return {"error": "No vehicle task data found"}

    mechanic_hours = depots[0]["MechanicHours"]
    answer = choose_tasks(vehicles, mechanic_hours)

    Log("backend", "info", "route", "schedule maintenance api returned optimized task list")
    return answer

