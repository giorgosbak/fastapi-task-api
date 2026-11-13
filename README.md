# Task Manager REST API

A RESTful Task Management API built with **Python, FastAPI, SQLAlchemy, and SQLite**.

The application supports creating, retrieving, updating, and deleting tasks, with request validation and automated testing.

## Features

- Create new tasks
- Retrieve all tasks or a specific task by ID
- Update existing tasks
- Delete tasks
- Persistent SQLite database storage
- Request validation using Pydantic
- Automatic OpenAPI/Swagger documentation
- Automated API tests using Pytest
- HTTP error handling

## Tech Stack

- Python 3.14
- FastAPI
- Pydantic
- SQLAlchemy
- SQLite
- Pytest
- HTTPX2

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API health message |
| POST | `/tasks` | Create a task |
| GET | `/tasks` | Retrieve all tasks |
| GET | `/tasks/{task_id}` | Retrieve a specific task |
| PUT | `/tasks/{task_id}` | Update a task |
| DELETE | `/tasks/{task_id}` | Delete a task |

## Installation

Clone the repository and navigate into the project directory.

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Initialize the database:

```bash
python init_db.py
```

Start the server:

```bash
python -m uvicorn main:app --reload --port 8002
```

## API Documentation

Once the server is running, visit:

`http://127.0.0.1:8002/docs`

## Example Request

Create a new task:

```bash
curl -X POST http://127.0.0.1:8002/tasks \
-H "Content-Type: application/json" \
-d '{
  "title": "Learn FastAPI",
  "description": "Build a REST API",
  "completed": false
}'
```

## Automated Testing

Run all tests using:

```bash
python -m pytest -v
```

The tests use an isolated in-memory SQLite database to avoid modifying production data.

## Project Purpose

This project demonstrates backend API development with Python, including RESTful endpoint design, database integration, request validation, and automated testing.

It was developed as a practical portfolio project to demonstrate backend development skills.
