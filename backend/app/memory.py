from sqlalchemy.orm import Session as DBSession
from app import models
from typing import List, Dict


def get_history(db: DBSession, session_id: int, limit: int = 20) -> List[Dict]:
    """Return recent messages as LangChain-compatible dicts."""
    messages = (
        db.query(models.Message)
        .filter(models.Message.session_id == session_id)
        .order_by(models.Message.created_at.desc())
        .limit(limit)
        .all()
    )
    return [{"role": m.role, "content": m.content} for m in reversed(messages)]


def save_message(db: DBSession, session_id: int, role: str, content: str) -> models.Message:
    msg = models.Message(session_id=session_id, role=role, content=content)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg


def get_or_create_session(db: DBSession, user_id: int, session_id: int | None) -> models.Session:
    if session_id:
        session = (
            db.query(models.Session)
            .filter(models.Session.id == session_id, models.Session.user_id == user_id)
            .first()
        )
        if session:
            return session

    session = models.Session(user_id=user_id)
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def update_session_title(db: DBSession, session: models.Session, first_message: str):
    """Set session title from first user message (truncated)."""
    if session.title == "New Chat":
        session.title = first_message[:60]
        db.commit()
