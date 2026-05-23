from fastapi.responses import StreamingResponse

import asyncio


async def generate(
text
):

    for token in text.split():

        yield token + " "

        await asyncio.sleep(
            0.03
        )


def stream(
text
):

    return StreamingResponse(

        generate(
            text
        ),

        media_type="text/plain"

    )