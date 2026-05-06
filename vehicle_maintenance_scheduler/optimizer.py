from logging_middleware.logger import Log


def choose_tasks(vehicles, mechanic_hours):
    Log("backend", "info", "domain", "vehicle maintenance optimization started using knapsack logic")

    n = len(vehicles)
    capacity = int(mechanic_hours)

    dp = []
    for i in range(n + 1):
        row = []
        for j in range(capacity + 1):
            row.append(0)
        dp.append(row)

    for i in range(1, n + 1):
        duration = int(vehicles[i - 1]["Duration"])
        impact = int(vehicles[i - 1]["Impact"])

        for hours in range(capacity + 1):
            if duration <= hours:
                take_task = impact + dp[i - 1][hours - duration]
                skip_task = dp[i - 1][hours]
                dp[i][hours] = max(take_task, skip_task)
            else:
                dp[i][hours] = dp[i - 1][hours]

    selected = []
    hours_left = capacity

    for i in range(n, 0, -1):
        if dp[i][hours_left] != dp[i - 1][hours_left]:
            task = vehicles[i - 1]
            selected.append(task)
            hours_left = hours_left - int(task["Duration"])

    selected.reverse()

    total_duration = 0
    total_impact = 0
    selected_ids = []

    for task in selected:
        selected_ids.append(task["TaskID"])
        total_duration += int(task["Duration"])
        total_impact += int(task["Impact"])

    Log("backend", "info", "domain", "selected vehicle maintenance tasks after optimization")
    Log("backend", "info", "handler", "vehicle maintenance final output prepared with duration and impact")

    return {
        "selectedTaskIDs": selected_ids,
        "totalDuration": total_duration,
        "totalImpact": total_impact,
        "mechanicHours": capacity,
    }

