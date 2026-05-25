import os
import re
import httpx
from typing import AsyncGenerator

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
CHAT_MODEL = os.getenv("CHAT_MODEL", "qwen2.5-coder:1.5b")
SQL_MODEL = os.getenv("SQL_MODEL", "qwen2.5-coder:1.5b")
EMBED_MODEL = os.getenv("EMBED_MODEL", "nomic-embed-text:latest")


async def ollama_embed(text: str) -> list[float]:
    # Long timeout — first call loads the model into memory (~60s on slow hardware)
    timeout = httpx.Timeout(connect=10.0, read=180.0, write=10.0, pool=10.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        resp = await client.post(
            f"{OLLAMA_URL}/api/embeddings",
            json={"model": EMBED_MODEL, "prompt": text},
        )
        resp.raise_for_status()
        return resp.json()["embedding"]


async def ollama_generate(
    model: str,
    prompt: str,
    system: str = "",
    stream: bool = False,
) -> AsyncGenerator[str, None]:
    payload = {
        "model": model,
        "prompt": prompt,
        "system": system,
        "stream": stream,
        "options": {"temperature": 0.1},
    }
    timeout = httpx.Timeout(connect=10.0, read=300.0, write=10.0, pool=10.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        if stream:
            async with client.stream("POST", f"{OLLAMA_URL}/api/generate", json=payload) as resp:
                async for line in resp.aiter_lines():
                    if line:
                        import json
                        chunk = json.loads(line)
                        if chunk.get("response"):
                            yield chunk["response"]
        else:
            resp = await client.post(f"{OLLAMA_URL}/api/generate", json=payload)
            resp.raise_for_status()
            yield resp.json()["response"]


def is_destructive_sql(sql: str) -> bool:
    """Block any non-SELECT statements."""
    cleaned = sql.strip().upper()
    return bool(re.match(r"^(INSERT|UPDATE|DELETE|DROP|ALTER|TRUNCATE|CREATE)", cleaned))


def extract_sql(text: str) -> str:
    """Pull SQL from LLM response (may be in code fences)."""
    fence = re.search(r"```(?:sql)?\s*(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if fence:
        return fence.group(1).strip()
    # Fallback: find first SELECT statement
    match = re.search(r"(SELECT\s+.+?;?)", text, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else text.strip()