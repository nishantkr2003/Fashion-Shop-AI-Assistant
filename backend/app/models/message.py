from sqlalchemy import ForeignKey

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.models.base_model import BaseModel


class Message(
    BaseModel
):

    __tablename__="messages"

    conversation_id:Mapped[int]=mapped_column(
        ForeignKey(
            "conversations.id"
        )
    )

    role:Mapped[str]

    content:Mapped[str]