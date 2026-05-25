import os
import re
from typing import Optional
from pinecone import Pinecone
from app.utils import ollama_embed, ollama_generate, CHAT_MODEL

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
PINECONE_INDEX = os.getenv("PINECONE_INDEX", "fashion-shop")

_pc: Optional[Pinecone] = None
_index = None


def get_index():
    global _pc, _index
    if _index is None and PINECONE_API_KEY:
        _pc = Pinecone(api_key=PINECONE_API_KEY)
        _index = _pc.Index(PINECONE_INDEX)
    return _index


async def upsert_document(doc_id: str, text: str, metadata: dict):
    """Embed and store a document chunk in Pinecone."""
    index = get_index()
    if not index:
        return
    vector = await ollama_embed(text)
    index.upsert(vectors=[{"id": doc_id, "values": vector, "metadata": {**metadata, "text": text}}])


async def retrieve_context(query: str, top_k: int = 5, filter: dict = None) -> str:
    """Semantic search Pinecone, return concatenated context."""
    index = get_index()
    if not index:
        return ""

    vector = await ollama_embed(query)
    results = index.query(
        vector=vector,
        top_k=top_k,
        include_metadata=True,
        filter=filter,
    )

    chunks = []
    for match in results.matches:
        if match.score > 0.5:
            chunks.append(match.metadata.get("text", ""))

    return "\n\n---\n\n".join(chunks)


async def rag_answer(query: str, history: list[dict]) -> str:
    """Full RAG pipeline: retrieve → augment → generate."""
    context = await retrieve_context(query)

    if not context:
        return "I couldn't find relevant information in the knowledge base for that question."

    history_text = "\n".join(f"{m['role'].upper()}: {m['content']}" for m in history[-6:])

    prompt = f"""Use the following context to answer the user's question accurately.
If the answer is not in the context, say so clearly.

CONTEXT:
{context}

CONVERSATION HISTORY:
{history_text}

USER QUESTION: {query}

Answer:"""

    full = ""
    async for chunk in ollama_generate(CHAT_MODEL, prompt, stream=False):
        full += chunk
    return full


async def ingest_pdf_text(text: str, source: str, chunk_size: int = 800):
    """Split text into chunks and index in Pinecone."""
    # Simple sentence-aware chunking
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks, current = [], ""

    for sentence in sentences:
        if len(current) + len(sentence) > chunk_size and current:
            chunks.append(current.strip())
            current = sentence
        else:
            current += " " + sentence

    if current:
        chunks.append(current.strip())

    for i, chunk in enumerate(chunks):
        doc_id = f"{source}_{i}"
        await upsert_document(doc_id, chunk, {"source": source, "chunk": i, "type": "pdf"})

    return len(chunks)
