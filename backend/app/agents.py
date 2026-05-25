import json
import re
from typing import Literal, AsyncGenerator
from sqlalchemy.orm import Session as DBSession
from sqlalchemy import text, inspect

from app.utils import ollama_generate, extract_sql, is_destructive_sql, CHAT_MODEL, SQL_MODEL
from app.rag import rag_answer, retrieve_context
from app import models


AgentType = Literal["sql", "rag", "chat", "review"]
# ── Schema introspection 

def get_schema_summary(db: DBSession) -> str:
    """Dynamically generate table/column summary for the SQL agent."""
    inspector = inspect(db.bind)
    lines = []
    for table_name in inspector.get_table_names():
        cols = inspector.get_columns(table_name)
        col_defs = ", ".join(f"{c['name']} ({c['type']})" for c in cols)
        lines.append(f"  {table_name}({col_defs})")
    return "TABLES:\n" + "\n".join(lines)


# ── Router Agent

async def route_query(query: str, history: list[dict]) -> tuple[AgentType, float]:
    """Decide which agent handles this query. Returns (agent_type, confidence)."""
    history_summary = "\n".join(f"{m['role']}: {m['content']}" for m in history[-4:])

    prompt = f"""Classify this user query into exactly one category.

Categories:
- sql: Questions about products, inventory, prices, stock, categories, brands, counts, statistics
- rag: Questions about policies, shipping, returns, warranties, store info, FAQ
- chat: General conversation, greetings, help requests, anything else

Recent conversation:
{history_summary}

User query: {query}

Respond with JSON only, no explanation:
{{"type": "sql|rag|chat", "confidence": 0.0-1.0}}"""

    result = ""
    async for chunk in ollama_generate(SQL_MODEL, prompt, stream=False):
        result += chunk

    try:
        # Extract JSON from response
        match = re.search(r'\{.*?\}', result, re.DOTALL)
        if match:
            data = json.loads(match.group())
            agent = data.get("type", "chat")
            confidence = float(data.get("confidence", 0.5))
            if agent not in ("sql", "rag", "chat"):
                agent = "chat"
            return agent, confidence
    except Exception:
        pass

    return "chat", 0.5


# ── SQL Agent 

async def sql_answer(query: str, db: DBSession) -> str:
    """Convert NL query → SQL → execute → format result."""
    schema = get_schema_summary(db)

    prompt = f"""You are a SQL expert. Convert the user question to a PostgreSQL SELECT query.

{schema}

Rules:
- Only SELECT statements allowed
- Use ILIKE for string searches
- Use LIMIT 20 unless user asks for more
- Return only the SQL query, no explanation

User question: {query}

SQL:"""

    sql_text = ""
    async for chunk in ollama_generate(SQL_MODEL, prompt, stream=False):
        sql_text += chunk

    sql_text = extract_sql(sql_text)

    if is_destructive_sql(sql_text):
        return "I can only run read-only queries for safety. Please rephrase your question."

    try:
        result = db.execute(text(sql_text))
        rows = result.fetchall()
        columns = list(result.keys())

        if not rows:
            return "No results found for your query."

        # Human-style formatter
        formatted = []

        for i, row in enumerate(rows[:10], 1):
            item = dict(zip(columns, row))

            formatted.append(
                f"""
{i}. {item.get("name")}
• Brand: {item.get("brand")}
• Color: {item.get("color")}
• Size: {item.get("size")}
• Price: ${item.get("price")}
• Rating: ⭐ {item.get("rating")}
• In stock: {item.get("stock")} units
• {item.get("description")}
"""
            )

        intro = f"I found {len(rows)} matching products for you:\n\n"

        if(len(rows) > 10):
            outro = f"\nShowing first 10 results."
        else:
            outro = ""

        return intro + "".join(formatted) + outro



        # Format as readable text
        # lines = [" | ".join(columns)]
        # lines.append("-" * len(lines[0]))
        # for row in rows[:20]:
        #     lines.append(" | ".join(str(v) if v is not None else "—" for v in row))

        # if len(rows) > 20:
        #     lines.append(f"... and {len(rows) - 20} more results")

        # return f"```\n{chr(10).join(lines)}\n```\n\n*Query: `{sql_text}`*"

    except Exception as e:
        return f"Query error: {str(e)}\n\nGenerated SQL: `{sql_text}`"


# ── Chat Agent 

async def chat_answer(query: str, history: list[dict]) -> str:
    history_text = "\n".join(f"{m['role'].upper()}: {m['content']}" for m in history[-8:])

    system = (
        "You are a helpful shopping assistant. "
        "Be friendly, concise, and useful. "
        "If asked about products or policies, let the user know you can query those for them."
    )

    prompt = f"""Conversation so far:
{history_text}

USER: {query}
ASSISTANT:"""

    full = ""
    async for chunk in ollama_generate(CHAT_MODEL, prompt, system=system, stream=False):
        full += chunk
    return full.strip()


# ── Main dispatch 

async def dispatch(
    query: str,
    history: list[dict],
    db: DBSession,
) -> tuple[str, AgentType, float, bool]:
    """
    Returns (response_text, agent_used, confidence, needs_review).
    needs_review=True if confidence < 0.75 or unsafe content detected.
    """
    agent, confidence = await route_query(query, history)
    needs_review = confidence < 0.75

    try:
        if agent == "sql":
            response = await sql_answer(query, db)
        elif agent == "rag":
            response = await rag_answer(query, history)
        else:
            response = await chat_answer(query, history)
    except Exception as e:
        response = f"I encountered an error processing your request. Please try again."
        needs_review = True

    return response, agent, confidence, needs_review


async def dispatch_stream(
    query: str,
    history: list[dict],
    db: DBSession,
) -> AsyncGenerator[str, None]:
    """
    SSE streaming dispatch. Yields text chunks then a final metadata JSON line.
    """
    agent, confidence = await route_query(query, history)
    needs_review = confidence < 0.75

    # SQL and RAG don't stream well (need full result first)
    if agent == "sql":
        response = await sql_answer(query, db)
        yield response
    elif agent == "rag":
        response = await rag_answer(query, history)
        yield response
    else:
        history_text = "\n".join(f"{m['role'].upper()}: {m['content']}" for m in history[-8:])
        system = (
            "You are a helpful shopping assistant. "
            "Be friendly, concise, and useful."
        )
        prompt = f"""Conversation:
{history_text}

USER: {query}
ASSISTANT:"""
        async for chunk in ollama_generate(CHAT_MODEL, prompt, system=system, stream=True):
            yield chunk

    # Final metadata (client can parse lines starting with __meta__)
    yield f"\n__meta__{json.dumps({'agent': agent, 'confidence': confidence, 'needs_review': needs_review})}"
