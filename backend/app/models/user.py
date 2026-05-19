from sqlalchemy import String
from sqlalchemy import Boolean

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.models.base_model import BaseModel


class User(BaseModel):

    __tablename__="users"

    email:Mapped[str]=mapped_column(
        String(255),
        unique=True,
        index=True
    )

    password_hash:Mapped[str]

    full_name:Mapped[str]

    is_verified:Mapped[bool]=mapped_column(
        Boolean,
        default=False
    )