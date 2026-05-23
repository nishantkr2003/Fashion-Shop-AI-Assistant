from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy import text

from app.db import engine

from app.agents import (
    router_agent,
    chat_agent,
    rag_agent
)

from app.sql_agent import (
    sql_agent
)

from app.utils import (
    format_result
)

from app.review import (
    evaluate,
    push_review
)

from app.memory import (
    save,
    load
)


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


class ChatRequest(BaseModel):
    message: str


@router.post("/session")
def create_session():

    with engine.begin() as conn:

        result = conn.execute(

            text("""

INSERT INTO sessions

(

user_id,

title

)

VALUES

(

1,

'New Chat'

)

RETURNING id

"""

            )

        )

        return {

            "session_id":

            result.scalar()

        }



@router.get("/history")
def history():

    with engine.begin() as conn:

        rows = conn.execute(

            text("""

SELECT

id,

title

FROM sessions

ORDER BY id DESC

"""

            )

        )

        return [

            dict(
                r._mapping
            )

            for r

            in rows

        ]


@router.post("/send")
def send(
payload: ChatRequest
):

    session = 1


    route = (

        router_agent(
            payload.message
        )

    )


    try:


        if route["agent"] == "sql":

            memory = load(
                session
            )

            history = memory.get(
                "history",
                []
            )


            context = "\n".join(
                history[-2:]
            )


            query = (

                context

                +

                "\n"

                +

                payload.message

            )


            result = (
                sql_agent(
                    query
                )
            )


            rows = result["rows"]


            confidence = (
                evaluate(
                    rows
                )
            )


            formatted = (
                format_result(
                    rows
                )
            )


            save(
                session,
                payload.message
            )


            return {

                "message":
                formatted,

                "review":
                False,

                "confidence":
                confidence

            }



        if route["agent"] == "rag":

            answer = (

                rag_agent(
                    payload.message
                )

            )

            return {

                "message":
                answer,

                "review":
                False

            }



        reply = (

            chat_agent(
                payload.message
            )

        )

        return {

            "message":
            reply,

            "review":
            False

        }


    except Exception as e:

        push_review(

            payload.message,

            str(e),

            "execution_error"

        )

        return {

            "message":

            "Waiting for review.",

            "review":
            True

        }