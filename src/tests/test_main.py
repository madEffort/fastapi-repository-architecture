# from fastapi.testclient import TestClient

from fastapi import responses
from database.orm import Todo

# from main import app


def test_health_check(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong"}


def test_get_todos(client, mocker):

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


def test_get_todo(client, mocker):

    # 200
    mocker.patch(
        "main.get_todo_by_todo_id",
        return_value=Todo(id=1, contents="컨텐츠1", is_done=True),
    )

    response = client.get("/todos/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "contents": "컨텐츠1", "is_done": True}

    # 404
    mocker.patch(
        "main.get_todo_by_todo_id",
        return_value=None,
    )

    response = client.get("/todos/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "투두를 찾을 수 없습니다."}


def test_create_todo(client, mocker):

    create_spy = mocker.spy(Todo, "create")
    mocker.patch(
        "main.create_todo",
        return_value=Todo(id=1, contents="컨텐츠1", is_done=True),
    )

    body = {"contents": "test", "is_done": False}

    response = client.post("/todos", json=body)

    assert create_spy.spy_return.id is None
    assert create_spy.spy_return.contents == "test"
    assert create_spy.spy_return.is_done is False

    assert response.status_code == 201
    assert response.json() == {"id": 1, "contents": "컨텐츠1", "is_done": True}
