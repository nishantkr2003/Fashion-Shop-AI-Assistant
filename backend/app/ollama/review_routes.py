from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy import text

from app.db import engine


router = APIRouter(
    prefix="/review",
    tags=["Review"]
)


class EditInput(BaseModel):
    response: str


@router.get("/queue")
def queue():

    with engine.begin() as conn:

        rows = conn.execute(
            text("""

SELECT *

FROM review_queue

WHERE status='pending'

ORDER BY id DESC

""")
        )

        return [

            dict(r._mapping)

            for r

            in rows

        ]


@router.post("/approve/{id}")
def approve(id:int):

    with engine.begin() as conn:

        conn.execute(

            text("""

UPDATE review_queue

SET status='approved'

WHERE id=:id

"""

            ),

            {

                "id":
                id

            }

        )

    return {

        "success":
        True

    }


@router.post("/reject/{id}")
def reject(id:int):

    with engine.begin() as conn:

        conn.execute(

            text("""

UPDATE review_queue

SET status='rejected'

WHERE id=:id

"""

            ),

            {

                "id":
                id

            }

        )

    return {

        "success":
        True

    }


@router.post("/edit/{id}")
def edit(
id:int,
payload:EditInput
):

    with engine.begin() as conn:

        conn.execute(

            text("""

UPDATE review_queue

SET

response=:r,

status='edited'

WHERE id=:id

"""

            ),

            {

                "id":
                id,

                "r":
                payload.response

            }

        )

    return {

        "success":
        True

    }