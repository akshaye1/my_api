import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from my_api.database import get_db
from my_api.main import app
from my_api.models import Base


test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


@pytest.fixture
def client():
    Base.metadata.create_all(bind=test_engine)

    def get_test_db():
        db = TestSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = get_test_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.pop(get_db, None)
        Base.metadata.drop_all(bind=test_engine)
        

def test_get_tasks(client):
    response = client.get("/tasks")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    
    
def test_create_task(client):
    payload = {
        "title": "Automated test task",
        "priority": 1,
    }

    response = client.post("/tasks", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == payload["title"]
    assert data["priority"] == payload["priority"]
    assert "id" in data
    
def test_created_task_can_be_retrieved(client):
    payload = {
        "title": "Check persistence",
        "priority": 2,
    }

    create_response = client.post("/tasks", json=payload)
    assert create_response.status_code == 200

    task_id = create_response.json()["id"]

    get_response = client.get(f"/tasks/{task_id}")

    assert get_response.status_code == 200
    assert get_response.json()["id"] == task_id
    assert get_response.json()["title"] == payload["title"]
    assert get_response.json()["priority"] == payload["priority"]
    
def test_get_missing_task(client):
    response = client.get("/tasks/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"
    
def test_update_task(client):
    payload = {
        "title": "Original title",
        "priority": 1,
    }

    create_response = client.post("/tasks", json=payload)
    assert create_response.status_code == 200

    task_id = create_response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={"priority": 3},
    )

    assert response.status_code == 200
    assert response.json()["priority"] == 3
    assert response.json()["title"] == "Original title"
    
def test_delete_task(client):
    payload = {
        "title": "Task to delete",
        "priority": 1,
    }

    create_response = client.post("/tasks", json=payload)
    assert create_response.status_code == 200

    task_id = create_response.json()["id"]

    delete_response = client.delete(f"/tasks/{task_id}")

    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Task deleted successfully!"

    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404
    
def test_create_task_missing_title(client):
    response = client.post(
        "/tasks",
        json={"priority": 1},
    )

    assert response.status_code == 422
    

def test_create_task_invalid_priority(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Invalid priority",
            "priority": "high",
        },
    )

    assert response.status_code == 422
    
def test_create_task_ignores_extra_field(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Learn FastAPI",
            "priority": 1,
            "completed": True,
        },
    )

    assert response.status_code == 200
    assert "completed" not in response.json()
    
def test_update_missing_task(client):
    response = client.patch(
        "/tasks/999999",
        json={"priority": 3},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"
    
def test_delete_missing_task(client):
    response = client.delete("/tasks/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"
    
def test_create_task_rejects_negative_priority(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Invalid priority",
            "priority": -1,
        },
    )

    assert response.status_code == 422
    
def test_update_task_rejects_negative_priority(client):
    create_response = client.post(
        "/tasks",
        json={
            "title": "Valid task",
            "priority": 1,
        },
    )

    task_id = create_response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={"priority": -1},
    )

    assert response.status_code == 422
    
def test_create_task_rejects_priority_above_five(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Invalid priority",
            "priority": 6,
        },
    )

    assert response.status_code == 422
    
def test_create_task_accepts_minimum_priority(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Minimum priority",
            "priority": 1,
        },
    )

    assert response.status_code == 200
    assert response.json()["priority"] == 1
    
def test_create_task_accepts_maximum_priority(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Maximum priority",
            "priority": 5,
        },
    )

    assert response.status_code == 200
    assert response.json()["priority"] == 5
    
    
def test_create_task_rejects_empty_title(client):
    response = client.post(
        "/tasks",
        json={
            "title": "",
            "priority": 1,
        },
    )

    assert response.status_code == 422
    
def test_create_task_rejects_whitespace_title(client):
    response = client.post(
        "/tasks",
        json={
            "title": "   ",
            "priority": 1,
        },
    )

    assert response.status_code == 422