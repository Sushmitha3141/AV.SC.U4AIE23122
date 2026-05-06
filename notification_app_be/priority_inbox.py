import heapq
from datetime import datetime
from logging_middleware.logger import Log


priority_value = {
    "Placement": 1,
    "Result": 2,
    "Event": 3,
}


def parse_time(value):
    if value is None:
        return datetime.min

    try:
        clean_value = value.replace("Z", "+00:00")
        return datetime.fromisoformat(clean_value)
    except ValueError:
        return datetime.min


def get_field(item, names, default_value=None):
    for name in names:
        if name in item:
            return item[name]
    return default_value


def top_unread_notifications(notifications, limit=10):
    Log("backend", "info", "domain", "priority inbox heap logic started for unread notifications")

    heap = []

    for notification in notifications:
        is_read = get_field(notification, ["isRead", "read", "IsRead"], False)
        if is_read is True:
            continue

        notification_type = get_field(notification, ["type", "notificationType", "NotificationType"], "Event")
        created_at = get_field(notification, ["createdAt", "timestamp", "created_at", "CreatedAt"], "")
        current_priority = priority_value.get(notification_type, 4)
        time_value = parse_time(created_at).timestamp()

        heapq.heappush(heap, (current_priority, -time_value, notification))

    result = []
    while len(heap) > 0 and len(result) < limit:
        item = heapq.heappop(heap)[2]

        result.append({
            "notificationID": get_field(item, ["id", "ID", "notificationID", "NotificationID"], ""),
            "type": get_field(item, ["type", "notificationType", "NotificationType"], ""),
            "message": get_field(item, ["message", "Message", "text"], ""),
            "timestamp": get_field(item, ["createdAt", "timestamp", "created_at", "CreatedAt"], ""),
        })

    Log("backend", "info", "handler", "top unread priority notifications prepared for response")
    return result

