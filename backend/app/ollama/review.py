from sqlalchemy import text

from app.db import engine


def evaluate(
rows
):

    if not rows:

        return 0.45


    count = len(
        rows
    )


    if count > 0:

        return 0.95


    return 0.60



def push_review(

query,

response,

reason

):

    with engine.begin() as conn:

        conn.execute(

            text("""

INSERT INTO review_queue

(

query,

response,

reason,

status

)

VALUES

(

:q,

:r,

:reason,

'pending'

)

"""

            ),

            {

                "q":
                query,

                "r":
                response,

                "reason":
                reason

            }

        )