from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


def get_access_token(
    auth_header: HTTPAuthorizationCredentials | None = Depends(
        HTTPBearer(auto_error=False)
    ),
) -> str:
    if auth_header is None:
        raise HTTPException(status_code=401, detail="인증 오류가 발생했습니다.")

    return auth_header.credentials
