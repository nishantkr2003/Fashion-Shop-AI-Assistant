from sqlalchemy import ForeignKey

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.models.base_model import BaseModel


class EmailVerification(
    BaseModel
):

    __tablename__="email_verifications"

    user_id:Mapped[int]=mapped_column(
        ForeignKey(
            "users.id"
        )
    )

    token:Mapped[str]

    used:Mapped[bool]=mapped_column(
        default=False
    )