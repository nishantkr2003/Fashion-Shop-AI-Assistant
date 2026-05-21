from sqlalchemy import select
from datetime import datetime
from datetime import timedelta
from app.models.user import User
from app.models.session import Session
from app.auth.password_service import (hash_password)

from app.auth.jwt_service import (
    create_access_token,
    create_refresh_token
)
from sqlalchemy import delete
from sqlalchemy import select
from app.auth.password_service import (verify_password)
from app.auth.jwt_service import (decode_refresh_token)

async def register_user(db,payload):
    existing = await db.execute(
        select( User).where(User.email == payload.email)
    )

    existing = existing.scalar_one_or_none()
    if existing:
        raise Exception("Email already exists")

    user = User(
        full_name=payload.full_name,
        email=payload.email,
        password_hash=hash_password(
            payload.password
        )
    )

    db.add(user)
    await db.flush()
    access = create_access_token(user.id)

    refresh = create_refresh_token(user.id)
    session = Session(
    user_id=user.id,
    refresh_token=refresh,
    device="web",
    expires_at=(datetime.utcnow() + timedelta(days=30))
    )

    db.add(session)
    await db.commit()
    await db.refresh(user)

    return (user,access,refresh)


async def login_user(db,payload):
    result = await db.execute(
        select(User).where(User.email == payload.email)
    )

    user = result.scalar_one_or_none()

    if not user:
        raise Exception("Invalid credentials")

    if not verify_password(payload.password,user.password_hash):
        raise Exception("Invalid credentials")

    access = create_access_token(user.id)
    refresh = create_refresh_token(user.id)
    await db.execute(
        delete(Session).where(Session.user_id == user.id)
    )
    db.add(
        Session(
            user_id=user.id,
            refresh_token=refresh,
            device="web",
            expires_at=(datetime.utcnow() + timedelta(days=30))
        )
    )

    await db.commit()
    return (user,access,refresh)


async def logout_user(db,user_id):

    await db.execute(delete(Session).where(Session.user_id == user_id))
    await db.commit()


async def refresh_session(db,refresh_token):

    payload = decode_refresh_token(refresh_token)
    if not payload:
        raise Exception("Expired refresh")

    user_id = int(payload["sub"])

    result = await db.execute(
        select(Session).where(Session.user_id == user_id)
    )

    session = result.scalar_one_or_none()

    if not session:

        raise Exception("Session not found")

    access = create_access_token(user_id)
    refresh = create_refresh_token(user_id)
    session.refresh_token = refresh
    await db.commit()

    return (access,refresh)