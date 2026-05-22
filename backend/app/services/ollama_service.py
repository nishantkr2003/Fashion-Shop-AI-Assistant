import httpx


OLLAMA_URL = (
    "http://127.0.0.1:11434"
)


async def generate(
    prompt
):

    async with httpx.AsyncClient(
        timeout=180
    ) as client:

        r = await client.post(

            f"{OLLAMA_URL}/api/generate",

            json={

                "model":
                "qwen2.5-coder:1.5b",

                "prompt":
                prompt,

                "stream":
                False

            }

        )

        print(
            "\nSTATUS:",
            r.status_code
        )

        data = r.json()

        print(
            "\nRAW:",
            data
        )

        if r.status_code != 200:

            raise Exception(
                str(data)
            )

        return (

            data

            .get(
                "response",
                ""
            )

            .strip()

        )