from database.orm import User
from database.repository import UserReposotory
from service.user import UserService


def test_user_sign_up(client, mocker):

    # create_spy = mocker.spy(User, "create")
    hash_password = mocker.patch.object(
        UserService, "hash_password", return_value="hashed"
    )
    mocker.patch.object(
        UserReposotory, "save_user", return_value=User(id=1, username="admin")
    )

    user_create = mocker.patch.object(
        User, "create", return_value=User(id=None, username="admin", password="hashed")
    )

    body = {"username": "admin", "password": "plain"}

    response = client.post("/users/sign-up", json=body)

    hash_password.assert_called_once_with(plain_password="plain")

    user_create.assert_called_once_with(username="admin", hashed_password="hashed")

    assert response.status_code == 201
    assert response.json() == {"id": 1, "username": "admin"}


def test_user_log_in(client, mocker):
    mocker.patch.object(
        UserReposotory,
        "get_user",
        return_value=User(id=1, username="admin", password="hashed"),
    )

    verify_password = mocker.patch.object(
        UserService, "verify_password", return_value=True
    )

    create_jwt = mocker.patch.object(
        UserService, "create_jwt", return_value="mocked_jwt_token"
    )

    body = {"username": "admin", "password": "plain"}

    response = client.post("/users/log-in", json=body)

    verify_password.assert_called_once_with(
        plain_password="plain", hashed_password="hashed"
    )
    create_jwt.assert_called_once_with(username="admin")

    assert response.status_code == 200
    assert response.json() == {"access_token": "mocked_jwt_token"}
