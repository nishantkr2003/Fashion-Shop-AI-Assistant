# from fastapi import (
#     APIRouter,
#     HTTPException,
#     Depends
# )

# from sqlalchemy.orm import Session

# from app.db import (
#     get_db
# )

# from app.models import (
#     User
# )

# from app.schemas import *

# from app.auth import *

# router = APIRouter(
#     prefix="/auth",
#     tags=["Auth"]
# )


# @router.post(
#     "/register"
# )
# def register(
#     body: RegisterInput,
#     db: Session = Depends(
#         get_db
#     )
# ):

#     exists = (
#         db.query(User)
#         .filter(
#             User.email ==
#             body.email
#         )
#         .first()
#     )

#     if exists:

#         raise HTTPException(
#             400,
#             "Email exists"
#         )

#     user = User(

#         full_name=
#         body.full_name,

#         email=
#         body.email,

#         # password_hash=hash_password(body.password)
#     )


#     db.add(user)

#     db.commit()

#     db.refresh(
#         user
#     )

#     token = create_token(
#         {
#             "id":
#             user.id
#         }
#     )

#     return {

#         "access_token":
#         token,

#         "token_type":
#         "bearer",

#         "user": {

#             "id":
#             user.id,

#             "email":
#             user.email,

#             "full_name":
#             user.full_name
#         }
#     }


# @router.post(
#     "/login"
# )
# def login(
#     body: LoginInput,
#     db: Session = Depends(
#         get_db
#     )
# ):

#     user = (
#         db.query(User)
#         .filter(
#             User.email ==
#             body.email
#         )
#         .first()
#     )

#     if (
#         not user
#         or
#         not verify_password(
#             body.password,
#             user.password_hash
#         )
#     ):

#         raise HTTPException(
#             401,
#             "Invalid credentials"
#         )

#     token = create_token(
#         {
#             "id":
#             user.id
#         }
#     )

#     return {

#         "access_token":
#         token,

#         "token_type":
#         "bearer",

#         "user": {

#             "id":
#             user.id,

#             "email":
#             user.email,

#             "full_name":
#             user.full_name
#         }
#     }




from fastapi import (
    APIRouter,
    HTTPException,
    Depends
)

from sqlalchemy.orm import Session

from app.db import get_db
from app.models import User
from app.schemas import *
from app.auth import *

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/register")
def register(
    body: RegisterInput,
    db: Session = Depends(get_db)
):

    exists = (
        db.query(User)
        .filter(User.email == body.email)
        .first()
    )

    if exists:
        raise HTTPException(
            status_code=400,
            detail="Email exists"
        )

    try:
        hashed = hash_password(body.password)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    user = User(
        full_name=body.full_name,
        email=body.email,
        password_hash=hashed
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_token(
        {
            "id": user.id
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name
        }
    }


@router.post("/login")
def login(
    body: LoginInput,
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(User.email == body.email)
        .first()
    )

    if (
        not user
        or
        not verify_password(
            body.password,
            user.password_hash
        )
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token = create_token(
        {
            "id": user.id
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name
        }
    }