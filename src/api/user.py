from fastapi import APIRouter, Depends

from schema.request import SignUpRequest
from service.user import UserService

router = APIRouter(prefix="/users")


@router.post("/sign-up", status_code=201)
def user_sign_up_handler(request: SignUpRequest, user_service: UserService = Depends()):
    # 1. request body(username, password)
    # 2. password -> hashing -> hashed_password
    hashed_password = user_service.hash_password(
        plain_password=request.password,
    )
    # 3. User(username, hashed_password)
    # 4. user -> db save
    # 5. return user(id, username)
    return True
