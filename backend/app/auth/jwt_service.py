from jose import jwt
from datetime import datetime
from datetime import timedelta

from app.utils.config import settings


ALGORITHM="HS256"


def create_access_token(
    user_id:int
):

    payload={

        "sub":str(
            user_id
        ),

        "exp":
        datetime.utcnow()
        +
        timedelta(
            minutes=30
        )
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm=ALGORITHM
    )


def create_refresh_token(
    user_id:int
):

    payload={

        "sub":str(
            user_id
        ),

        "exp":
        datetime.utcnow()
        +
        timedelta(
            days=30
        )
    }

    return jwt.encode(
        payload,
        settings.JWT_REFRESH_SECRET,
        algorithm=ALGORITHM
    )