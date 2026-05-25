"""
Ingest a PDF or .txt policy file into Pinecone for RAG.

Usage:
    pip install PyPDF2 python-dotenv
    python ingest_policy.py policies.pdf
    python ingest_policy.py policies.txt   # plain text also works

Place this file in the backend/ folder.
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Validate args
if len(sys.argv) < 2:
    print("Usage: python ingest_policy.py <file.pdf or file.txt>")
    sys.exit(1)

FILE_PATH = sys.argv[1]
if not os.path.exists(FILE_PATH):
    print(f"❌  File not found: {FILE_PATH}")
    sys.exit(1)


def read_pdf(path: str) -> str:
    try:
        import PyPDF2
    except ImportError:
        print("❌  PyPDF2 not installed. Run: pip install PyPDF2")
        sys.exit(1)

    text = ""
    with open(path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for i, page in enumerate(reader.pages):
            page_text = page.extract_text() or ""
            text += f"\n{page_text}"
            print(f"   Read page {i + 1}/{len(reader.pages)}")
    return text.strip()


def read_txt(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()


async def main():
    # Import here so .env is loaded first
    from app.rag import ingest_pdf_text

    ext = os.path.splitext(FILE_PATH)[1].lower()
    source = os.path.splitext(os.path.basename(FILE_PATH))[0]

    print(f"📂  Reading {FILE_PATH}…")
    if ext == ".pdf":
        text = read_pdf(FILE_PATH)
    elif ext == ".txt":
        text = read_txt(FILE_PATH)
    else:
        print(f"❌  Unsupported file type: {ext}. Use .pdf or .txt")
        sys.exit(1)

    if not text:
        print("❌  No text extracted from file.")
        sys.exit(1)

    print(f"📝  Extracted {len(text)} characters")
    print(f"🔪  Chunking and embedding into Pinecone (source='{source}')…")

    count = await ingest_pdf_text(text, source=source, chunk_size=800)

    print(f"✅  Done! Indexed {count} chunks into Pinecone under source='{source}'")
    print(f"\nYou can now ask questions like:")
    print(f"  - What is the return policy?")
    print(f"  - How long does shipping take?")
    print(f"  - Do you offer a warranty?")


if __name__ == "__main__":
    asyncio.run(main())