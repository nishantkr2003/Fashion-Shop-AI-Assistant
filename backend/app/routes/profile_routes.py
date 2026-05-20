from fastapi import APIRouter
from fastapi import Depends

from app.middleware.auth import (get_current_user)

router = APIRouter()


@router.get(
    "/profile"
)

async def profile(
    user_id=Depends(get_current_user)
):
    return {"user_id":user_id}