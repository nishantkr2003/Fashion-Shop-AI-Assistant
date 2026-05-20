from fastapi import Request
from fastapi import HTTPException

from app.auth.jwt_service import (decode_access_token)


async def get_current_user(request: Request):

    token = request.cookies.get(
        "access_token"
    )

    if not token:
        raise HTTPException(401,"Unauthorized")

    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(401,"Invalid token")

    return int(payload["sub"])