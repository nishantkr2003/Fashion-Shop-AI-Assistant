from jose import jwt
from datetime import datetime
from datetime import timedelta
from app.utils.config import settings
from jose import JWTError

ALGORITHM="HS256"

def create_access_token(user_id:int):
    payload={
        "sub":str(user_id),
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }
    return jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm=ALGORITHM
    )


def create_refresh_token(user_id:int):
    payload={
        "sub":str(user_id),
        "exp": datetime.utcnow() + timedelta(days=30)
    }

    return jwt.encode(
        payload,
        settings.JWT_REFRESH_SECRET,
        algorithm=ALGORITHM
    )

def decode_access_token(token:str):
    try:
        return jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[ALGORITHM]
        )
    except JWTError:
        return None


def decode_refresh_token(token:str):
    try:
        return jwt.decode(
            token,
            settings.JWT_REFRESH_SECRET,
            algorithms=[ALGORITHM]
        )
    except JWTError:
        return None