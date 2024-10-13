# from fastapi.testclient import TestClient

from database.orm import Todo, User
from database.repository import TodoRepository, UserReposotory
from service.user import UserService

# from main import app


def test_get_todos(client, mocker):

    # order=ASC
    # mocker.patch(
    #     "api.todo.get_todos",
    #     return_value=[
    #         Todo(id=1, contents="컨텐츠1", is_done=True),
    #         Todo(id=2, contents="컨텐츠2", is_done=False),
    #     ],
    # )

    access_token: str = UserService().create_jwt(username="admin")
    headers: dict = {"Authorization": f"Bearer {access_token}"}

    user = User(id=1, username="admin", password="hashed")
    user.todos = [
        Todo(id=1, contents="컨텐츠1", is_done=True),
        Todo(id=2, contents="컨텐츠2", is_done=False),
    ]

    mocker.patch.object(UserReposotory, "get_user", return_value=user)

    # mocker.patch.object(
    #     TodoRepository,
    #     "get_todos",
    #     return_value=[
    #         Todo(id=1, contents="컨텐츠1", is_done=True),
    #         Todo(id=2, contents="컨텐츠2", is_done=False),
    #     ],
    # )

    response = client.get("/todos", headers=headers)
    assert response.status_code == 200

    # order=DESC
    # response = client.get("/todos?order=DESC")
    # assert response.status_code == 200
    # assert response.json() == user.todos[::-1]


def test_get_todo(client, mocker):

    # 200
    mocker.patch.object(
        TodoRepository,
        "get_todo_by_todo_id",
        return_value=Todo(id=1, contents="컨텐츠1", is_done=True),
    )

    response = client.get("/todos/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "contents": "컨텐츠1", "is_done": True}

    # 404
    mocker.patch.object(
        TodoRepository,
        "get_todo_by_todo_id",
        return_value=None,
    )

    response = client.get("/todos/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "투두를 찾을 수 없습니다."}


def test_create_todo(client, mocker):

    create_spy = mocker.spy(Todo, "create")
    mocker.patch.object(
        TodoRepository,
        "create_todo",
        return_value=Todo(id=1, contents="컨텐츠1", is_done=True),
    )

    body = {"contents": "test", "is_done": False}

    response = client.post("/todos", json=body)

    assert create_spy.spy_return.id is None
    assert create_spy.spy_return.contents == "test"
    assert create_spy.spy_return.is_done is False

    assert response.status_code == 201
    assert response.json() == {"id": 1, "contents": "컨텐츠1", "is_done": True}


def test_update_todo(client, mocker):

    # 200
    mocker.patch.object(
        TodoRepository,
        "get_todo_by_todo_id",
        return_value=Todo(id=1, contents="컨텐츠1", is_done=True),
    )
    undone = mocker.patch.object(Todo, "undone")
    mocker.patch.object(
        TodoRepository,
        "update_todo",
        return_value=Todo(id=1, contents="컨텐츠1", is_done=False),
    )

    body = {"is_done": False}

    response = client.patch("/todos/1", json=body)

    undone.assert_called_once()
    assert response.status_code == 200
    assert response.json() == {"id": 1, "contents": "컨텐츠1", "is_done": False}

    # 404
    mocker.patch.object(
        TodoRepository,
        "get_todo_by_todo_id",
        return_value=None,
    )

    response = client.patch("/todos/1", json={"is_done": False})
    assert response.status_code == 404
    assert response.json() == {"detail": "투두를 찾을 수 없습니다."}


def test_delete_todo(client, mocker):

    # 204
    mocker.patch.object(
        TodoRepository,
        "get_todo_by_todo_id",
        return_value=Todo(id=1, contents="컨텐츠1", is_done=True),
    )

    mocker.patch.object(TodoRepository, "delete_todo", return_value=None)

    response = client.delete("/todos/1")
    assert response.status_code == 204

    # 404
    mocker.patch.object(TodoRepository, "get_todo_by_todo_id", return_value=None)

    response = client.delete("/todos/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "투두를 찾을 수 없습니다."}
