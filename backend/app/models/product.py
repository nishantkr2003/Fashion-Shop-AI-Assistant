# from sqlalchemy import (
#     String,
#     Float,
#     Integer
# )

# from sqlalchemy.orm import (
#     Mapped,
#     mapped_column
# )

# from app.models.base import (
#     Base
# )


# class Product(
#     Base
# ):

#     __tablename__ = "products"

#     id: Mapped[int] = mapped_column(
#         primary_key=True
#     )

#     name: Mapped[str] = mapped_column(
#         String
#     )

#     brand: Mapped[str] = mapped_column(
#         String
#     )

#     category: Mapped[str] = mapped_column(
#         String
#     )

#     color: Mapped[str] = mapped_column(
#         String
#     )

#     size: Mapped[str] = mapped_column(
#         String
#     )

#     price: Mapped[float] = mapped_column(
#         Float
#     )

#     rating: Mapped[float] = mapped_column(
#         Float
#     )

#     stock: Mapped[int] = mapped_column(
#         Integer
#     )

#     description: Mapped[str] = mapped_column(
#         String
#     )

#     image_url: Mapped[str] = mapped_column(
#         String
#     )


from sqlalchemy import (
    String,
    Float,
    Integer
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from app.models.base_model import (
    BaseModel
)


class Product(
    BaseModel
):

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(255))

    brand: Mapped[str] = mapped_column(String(255))

    category: Mapped[str] = mapped_column(String(255))

    color: Mapped[str] = mapped_column(String(255))

    size: Mapped[str] = mapped_column(String(50))

    price: Mapped[float] = mapped_column(Float)

    rating: Mapped[float] = mapped_column(Float)

    stock: Mapped[int] = mapped_column(Integer)

    description: Mapped[str] = mapped_column(String)

    image_url: Mapped[str] = mapped_column(String)