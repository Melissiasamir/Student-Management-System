# Student Management System — API (Task 05)

## Project Overview

This project is the backend evolution of the Task 04 **Student Management
System**, a command-line application that stored student records in
`students.json`. Task 05 upgrades that project into a production-style
**RESTful API** built with **FastAPI** and backed by a **SQLite** database
accessed through the **SQLAlchemy ORM**.

The original CLI logic has been preserved conceptually (add / view / search /
update / delete students) but re-architected using proper separation of
concerns: routing, schemas, database models, and business logic each live in
their own module. The original Task 04 script is kept unmodified under
`legacy/student_manager.py` for reference and to show the evolution from
procedural CLI code to an object-oriented, layered web service.

## Features

- Full CRUD REST API for student records
- SQLite persistence via SQLAlchemy ORM (replaces `students.json`)
- Strong request validation with Pydantic, including real email format
  validation (not just a check for `"@"`), positive-age enforcement, and
  required-field checks
- Duplicate email protection with meaningful `409 Conflict` responses
- Clean, layered architecture: routers → schemas → CRUD/service layer →
  models → database
- Auto-generated interactive API docs via Swagger UI and ReDoc
- Health check endpoint for monitoring

## Technologies Used

- **Python 3.12+**
- **FastAPI** — web framework
- **Uvicorn** — ASGI server
- **SQLAlchemy 2.x** — ORM
- **SQLite** — relational database
- **Pydantic v2** — data validation and serialization
- **email-validator** — RFC-compliant email validation

## Folder Structure

```
Student-Management-System/
├── app/
│   ├── main.py            # FastAPI app instance, startup, health check
│   ├── database.py         # Engine, session factory, declarative base
│   ├── models.py           # SQLAlchemy ORM models (Student)
│   ├── schemas.py           # Pydantic request/response schemas + validation
│   ├── crud.py               # StudentService: business logic & DB operations
│   ├── config.py               # Centralized app settings
│   └── routers/
│       └── students.py           # /students endpoint definitions
├── legacy/
│   └── student_manager.py            # Original Task 04 CLI implementation
├── students.db                          # SQLite database (created at runtime)
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation

### 1. Clone or download the project

```bash
git clone <your-repo-url>
cd Student-Management-System
```

### 2. Virtual Environment Setup

Create and activate a virtual environment:

**macOS / Linux**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows**
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Running the API

Start the FastAPI application with Uvicorn:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

On first run, SQLAlchemy automatically creates `students.db` and the
`students` table — no manual database setup is required.

## Swagger Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`

Visiting the root URL (`/`) redirects to `/docs`.

## API Endpoints

| Method | Endpoint            | Description             | Success Status | Error Status |
|--------|---------------------|--------------------------|-----------------|--------------|
| POST   | `/students`          | Create a new student     | `201 Created`    | `409`, `422` |
| GET    | `/students`           | List all students        | `200 OK`          | –            |
| GET    | `/students/{id}`       | Get a student by ID       | `200 OK`           | `404`        |
| PUT    | `/students/{id}`        | Update a student           | `200 OK`            | `404`, `409`, `422` |
| DELETE | `/students/{id}`         | Delete a student             | `204 No Content`     | `404`        |
| GET    | `/health`                 | Health check                  | `200 OK`              | –            |

## Example Requests

### Create a student

```bash
curl -X POST http://127.0.0.1:8000/students \
  -H "Content-Type: application/json" \
  -d '{
        "name": "Ahmed",
        "age": 20,
        "grade": "A",
        "email": "ahmed@example.com"
      }'
```

### Get all students

```bash
curl http://127.0.0.1:8000/students
```

### Get a student by ID

```bash
curl http://127.0.0.1:8000/students/1
```

### Update a student

```bash
curl -X PUT http://127.0.0.1:8000/students/1
  -H "Content-Type: application/json" \
  -d '{"grade": "A+"}'
```

### Delete a student

```bash
curl -X DELETE http://127.0.0.1:8000/students/1
```

## Validation Rules

- `id`: automatically generated by the database (auto-increment primary key)
- `name`: required, non-empty, max 100 characters
- `age`: required, integer greater than 0 and less than 150
- `grade`: required, non-empty
- `email`: required, must be a valid email format, unique across students

Invalid requests return `422 Unprocessable Entity` with details on which
field failed and why. Duplicate email addresses return `409 Conflict`.

## Evolution From Task 04

| Aspect              | Task 04 (CLI)                  | Task 05 (API)                                   |
|---------------------|----------------------------------|--------------------------------------------------|
| Interface            | Command-line menu                 | REST API (HTTP)                                    |
| Storage               | `students.json` (flat file)         | `students.db` (SQLite via SQLAlchemy)                |
| Architecture           | Single procedural script              | Layered: routers / schemas / crud / models            |
| Validation               | Manual, minimal (e.g. age cast only)     | Pydantic-enforced, including real email validation      |
| Error handling             | `print()` statements                        | HTTP status codes + JSON error details                   |

