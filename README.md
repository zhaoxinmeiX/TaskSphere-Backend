# TaskSphere-Backend

A Django REST API backend for task management with user authentication.

## Quick Start

1. Clone the repository
2. Create a `.env` file (see Environment Variables section)
3. Install dependencies: `pip install -r requirements.txt`
4. Run migrations: `python manage.py migrate`
5. Start server: `python manage.py runserver`

## API Documentation

Complete API documentation is available in [docs/API.md](docs/API.md)

### Quick API Overview

- **Register:** `POST /api/accounts/register/`
- **Login:** `POST /api/accounts/login/`
- **Logout:** `POST /api/accounts/logout/`
- **Create Task:** `POST /api/tasks/create/`
- **List Tasks:** `GET /api/tasks/`

### Docker Compose services

- `web`: Django backend on `http://localhost:8000`
- `db`: PostgreSQL 17 on `localhost:5432`
- `postgres_data`: named Docker volume that persists database data across container rebuilds

### Environment variables

Create a `.env` file in the project root with the following variables:

- `PGDATABASE` - PostgreSQL database name
- `PGUSER` - PostgreSQL username
- `PGPASSWORD` - PostgreSQL password
- `PGHOST` - PostgreSQL host (e.g., `localhost` or Neon database URL)
- `PGPORT` - PostgreSQL port (defaults to `5432`)

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
