from langchain_ollama import ChatOllama

from app.rag import retrieve


llm = ChatOllama(
    model="qwen2.5-coder:1.5b",
    temperature=0
)


def router_agent(
query:str
):

    prompt = f"""
You classify requests.

Return EXACTLY ONE:

sql
rag
chat

sql:
database
products
price
inventory
stock
count
filter
show
compare

rag:
refund
shipping
exchange
faq
policy
delivery

chat:
general
conversation

Query:
{query}
"""

    result = (

        llm.invoke(
            prompt
        )

        .content

        .lower()

        .strip()

    )


    if "rag" in result:

        return {

            "agent":
            "rag",

            "confidence":
            0.95

        }


    if "sql" in result:

        return {

            "agent":
            "sql",

            "confidence":
            0.95

        }


    return {

        "agent":
        "chat",

        "confidence":
        0.90

    }



def chat_agent(
query
):

    return (

        llm.invoke(

f"""

You are Fashion Shop AI.

Keep replies concise.

User:

{query}

"""

        )

        .content

    )



def rag_agent(
query
):

    docs = retrieve(
        query
    )


    if not docs:

        return (

            "No document found."

        )


    context = "\n\n".join(

        [

            x.page_content

            for x

            in docs

        ]

    )


    return (

        llm.invoke(

f"""

Answer ONLY from context.

If unavailable say:
Information not available.

Context:

{context}

Question:

{query}

"""

        )

        .content

    )