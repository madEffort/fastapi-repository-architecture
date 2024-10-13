from fastapi import APIRouter, Depends, HTTPException


from database.orm import User
from database.repository import UserReposotory
from schema.request import (
    CreateOTPRequest,
    LogInRequest,
    SignUpRequest,
)
from schema.response import JWTResponse, UserSchema
from security import get_access_token
from service.user import UserService
from cache import redis_client

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
        raise HTTPException(status_code=401, detail="인증 오류가 발생했습니다.")

    # 4. create jwt
    access_token: str = user_service.create_jwt(username=user.username)
    # 5. return jwt
    return JWTResponse.model_validate({"access_token": access_token})


# 회원가입(username, password) / 로그인
# 이메일 알림: 회원가입 -> 이메일 인증(otp) -> 유저 이메일 저장 -> 이메일 알림

# POST /users/email/otp -> (key: email, value: 1234, exp: 3분)
# POST /users/email/otp/verify -> request(email, otp) -> user(email)


@router.post("/email/otp")
def create_otp_handler(
    request: CreateOTPRequest,
    _: str = Depends(get_access_token),
    user_service: UserService = Depends(),
):
    # 1. access_token
    # 2. request body(email)
    # 3. otp create(random 4 digit)
    otp: int = user_service.create_otp()

    # 4. redis otp(email, 1234, exp=3min)
    redis_client.set(request.email, otp)
    redis_client.expire(request.email, 3 * 60)

    # 5. send otp to email
    # 나중에 구현
    return {"otp": otp}


@router.post("/email/otp/verify")
def verify_otp_handler(access_token: str = Depends(get_access_token)):

    pass
