import json
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.db import get_db
from app.auth import get_current_user
from app import models, schemas
from app.memory import get_history, save_message, get_or_create_session, update_session_title
from app.agents import dispatch, dispatch_stream
from app.review import queue_for_review

router = APIRouter()


@router.post("/sessions", response_model=schemas.SessionOut, status_code=201)
def create_session(
    data: schemas.SessionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    session = models.Session(user_id=current_user.id, title=data.title)
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


@router.get("/sessions", response_model=list[schemas.SessionOut])
def list_sessions(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return (
        db.query(models.Session)
        .filter(models.Session.user_id == current_user.id)
        .order_by(models.Session.created_at.desc())
        .limit(50)
        .all()
    )


@router.get("/sessions/{session_id}/messages", response_model=list[schemas.MessageOut])
def get_messages(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    session = (
        db.query(models.Session)
        .filter(models.Session.id == session_id, models.Session.user_id == current_user.id)
        .first()
    )
    if not session:
        raise HTTPException(404, "Session not found")

    return (
        db.query(models.Message)
        .filter(models.Message.session_id == session_id)
        .order_by(models.Message.created_at.asc())
        .all()
    )


@router.delete("/sessions/{session_id}")
def delete_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    session = (
        db.query(models.Session)
        .filter(models.Session.id == session_id, models.Session.user_id == current_user.id)
        .first()
    )
    if not session:
        raise HTTPException(404, "Session not found")
    db.delete(session)
    db.commit()
    return {"deleted": True}


@router.post("/stream")
async def chat_stream(
    data: schemas.ChatRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """SSE streaming endpoint."""
    session = (
        db.query(models.Session)
        .filter(models.Session.id == data.session_id, models.Session.user_id == current_user.id)
        .first()
    )
    if not session:
        raise HTTPException(404, "Session not found")

    history = get_history(db, data.session_id)
    update_session_title(db, session, data.message)
    save_message(db, data.session_id, "user", data.message)

    async def event_generator():
        full_response = ""
        agent = "chat"
        confidence = 1.0
        needs_review = False

        async for chunk in dispatch_stream(data.message, history, db):
            if chunk.startswith("\n__meta__"):
                meta = json.loads(chunk.replace("\n__meta__", ""))
                agent = meta.get("agent", "chat")
                confidence = meta.get("confidence", 1.0)
                needs_review = meta.get("needs_review", False)
            else:
                full_response += chunk
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"

        # Save assistant response
        save_message(db, data.session_id, "assistant", full_response)

        # Queue for human review if needed
        if needs_review:
            queue_for_review(
                db,
                query=data.message,
                response=full_response,
                reason=f"Low confidence ({confidence:.2f}) from {agent} agent",
            )

        yield f"data: {json.dumps({'done': True, 'agent': agent, 'confidence': confidence})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
