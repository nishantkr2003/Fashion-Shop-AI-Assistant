from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.auth import get_current_user
from app import models, schemas

router = APIRouter()


def queue_for_review(db: Session, query: str, response: str, reason: str) -> models.ReviewQueue:
    item = models.ReviewQueue(query=query, response=response, reason=reason)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("/", response_model=list[schemas.ReviewOut])
def list_reviews(
    status: str = None,
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user),
):
    q = db.query(models.ReviewQueue)
    if status:
        q = q.filter(models.ReviewQueue.status == status)
    return q.order_by(models.ReviewQueue.created_at.desc()).limit(100).all()


@router.patch("/{review_id}", response_model=schemas.ReviewOut)
def update_review(
    review_id: int,
    data: schemas.ReviewUpdate,
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user),
):
    item = db.query(models.ReviewQueue).filter(models.ReviewQueue.id == review_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Review not found")

    item.status = data.status
    if data.response is not None:
        item.response = data.response
    db.commit()
    db.refresh(item)
    return item
