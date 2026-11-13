from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Task Manager API is running"
    }

def test_create_task(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Test Task",
            "description": "Testing POST endpoint",
            "completed": False
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["message"] == "Task created successfully"
    assert data["task"]["id"] == 1
    assert data["task"]["title"] == "Test Task"
    assert data["task"]["completed"] is False

def test_get_task(client):
    # Create a task
    create_response = client.post(
        "/tasks",
        json={
            "title": "Learn Testing",
            "description": "Practice Pytest",
            "completed": False
        }
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["task"]["id"]

    # Retrieve the task
    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == task_id
    assert data["title"] == "Learn Testing"
    assert data["description"] == "Practice Pytest"
    assert data["completed"] is False

def test_get_nonexistent_task(client):
    response = client.get("/tasks/999")

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Task not found"
    }

def test_update_task(client):
    # Create a task
    create_response = client.post(
        "/tasks",
        json={
            "title": "Learn FastAPI",
            "description": "Practice REST APIs",
            "completed": False
        }
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["task"]["id"]

    # Update the task
    update_response = client.put(
        f"/tasks/{task_id}",
        json={
            "title": "Learn FastAPI",
            "description": "Practice REST APIs",
            "completed": True
        }
    )

    assert update_response.status_code == 200
    assert update_response.json()["completed"] is True

    # Verify the saved state
    get_response = client.get(f"/tasks/{task_id}")

    assert get_response.status_code == 200
    assert get_response.json()["completed"] is True

def test_delete_task(client):
    # Create a task
    create_response = client.post(
        "/tasks",
        json={
            "title": "Delete Test",
            "description": "Testing DELETE endpoint",
            "completed": False
        }
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["task"]["id"]

    # Delete the task
    delete_response = client.delete(f"/tasks/{task_id}")

    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Task deleted successfully"

    # Verify that the task no longer exists
    get_response = client.get(f"/tasks/{task_id}")

    assert get_response.status_code == 404
    assert get_response.json() == {
        "detail": "Task not found"
    }

def test_create_task_missing_title(client):
    response = client.post(
        "/tasks",
        json={
            "description": "Task without title",
            "completed": False
        }
    )

    assert response.status_code == 422

def test_create_task_invalid_completed(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Invalid Task",
            "description": "Testing validation",
            "completed": "not_a_boolean"
        }
    )

    assert response.status_code == 422
