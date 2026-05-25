# Fashion Shop AI

A production-ready, full-stack AI-powered shopping assistant with multi-agent architecture, streaming responses, RAG knowledge base, and human review queue.

---

## Architecture

```
User → Next.js Frontend → FastAPI Backend → Router Agent
                                               ├── SQL Agent    → Neon PostgreSQL
                                               ├── RAG Agent    → Pinecone + PDF
                                               └── Chat Agent   → Ollama LLM
```

## Tech Stack

| Layer | Tech |
|---|---|
| Frontend | Next.js 14, TypeScript, Tailwind CSS, Zustand |
| Backend | FastAPI, SQLAlchemy, JWT, Passlib |
| AI | llama3.1:8b (chat), qwen2.5-coder:1.5b (SQL/routing), nomic-embed-text (embeddings) |
| Vector DB | Pinecone |
| Database | Neon PostgreSQL |
| Deployment | Vercel (frontend), Render (backend) |

---

## Project Structure

```
fashion-shop-ai/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI app, CORS, routers
│   │   ├── db.py            # SQLAlchemy + Neon connection
│   │   ├── models.py        # users, products, sessions, messages, review_queue
│   │   ├── schemas.py       # Pydantic request/response models
│   │   ├── auth.py          # JWT auth, bcrypt, /auth/* routes
│   │   ├── chat.py          # SSE streaming, /chat/* routes
│   │   ├── agents.py        # Router, SQL, RAG, Chat agents
│   │   ├── rag.py           # Pinecone vector store, PDF ingestion
│   │   ├── memory.py        # Chat history, session management
│   │   ├── csv_import.py    # Dynamic CSV → PostgreSQL → Pinecone
│   │   ├── review.py        # Human review queue
│   │   └── utils.py         # Ollama client, SQL safety, helpers
│   ├── requirements.txt
│   └── .env.example
└── frontend/
    ├── src/
    │   ├── app/
    │   │   ├── login/page.tsx
    │   │   ├── signup/page.tsx
    │   │   └── chat/page.tsx
    │   ├── components/
    │   │   ├── Sidebar.tsx
    │   │   ├── ChatMessage.tsx
    │   │   └── ChatInput.tsx
    │   ├── stores/
    │   │   ├── auth.ts       # Zustand auth store
    │   │   └── chat.ts       # Zustand chat + session store
    │   └── lib/
    │       └── api.ts        # Axios client, SSE stream helper
    └── .env.local.example
```

---

## Local Development

### Prerequisites

- Python 3.11+
- Node.js 18+
- [Ollama](https://ollama.ai) running locally
- Neon PostgreSQL database
- Pinecone account

### 1. Pull Ollama models

```bash
ollama pull llama3.1:8b
ollama pull qwen2.5-coder:1.5b
ollama pull nomic-embed-text:latest
```

### 2. Backend setup

```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# Edit .env with your credentials

uvicorn app.main:app --reload --port 8000
```

### 3. Frontend setup

```bash
cd frontend
npm install

cp .env.local.example .env.local
# Edit .env.local: NEXT_PUBLIC_API_URL=http://localhost:8000

npm run dev
```

Visit http://localhost:3000

---

## Environment Variables

### Backend (`backend/.env`)

| Variable | Description |
|---|---|
| `DATABASE_URL` | Neon PostgreSQL connection string |
| `JWT_SECRET` | Secret key for JWT signing (min 32 chars) |
| `OLLAMA_URL` | Ollama server URL (default: http://localhost:11434) |
| `PINECONE_API_KEY` | Pinecone API key |
| `PINECONE_INDEX` | Pinecone index name (default: fashion-shop) |
| `CHAT_MODEL` | Ollama chat model (default: llama3.1:8b) |
| `SQL_MODEL` | Ollama SQL/routing model (default: qwen2.5-coder:1.5b) |
| `EMBED_MODEL` | Ollama embedding model (default: nomic-embed-text:latest) |

### Frontend (`frontend/.env.local`)

| Variable | Description |
|---|---|
| `NEXT_PUBLIC_API_URL` | Backend API URL |

---

## API Reference

### Auth

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login, get JWT |
| GET | `/auth/me` | Get current user |
| POST | `/auth/logout` | Logout (clears client token) |

### Chat

| Method | Endpoint | Description |
|---|---|---|
| POST | `/chat/sessions` | Create session |
| GET | `/chat/sessions` | List user sessions |
| GET | `/chat/sessions/{id}/messages` | Get messages |
| DELETE | `/chat/sessions/{id}` | Delete session |
| POST | `/chat/stream` | SSE streaming chat |

### CSV Import

| Method | Endpoint | Description |
|---|---|---|
| POST | `/import/upload` | Upload CSV, auto-create table |

### Review Queue

| Method | Endpoint | Description |
|---|---|---|
| GET | `/review/` | List review items |
| PATCH | `/review/{id}` | Update review status |

---

## Agent System

### Router Agent
Uses `qwen2.5-coder:1.5b` to classify queries:
- `sql` → product data questions (inventory, prices, stock)
- `rag` → policy questions (shipping, returns, FAQ)
- `chat` → general conversation

Returns confidence score. If `< 0.75`, triggers human review.

### SQL Agent
- Introspects database schema dynamically
- Generates PostgreSQL SELECT queries
- Blocks all destructive operations (INSERT/UPDATE/DELETE/DROP)
- Supports: COUNT, AVG, GROUP BY, ORDER BY, LIMIT, ILIKE

### RAG Agent
- Embeds query with `nomic-embed-text`
- Retrieves top-5 chunks from Pinecone
- Filters by cosine similarity > 0.5
- Generates answer with `llama3.1:8b`

### Chat Agent
- Multi-turn conversation with history (last 8 messages)
- General assistant persona

---

## CSV Import

POST any CSV to `/import/upload`. The system:
1. Detects column names and types (String/Float/Integer)
2. Creates or updates the PostgreSQL table automatically
3. Inserts rows (ignores errors, skips duplicates)
4. Embeds all rows into Pinecone for semantic search
5. Returns a summary: table name, columns, inserted/skipped counts

No hardcoded schema — works with any CSV structure.

---

## PDF Knowledge Base

Use `app/rag.py:ingest_pdf_text()` to index PDFs:

```python
from app.rag import ingest_pdf_text
import asyncio

with open("policies.pdf", "rb") as f:
    import PyPDF2
    reader = PyPDF2.PdfReader(f)
    text = "\n".join(page.extract_text() for page in reader.pages)

asyncio.run(ingest_pdf_text(text, source="policies", chunk_size=800))
```

---

## Deployment

### Backend → Render

1. Create a new **Web Service** on Render
2. Connect your repo, set root directory to `backend/`
3. Build: `pip install -r requirements.txt`
4. Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add all environment variables in Render dashboard

### Frontend → Vercel

1. Import the repo on Vercel
2. Set root directory to `frontend/`
3. Add environment variable: `NEXT_PUBLIC_API_URL=https://your-render-app.onrender.com`
4. Deploy

### Pinecone Setup

1. Create a Pinecone index named `fashion-shop`
2. Dimensions: **768** (nomic-embed-text output)
3. Metric: **cosine**

---

## Human Review

Responses are automatically queued for review when:
- Routing confidence < 0.75
- Agent encounters an error

Reviewers can PATCH `/review/{id}` with status: `approved | edited | rejected`.

---

## Extending to a New Dataset

1. Upload your CSV via `POST /import/upload`
2. The table is auto-created, rows inserted, embeddings indexed
3. The SQL agent reads the schema dynamically — no code changes needed
4. The RAG agent searches Pinecone — PDF documents add context automatically
