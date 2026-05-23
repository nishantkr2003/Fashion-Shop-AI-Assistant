from app.agents.sql_memory import (
    get_context,
    save_context
)


FOLLOW_WORDS = [

    "under",
    "above",
    "below",
    "over",
    "less",
    "more",
    "cheap",
    "cheaper",

    "nike",
    "adidas",

    "black",
    "white",
    "blue",

    "only",

    "price"

]


def build_query(

    conversation_id,

    message

):

    message = (

        message
        .lower()
        .strip()

    )

    previous = (

        get_context(
            conversation_id
        )

    )

    if previous:

        short_query = (

            len(
                message.split()
            )

            <= 3
        )

        follow = (

            short_query

            or

            any(
                x in message

                for x in FOLLOW_WORDS
            )

        )

        if follow:

            final = (

                previous
                + " "
                + message
            )

        else:

            final = message

    else:

        final = message

    save_context(

        conversation_id,

        final

    )

    print(
        "\nMEMORY:",
        final
    )

    return final