from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from datetime import datetime

from app.models.base_model import BaseModel


class Session(BaseModel):

    __tablename__="sessions"

    user_id:Mapped[int]=mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        )
    )

    refresh_token:Mapped[str]

    device:Mapped[str]=mapped_column(
        String(255)
    )

    expires_at:Mapped[datetime]