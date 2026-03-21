# TaskSphere API Documentation

## Authentication

All API endpoints (except register and login) require token-based authentication. Include the token in the `Authorization` header:

```
Authorization: Token your-auth-token-here
```

## Account APIs

### Register User

Create a new user account.

- **Endpoint:** `POST /api/accounts/register/`
- **Content-Type:** `application/json`
- **Body:**
  - `username` (string, required)
  - `password` (string, required)

**Request Example:**
```json
{
  "username": "newuser",
  "password": "StrongPass123!"
}
```

**Success Response (201 Created):**
```json
{
  "id": 1,
  "username": "newuser"
}
```

### Login

Authenticate user and receive auth token.

- **Endpoint:** `POST /api/accounts/login/`
- **Content-Type:** `application/json`
- **Body:**
  - `username` (string, required)
  - `password` (string, required)

**Request Example:**
```json
{
  "username": "testuser",
  "password": "TestPass123!"
}
```

**Success Response (200 OK):**
```json
{
  "token": "b90bb8105cccdfa0cccfa8b7f2238aec282f5526",
  "user": {
    "id": 6,
    "username": "testuser"
  }
}
```

**Error Response (400 Bad Request):**
```json
{
  "non_field_errors": ["Invalid credentials."]
}
```

### Logout

Logout the current user (invalidates the token).

- **Endpoint:** `POST /api/accounts/logout/`
- **Content-Type:** `application/json`
- **Authentication:** Required

**Success Response (200 OK):**
```json
{
  "message": "Successfully logged out."
}
```

## Task APIs

### Create Task

Create a new task for the authenticated user.

- **Endpoint:** `POST /api/tasks/create/`
- **Content-Type:** `application/json`
- **Authentication:** Required
- **Body:**
  - `title` (string, required)
  - `description` (string, optional)

**Request Example:**
```json
{
  "title": "Complete project documentation",
  "description": "Write comprehensive documentation for the TaskSphere backend API"
}
```

**Success Response (201 Created):**
```json
{
  "id": 1,
  "title": "Complete project documentation",
  "description": "Write comprehensive documentation for the TaskSphere backend API",
  "status": "todo",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### List Tasks

Get all tasks for the authenticated user.

- **Endpoint:** `GET /api/tasks/`
- **Authentication:** Required

**Success Response (200 OK):**
```json
[
  {
    "id": 1,
    "title": "Complete project documentation",
    "description": "Write comprehensive documentation for the TaskSphere backend API",
    "status": "todo",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  },
  {
    "id": 2,
    "title": "Review pull requests",
    "description": "Check and approve pending pull requests",
    "status": "in_progress",
    "created_at": "2024-01-15T09:15:00Z",
    "updated_at": "2024-01-15T09:15:00Z"
  }
]
```

**Notes:**
- Tasks are returned in descending order of creation date (newest first)
- Only tasks belonging to the authenticated user are returned
- The `status` field shows the current task status

### Update Task Status

Update the status of a specific task.

- **Endpoint:** `PATCH /api/tasks/{id}/update/`
- **Content-Type:** `application/json`
- **Authentication:** Required
- **Body:**
  - `status` (string, required) - New status value

**Status Options:**
- `"todo"` - Task is not started
- `"in_progress"` - Task is currently being worked on
- `"completed"` - Task is finished

**Request Example:**
```json
{
  "status": "in_progress"
}
```

**Success Response (200 OK):**
```json
{
  "id": 1,
  "title": "Complete project documentation",
  "description": "Write comprehensive documentation for the TaskSphere backend API",
  "status": "in_progress",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T11:15:00Z"
}
```

**Error Responses:**

**Missing Status Field (400 Bad Request):**
```json
{
  "error": "Status field is required"
}
```

**Invalid Status Value (400 Bad Request):**
```json
{
  "status": ["\"invalid_status\" is not a valid choice."]
}
```

**Not Found (404 Not Found):**
```json
{
  "detail": "Not found."
}
```

## Error Responses

Most endpoints return standard HTTP status codes:

- `200 OK` - Successful request
- `201 Created` - Resource successfully created
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required/invalid
- `403 Forbidden` - Permission denied
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## Data Models

### Task Model

```json
{
  "id": "integer (auto-generated)",
  "title": "string (max 200 characters)",
  "description": "text (optional)",
  "status": "string (choices: 'todo', 'in_progress', 'completed', default: 'todo')",
  "created_at": "datetime (auto-generated)",
  "updated_at": "datetime (auto-updated)",
  "user": "foreign key to User"
}
```

### User Model

```json
{
  "id": "integer (auto-generated)",
  "username": "string (unique)",
  "password": "string (hashed, not returned in API)"
}
```
