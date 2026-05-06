# Campus Notifications Microservice

This design is written in a simple backend style for a campus notification system. Students can get notifications for placements, events, and results.

## Stage 1

### Main Actions

- Create a notification
- Send notification to students
- Get all notifications for a student
- Get unread notifications
- Mark one notification as read
- Mark all notifications as read
- See notification history
- See priority inbox
- Get real-time notifications

### Common Headers

```http
Authorization: Bearer access_token
Content-Type: application/json
```

### Create Notification

```http
POST /api/notifications
```

Request:

```json
{
  "title": "Campus Placement Drive",
  "message": "ABC company is visiting campus tomorrow",
  "notificationType": "Placement",
  "targetBatch": "2027",
  "createdBy": "placement_cell"
}
```

Response:

```json
{
  "notificationID": 501,
  "message": "Notification created successfully"
}
```

### Get Notifications

```http
GET /api/students/1042/notifications?page=1&limit=20
```

Response:

```json
{
  "studentID": 1042,
  "page": 1,
  "notifications": [
    {
      "notificationID": 501,
      "type": "Placement",
      "title": "Campus Placement Drive",
      "message": "ABC company is visiting campus tomorrow",
      "isRead": false,
      "createdAt": "2026-05-06T10:20:00"
    }
  ]
}
```

### Get Unread Notifications

```http
GET /api/students/1042/notifications/unread
```

Response:

```json
{
  "studentID": 1042,
  "unreadCount": 2,
  "notifications": []
}
```

### Mark Notification As Read

```http
PATCH /api/students/1042/notifications/501/read
```

Response:

```json
{
  "message": "Notification marked as read"
}
```

### Mark All As Read

```http
PATCH /api/students/1042/notifications/read-all
```

Response:

```json
{
  "message": "All notifications marked as read"
}
```

### Notification History

```http
GET /api/students/1042/notifications/history?from=2026-04-01&to=2026-05-06
```

Response:

```json
{
  "studentID": 1042,
  "notifications": []
}
```

### Priority Inbox

```http
GET /api/students/1042/notifications/priority-inbox
```

Response:

```json
{
  "notifications": [
    {
      "notificationID": 501,
      "type": "Placement",
      "message": "ABC company is visiting campus tomorrow",
      "createdAt": "2026-05-06T10:20:00"
    }
  ]
}
```

### Real-Time Mechanism

For real-time notifications, I would use WebSocket.

```http
GET /ws/students/1042/notifications
```

When a new notification is created, backend pushes it to the connected student socket. If the student is offline, the notification is still saved in the database and shown on next login.

## Stage 2

### Database Choice

I would use SQL, mainly PostgreSQL. The data has clear relations like students, notifications, and student notification status. SQL is also good for filtering, sorting, joins, and reports.

### Tables

```sql
CREATE TABLE students (
    studentID INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(150),
    batch VARCHAR(20),
    department VARCHAR(50)
);

CREATE TABLE notifications (
    notificationID SERIAL PRIMARY KEY,
    title VARCHAR(200),
    message TEXT,
    notificationType VARCHAR(20),
    createdBy VARCHAR(100),
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE student_notifications (
    id SERIAL PRIMARY KEY,
    studentID INT REFERENCES students(studentID),
    notificationID INT REFERENCES notifications(notificationID),
    isRead BOOLEAN DEFAULT false,
    readAt TIMESTAMP NULL
);
```

### Useful Queries

```sql
SELECT n.notificationID, n.title, n.message, n.notificationType, sn.isRead, n.createdAt
FROM student_notifications sn
JOIN notifications n ON sn.notificationID = n.notificationID
WHERE sn.studentID = 1042
ORDER BY n.createdAt DESC;
```

```sql
UPDATE student_notifications
SET isRead = true, readAt = CURRENT_TIMESTAMP
WHERE studentID = 1042 AND notificationID = 501;
```

```sql
INSERT INTO notifications (title, message, notificationType, createdBy)
VALUES ('Result Published', 'Semester results are published', 'Result', 'exam_cell');
```

### Scaling Problems

As students and notifications increase, the `student_notifications` table becomes very large. One notification sent to 50,000 students means 50,000 rows. Fetching unread notifications can become slow if indexes are missing.

### Solutions

- Add indexes on common filter columns
- Use pagination
- Archive old notifications
- Use Redis cache for unread count and latest notifications
- Use background jobs for bulk notification sending
- Partition old data by month or year if table becomes very big

## Stage 3

Given query:

```sql
SELECT * FROM notifications
WHERE studentID = 1042
AND isRead = false
ORDER BY createdAt DESC;
```

This query is not fully accurate for my schema because `studentID` and `isRead` are in `student_notifications`, not directly in `notifications`.

Better query:

```sql
SELECT n.notificationID, n.title, n.message, n.notificationType, n.createdAt
FROM student_notifications sn
JOIN notifications n ON sn.notificationID = n.notificationID
WHERE sn.studentID = 1042
AND sn.isRead = false
ORDER BY n.createdAt DESC;
```

### Why It Can Be Slow

It can be slow because the database may scan many rows for one student, then filter unread rows, then sort by created time. If the table has lakhs of rows, this becomes expensive.

### Computation Cost

Without an index, cost is close to scanning the full table. If there are 10 lakh rows, the database may check a huge number of rows before returning a small list.

### Why Indexing Every Column Is Bad

Indexing every column wastes storage. It also slows inserts and updates because every index must be updated. Indexes should be made only for columns used often in `WHERE`, `JOIN`, and `ORDER BY`.

### Indexing Strategy

```sql
CREATE INDEX idx_student_read
ON student_notifications(studentID, isRead);

CREATE INDEX idx_notifications_created
ON notifications(createdAt DESC);

CREATE INDEX idx_notifications_type_created
ON notifications(notificationType, createdAt DESC);
```

If unread notifications are queried very often, this is also useful:

```sql
CREATE INDEX idx_student_unread
ON student_notifications(studentID, notificationID)
WHERE isRead = false;
```

### Placement Notifications In Last 7 Days

```sql
SELECT DISTINCT s.studentID, s.name, s.email
FROM students s
JOIN student_notifications sn ON s.studentID = sn.studentID
JOIN notifications n ON sn.notificationID = n.notificationID
WHERE n.notificationType = 'Placement'
AND n.createdAt >= CURRENT_TIMESTAMP - INTERVAL '7 days';
```

## Stage 4

If notifications are fetched on every page load, database load will increase quickly. The backend should not hit the database heavily for the same repeated data.

### Improvements

- Cache latest notifications in Redis using key like `student:1042:notifications`
- Cache unread count separately using key like `student:1042:unread_count`
- Use pagination with `limit` and `page`
- Use lazy loading when user scrolls
- Send real-time updates using WebSocket instead of repeated refresh
- Use short cache expiry like 30 or 60 seconds for latest notifications

### Tradeoffs

Caching makes reads faster, but cache can become stale for a short time. Pagination is simple, but the frontend must handle loading more data. WebSocket gives a better real-time feel, but it needs connection handling.

My practical plan would be:

1. First check Redis for latest notifications.
2. If not found, fetch from database and store in Redis.
3. Update unread count cache when notification is read.
4. Use pagination for history because old notifications do not need to load together.

## Stage 5

Bad pseudocode:

```text
for each student:
    send email
    save to DB
    push app notification
```

### Why This Is Bad

This is slow because every student is processed one by one. If email sending is slow, the whole process waits. If email fails after 200 students, remaining students may not get notification. It is also hard to retry safely.

### Better Design

Create the notification once, save target students, and push jobs into a queue. Workers can process email and push notifications in the background.

DB save and email should not depend on each other directly. The notification should be saved first. Email sending can happen async. If email fails, the app notification still exists in the system.

### Retry Strategy

- Retry failed email jobs 3 times
- Add delay between retries
- Store failed jobs in a dead-letter queue after max retries
- Keep status like `pending`, `sent`, `failed`

### Improved Pseudocode

```text
create notification in DB
find target students

for each student:
    save student_notification row as unread
    add email job to queue
    add push notification job to queue

worker for email queue:
    take one email job
    try:
        send email
        mark email_status as sent
    except:
        retry job if retry_count < 3
        otherwise mark email_status as failed

worker for push queue:
    take one push job
    send app notification
```

This is better because the API returns fast and background workers handle slow tasks.

## Stage 6

Stage 6 working code is inside `notification_app_be/`.

The app fetches notifications from:

```http
GET http://20.207.122.201/evaluation-service/notifications
```

It uses a heap priority queue:

- Placement priority is highest
- Result is second
- Event is third
- Newer notifications come first when type is same
- Only unread notifications are included

Run:

```bash
uvicorn notification_app_be.main:app --reload --port 8002
```

Then open:

```http
GET http://127.0.0.1:8002/priority-inbox
```

