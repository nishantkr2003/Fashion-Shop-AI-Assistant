from fastapi import APIRouter

router=APIRouter(
    prefix="/auth"
)


@router.get(
    "/health"
)

async def auth():

    return {
        "auth":"ok"
    }