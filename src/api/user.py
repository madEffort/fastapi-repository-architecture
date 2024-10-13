from fastapi import APIRouter, Depends, HTTPException

from database.orm import User
from database.repository import UserReposotory
from schema.request import LogInRequest, SignUpRequest
from schema.response import JWTResponse, UserSchema
from service.user import UserService

router = APIRouter(prefix="/users")


@router.post("/sign-up", status_code=201)
def user_sign_up_handler(
    request: SignUpRequest,
    user_service: UserService = Depends(),
    user_repo: UserReposotory = Depends(),
):
    # 1. request body(username, password)
    # 2. password -> hashing -> hashed_password
    hashed_password = user_service.hash_password(
        plain_password=request.password,
    )
    # 3. User(username, hashed_password)
    user: User = User.create(username=request.username, hashed_password=hashed_password)
    # 4. user -> db save
    user: User = user_repo.save_user(user=user)
    # 5. return user(id, username)
    return UserSchema.model_validate(user)


@router.post("/log-in")
def user_log_in_handler(
    request: LogInRequest,
    user_repo: UserReposotory = Depends(),
    user_service: UserService = Depends(),
):

    # 1. request body(username, password)
    # 2. db read user
    user: User | None = user_repo.get_user(username=request.username)

    if not user:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")

    # 3. user.password, request.password -> bycrypt.checkpw
    verified: bool = user_service.verify_password(
        plain_password=request.password,
        hashed_password=user.password,
    )

    if not verified:
        raise HTTPException(status_code=401, detail="인증되지 않은 사용자입니다.")

    # 4. create jwt
    access_token: str = user_service.create_jwt(username=user.username)
    # 5. return jwt
    return JWTResponse.model_validate({"access_token": access_token})
