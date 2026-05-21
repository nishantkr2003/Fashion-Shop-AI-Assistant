from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy.sql import func

from datetime import datetime


class Base(DeclarativeBase):
    pass


class BaseModel(Base):

    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )