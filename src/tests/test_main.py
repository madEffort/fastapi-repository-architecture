from fastapi.testclient import TestClient

from database.orm import Todo
from main import app

client = TestClient(app=app)


def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong"}


def test_get_todos(mocker):

    # order=ASC
    mocker.patch(
        "main.get_todos",
        return_value=[
            Todo(id=1, contents="컨텐츠1", is_done=True),
            Todo(id=2, contents="컨텐츠2", is_done=False),
        ],
    )

    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == {
        "todos": [
            {"id": 1, "contents": "컨텐츠1", "is_done": True},
            {"id": 2, "contents": "컨텐츠2", "is_done": False},
        ]
    }

    # order=DESC
    response = client.get("/todos?order=DESC")
    assert response.status_code == 200
    assert response.json() == {
        "todos": [
            {"id": 2, "contents": "컨텐츠2", "is_done": False},
            {"id": 1, "contents": "컨텐츠1", "is_done": True},
        ]
    }
