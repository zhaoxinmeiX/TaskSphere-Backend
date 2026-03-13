# TaskSphere-Backend

## Account registration API

The backend exposes a registration endpoint for creating user accounts.

- **Endpoint:** `POST /api/accounts/register/`
- **Content-Type:** `application/json`
- **Body:**
  - `username` (string, required)
  - `password` (string, required)

Example request body:

```json
{
  "username": "newuser",
  "password": "StrongPass123!"
}
```

Example success response (`201 Created`):

```json
{
  "id": 1,
  "username": "newuser"
}
```

Passwords are stored securely using Django's built-in password hashing.

## Login API

The backend exposes a login endpoint for user authentication.

- **Endpoint:** `POST /api/accounts/login/`
- **Content-Type:** `application/json`
- **Body:**
  - `username` (string, required)
  - `password` (string, required)

Example request body:

```json
{
  "username": "testuser",
  "password": "TestPass123!"
}
```

Example success response (`200 OK`):

```json
{
  "token": "b90bb8105cccdfa0cccfa8b7f2238aec282f5526",
  "user": {
    "id": 6,
    "username": "testuser"
  }
}
```

Example error response (`400 Bad Request`):

```json
{
  "non_field_errors": ["Invalid credentials."]
}
```

The returned authentication token can be used for subsequent authenticated requests by including it in the `Authorization` header: `Authorization: Token b90bb8105cccdfa0cccfa8b7f2238aec282f5526`

## Database setup

This backend now supports PostgreSQL through Docker Compose for durable local development data.

### Docker Compose services

- `web`: Django backend on `http://localhost:8000`
- `db`: PostgreSQL 17 on `localhost:5432`
- `postgres_data`: named Docker volume that persists database data across container rebuilds

### Environment variables

The project reads database settings from `DATABASE_URL` first. If that is not set, it falls back to `POSTGRES_*` variables. If neither is provided, Django uses the local `db.sqlite3` file.

Recommended `.env` values for Docker Compose:

- `SECRET_KEY=django-insecure-tasksphere-dev-secret-key-change-in-production`
- `DEBUG=True`
- `ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0`
- `POSTGRES_DB=tasksphere`
- `POSTGRES_USER=tasksphere`
- `POSTGRES_PASSWORD=tasksphere`
- `POSTGRES_HOST=db`
- `POSTGRES_PORT=5432`
- `DATABASE_URL=postgresql://tasksphere:tasksphere@db:5432/tasksphere`

### Start the stack

```zsh
docker compose up --build
```

Django runs migrations automatically when the `web` container starts.

### Stop the stack

```zsh
docker compose down
```

### Reset the PostgreSQL data volume

```zsh
docker compose down -v
```

### Local non-Docker fallback

If you want to run Django without Docker, remove `DATABASE_URL` and the `POSTGRES_*` variables from `.env`. The backend will fall back to SQLite using `db.sqlite3`.
