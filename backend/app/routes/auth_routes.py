from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from fastapi import Response
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from app.db.database import get_db

from app.schemas.auth_schema import (
    RegisterInput,
    LoginInput
)

from app.auth.auth_service import (
    register_user,
    login_user,
    refresh_session,
    logout_user
)

from app.middleware.auth import (
    get_current_user
)


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


def set_auth_cookies(

    response,

    access: str,

    refresh: str

):

    response.set_cookie(

        key="access_token",

        value=access,

        httponly=True,

        secure=False,

        samesite="lax",

        path="/",

        max_age=60 * 60
    )

    response.set_cookie(

        key="refresh_token",

        value=refresh,

        httponly=True,

        secure=False,

        samesite="lax",

        path="/",

        max_age=60 * 60 * 24 * 30
    )

    return response


# REGISTER


@router.post(
    "/register",
    operation_id="register_user"
)
async def register(

    payload: RegisterInput,

    db=Depends(get_db)

):

    try:

        user, access, refresh = (

            await register_user(
                db,
                payload
            )
        )

        response = JSONResponse(

            content={

                "message":
                "registered",

                "user": {

                    "id":
                    user.id,

                    "email":
                    user.email
                }
            }

        )

        return set_auth_cookies(

            response,

            access,

            refresh
        )

    except Exception as e:

        raise HTTPException(
            400,
            str(e)
        )


# LOGIN


@router.post(
    "/login",
    operation_id="login_user"
)
async def login(

    payload: LoginInput,

    db=Depends(get_db)

):

    try:

        user, access, refresh = (

            await login_user(
                db,
                payload
            )
        )

        response = JSONResponse(

            content={

                "message":
                "logged_in",

                "user": {

                    "id":
                    user.id,

                    "email":
                    user.email
                }

            }

        )

        return set_auth_cookies(

            response,

            access,

            refresh
        )

    except Exception as e:

        raise HTTPException(
            401,
            str(e)
        )


# REFRESH


@router.post(
    "/refresh",
    operation_id="refresh_token"
)
async def refresh(

    request: Request,

    db=Depends(get_db)

):

    try:

        token = (

            request.cookies.get(
                "refresh_token"
            )
        )

        access, refresh_token = (

            await refresh_session(
                db,
                token
            )
        )

        response = JSONResponse(

            content={

                "message":
                "refreshed"
            }

        )

        return set_auth_cookies(

            response,

            access,

            refresh_token
        )

    except Exception as e:

        raise HTTPException(
            401,
            str(e)
        )


# LOGOUT


@router.post(
    "/logout",
    operation_id="logout_user"
)
async def logout(

    user_id: int = Depends(
        get_current_user
    ),

    db=Depends(
        get_db
    )

):

    await logout_user(
        db,
        user_id
    )

    response = JSONResponse(

        content={

            "message":
            "logged_out"
        }

    )

    response.delete_cookie(

        key="access_token",

        path="/"
    )

    response.delete_cookie(

        key="refresh_token",

        path="/"
    )

    return response