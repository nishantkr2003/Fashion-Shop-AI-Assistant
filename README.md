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

![System Architecture](Images/Backend%20Service%20Dependency%20Graph.png)

---

## Tech Stack

| Layer      | Tech                                                                                 |
| ---------- | ------------------------------------------------------------------------------------ |
| Frontend   | Next.js 14, TypeScript, Tailwind CSS, Zustand                                        |
| Backend    | FastAPI, SQLAlchemy, JWT, Passlib                                                    |
| AI         | llama3.1:8b (chat), qwen2.5-coder:1.5b (SQL/routing), nomic-embed-text (embeddings) |
| Vector DB  | Pinecone                                                                             |
| Database   | Neon PostgreSQL                                                                      |
| Deployment | Vercel (frontend), Render (backend)                                                  |

---

## Sequence Diagram

![Sequence Diagram](Images/Complete%20AI%20Query%20Flow%20Diagram.png)

---

## Agent Routing

![Agent Routing](Images/LangGraph%20Multi-Agent%20Routing%20Architectur....png)

---

## RAG Workflow

![RAG Workflow](Images/RAG%20Pipeline%20Diagram.png)

---

## SQL Agent Flow

![SQL Agent Flow](Images/SQL%20Agent%20Internal%20Pipeline.png)

---

## Streaming Flow

![Streaming Flow](Images/Streaming%20Architecture%20Diagram.png)

---

## Review Queue Flow

![Review Queue Flow](Images/Human%20Review%20Pipeline.png)

---

## Project Structure

```
fashion-shop-ai/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app, CORS, router mounting
│   │   ├── db.py                # SQLAlchemy engine, SessionLocal, Base
│   │   ├── models.py            # User, Product, Session, Message, ReviewQueue
│   │   ├── schemas.py           # Pydantic: RegisterInput, LoginInput, AuthResponse
│   │   ├── auth.py              # hash_password, verify_password, create_token
│   │   ├── agents.py            # router_agent, sql_agent_fn, rag_agent, chat_agent
│   │   ├── sql_agent.py         # Pinecone schema retrieval → SQL generation → execution
│   │   ├── rag.py               # Pinecone ingest (PDF + TXT) + retrieve
│   │   ├── memory.py            # In-memory session history dict
│   │   ├── review.py            # evaluate(), push_review() → returns id
│   │   ├── utils.py             # format_result(rows) → formatted string
│   │   ├── routes/
│   │   │   ├── auth.py          # POST /auth/register, POST /auth/login
│   │   │   ├── chat.py          # POST /chat/send, GET /chat/review/status/{id}
│   │   │   └── review.py        # GET /review/queue, POST /review/approve/{id}, etc.
│   │   └── scripts/
│   │       ├── seed.py          # Import products CSV → Neon
│   │       ├── ingest_rag.py    # Ingest docs/ PDFs and TXTs into Pinecone (rag_docs ns)
│   │       └── ingest_schema.py # Embed DB schema into Pinecone (sql_schema ns)
│   ├── data/
│   │   ├── products.csv         # 50+ fashion products
│   │   └── docs/                # Policy PDFs and TXT files for RAG
│   │       ├── refund_policy.pdf
│   │       ├── shipping_policy.pdf
│   │       ├── exchange_policy.pdf
│   │       └── faq.txt
│   └── requirements.txt
├── frontend/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx             # Redirects to /chat
│   │   ├── login/page.tsx
│   │   ├── register/page.tsx
│   │   └── chat/
│   │       └── page.tsx         # Main chat page
│   ├── components/
│   │   ├── Sidebar.tsx          # Session history, new chat, review toggle
│   │   ├── ChatMessages.tsx     # Message list, streaming, product cards
│   │   ├── MessageBubble.tsx    # User/AI bubble, review banner with polling
│   │   ├── ProductCards.tsx     # Grid of product cards from SQL results
│   │   ├── ReviewPanel.tsx      # Slide-in review queue panel
│   │   └── ChatInput.tsx        # Textarea, send button, suggestions
│   ├── store/
│   │   └── chatStore.ts         # Zustand: sessions, messages, reviewItems
│   └── lib/
│       └── api.ts               # fetch wrappers for all backend endpoints
├── Images/
│   ├── Backend Service Dependency Graph.png
│   ├── Complete AI Query Flow Diagram.png
│   ├── Conversation Memory Flow.png
│   ├── Deployment Architecture Diagram.png
│   ├── Human Review Pipeline.png
│   ├── LangGraph Multi-Agent Routing Architectur....png
│   ├── RAG Pipeline Diagram.png
│   ├── SQL Agent Internal Pipeline.png
│   ├── Streaming Architecture Diagram.png
│   └── mermaid-diagram (8).png
├── .gitignore
├── README.md
└── run.md
```

---

## Database Schema (Neon / PostgreSQL)

```sql
CREATE TABLE users (
    id            SERIAL PRIMARY KEY,
    full_name     VARCHAR NOT NULL,
    email         VARCHAR UNIQUE NOT NULL,
    password_hash VARCHAR NOT NULL,
    created_at    TIMESTAMP DEFAULT NOW()
);

CREATE TABLE products (
    id       SERIAL PRIMARY KEY,
    name     VARCHAR,
    category VARCHAR,   -- Shoes | Hoodies | Jackets | Jeans | T-Shirts | Bags
    price    FLOAT,
    brand    VARCHAR,
    color    VARCHAR,
    stock    INTEGER
);

CREATE TABLE sessions (
    id         SERIAL PRIMARY KEY,
    user_id    INTEGER NOT NULL,
    title      VARCHAR DEFAULT 'New Chat',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE messages (
    id         SERIAL PRIMARY KEY,
    session_id INTEGER NOT NULL,
    role       VARCHAR NOT NULL,   -- user | assistant
    content    TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE review_queue (
    id       SERIAL PRIMARY KEY,
    query    TEXT,
    response TEXT,
    reason   VARCHAR,
    status   VARCHAR DEFAULT 'pending'  -- pending | approved | edited | rejected
);
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

| Variable           | Description                                               |
| ------------------ | --------------------------------------------------------- |
| `DATABASE_URL`     | Neon PostgreSQL connection string                         |
| `JWT_SECRET`       | Secret key for JWT signing (min 32 chars)                 |
| `OLLAMA_URL`       | Ollama server URL (default: http://localhost:11434)       |
| `PINECONE_API_KEY` | Pinecone API key                                          |
| `PINECONE_INDEX`   | Pinecone index name (default: fashion-rag)                |
| `PINECONE_CLOUD`   | Pinecone cloud provider (default: aws)                    |
| `PINECONE_REGION`  | Pinecone region (default: us-east-1)                      |
| `CHAT_MODEL`       | Ollama chat model (default: llama3.1:8b)                  |
| `SQL_MODEL`        | Ollama SQL/routing model (default: qwen2.5-coder:1.5b)   |
| `EMBED_MODEL`      | Ollama embedding model (default: nomic-embed-text:latest) |

### Frontend (`frontend/.env.local`)

| Variable              | Description     |
| --------------------- | --------------- |
| `NEXT_PUBLIC_API_URL` | Backend API URL |

---

## API Reference

### Auth

| Method | Endpoint         | Description                  |
| ------ | ---------------- | ---------------------------- |
| POST   | `/auth/register` | Register new user            |
| POST   | `/auth/login`    | Login, get JWT               |
| GET    | `/auth/me`       | Get current user             |
| POST   | `/auth/logout`   | Logout (clears client token) |

### Chat

| Method | Endpoint                       | Description        |
| ------ | ------------------------------ | ------------------ |
| POST   | `/chat/sessions`               | Create session     |
| GET    | `/chat/sessions`               | List user sessions |
| GET    | `/chat/sessions/{id}/messages` | Get messages       |
| DELETE | `/chat/sessions/{id}`          | Delete session     |
| POST   | `/chat/send`                   | Send message       |
| GET    | `/chat/review/status/{id}`     | Poll review status |

### Review Queue

| Method | Endpoint                    | Description          |
| ------ | --------------------------- | -------------------- |
| GET    | `/review/queue`             | List review items    |
| POST   | `/review/approve/{id}`      | Approve review item  |
| POST   | `/review/reject/{id}`       | Reject review item   |
| POST   | `/review/edit/{id}`         | Edit review response |

---

## Agent System

### Router Agent

Uses `qwen2.5-coder:1.5b` to classify queries into one of three routes:

- `sql` → product data questions (inventory, prices, stock, filters)
- `rag` → policy questions (shipping, returns, exchange, FAQ)
- `chat` → general conversation and small talk

Returns a confidence score. If `< 0.75`, the query is flagged for human review.

### SQL Agent (`app/sql_agent.py`)

```
User question
    ↓
retrieve_relevant_schema(question, k=4)   ← Pinecone similarity search on sql_schema namespace
    ↓
LLM prompt: question + relevant schema chunks → generates SQL
    ↓
validate_sql()   ← blocks DELETE/UPDATE/DROP/ALTER/TRUNCATE/INSERT
    ↓
verify_sql()     ← runs EXPLAIN {sql} against Neon to catch syntax errors
    ↓
execute_sql()    ← runs query, returns list[dict]
    ↓ (on failure, up to 2 retries)
repair_sql()     ← LLM re-generates with error message + relevant schema
```

**Blocked operations:** `DELETE`, `UPDATE`, `DROP`, `ALTER`, `TRUNCATE`, `INSERT` — only `SELECT` is permitted.

### RAG Agent (`app/rag.py`)

- Embeds query with `nomic-embed-text:latest`
- Retrieves top-3 chunks from Pinecone (`rag_docs` namespace)
- Generates answer grounded strictly in retrieved context
- Falls back to `"Information not available."` if context is empty

### Chat Agent

- Multi-turn conversation with session history (last 8 messages)
- General assistant persona for greetings and small talk

---

## Pinecone Setup

### Index configuration

```python
pc.create_index(
    name="fashion-rag",
    dimension=768,          # nomic-embed-text:latest output dimension
    metric="cosine",
    spec=ServerlessSpec(cloud="aws", region="us-east-1")
)
```

### Namespaces

| Namespace    | Contents                              | Used by   |
| ------------ | ------------------------------------- | --------- |
| `rag_docs`   | Chunked text from PDFs and TXT files  | RAG agent |
| `sql_schema` | Per-table schema descriptions as docs | SQL agent |

---

## Auth System (Manual JWT)

- `hash_password(password)` — bcrypt via passlib, rejects passwords > 72 bytes
- `verify_password(plain, hashed)` — constant-time comparison
- `create_token(data)` — HS256 JWT with 24-hour expiry
- Register validates email uniqueness, hashes password, returns JWT + user object
- Response shape: `{ access_token, token_type: "bearer", user: { id, email, full_name } }`

---

## Memory (`app/memory.py`)

Simple in-memory dict keyed by session ID. Stores last N user messages for multi-turn context. The SQL agent uses `history[-2:]` (last 2 user messages) to resolve follow-up queries like "only show black ones".

```python
memory: dict = {}

def load(session) -> dict:
    return memory.get(session, {})

def save(session, message: str):
    state = load(session)
    state.setdefault("history", []).append(message)
    memory[session] = state

def clear(session):
    memory.pop(session, None)
```

---

## Human-in-the-Loop Flow

Responses are automatically queued for review when routing confidence is below 0.75 or an agent raises an exception.

```
User sends message
    ↓
Exception raised (SQL error, routing failure, low confidence, etc.)
    ↓
push_review(query, error, "execution_error") → returns review_id
    ↓
Response: { message: "Queued for review", review: true, review_id: 42 }
    ↓
Frontend shows "Awaiting review" banner with pulsing dots
    ↓
Frontend polls GET /chat/review/status/42 every 2500ms
    ↓
Admin opens Review Panel → sees queue → clicks Approve / Edit / Reject
    ↓
POST /review/approve/42 → returns { message: "resolved answer" }
    ↓
Poller receives status != "pending" → resolves banner to message bubble
    ↓
Review panel refreshes queue count
```

### Review Routes

| Endpoint                    | Description                        | Returns                                     |
| --------------------------- | ---------------------------------- | ------------------------------------------- |
| `GET /review/queue`         | All pending items                  | `[{id, query, response, reason, status}]`   |
| `POST /review/approve/{id}` | Set status = approved              | `{success, id, status, message, query}`     |
| `POST /review/reject/{id}`  | Set status = rejected              | `{success, id, status, message}`            |
| `POST /review/edit/{id}`    | Update response, set status=edited | `{success, id, status, message}`            |

> **Note:** `approve` and `edit` must return `message` in the response body so the frontend can display it immediately after the poller fires — no second round-trip needed.

---

## Frontend Architecture (Next.js 14)

### Zustand store (`store/chatStore.ts`)

```typescript
interface ChatStore {
  sessions: Session[];
  activeSession: number | null;
  messages: Record<number, Message[]>;
  reviewItems: ReviewItem[];
  isStreaming: boolean;

  addMessage: (sessionId: number, msg: Message) => void;
  setStreaming: (v: boolean) => void;
  loadReviewQueue: () => Promise<void>;
  resolveReviewMessage: (reviewId: number, text: string) => void;
}
```

### Message rendering

| `agent` value  | Render as                                          |
| -------------- | -------------------------------------------------- |
| `sql`          | Parse `\n\n`-separated blocks → Product card grid  |
| `rag`          | Plain text bubble                                  |
| `chat`         | Plain text bubble                                  |
| `review: true` | "Awaiting review" banner, starts polling           |

### Product card parsing

`format_result()` returns blocks like:

```
Name: Air Sprint Low
Category: Shoes
Price: ₹2499
Brand: Nike
Color: Black
Stock: 15
```

Split on `\n\n` to get blocks, then split each line on `:` to get key-value pairs. Render as cards with category emoji, price in gold, and a stock indicator dot.

---

## Setup & Run Sequence

```bash
# 1. Pull Ollama models
ollama pull qwen2.5-coder:1.5b
ollama pull nomic-embed-text:latest

# 2. Backend dependencies
cd backend
pip install fastapi uvicorn sqlalchemy asyncpg python-jose passlib[bcrypt] \
    python-dotenv langchain langchain-community langchain-ollama \
    langchain-pinecone langchain-text-splitters pinecone-client pypdf pandas

# 3. Configure environment
cp .env.example .env
# Fill in DATABASE_URL, JWT_SECRET, PINECONE_API_KEY, etc.

# 4. Run database migrations (auto via SQLAlchemy on startup)
uvicorn app.main:app --reload --port 8000

# 5. Seed products
python -m app.scripts.seed          # imports data/products.csv → Neon products table

# 6. Ingest schema into Pinecone (run once after seeding)
python -m app.scripts.ingest_schema # embeds table schemas → sql_schema namespace

# 7. Ingest RAG documents into Pinecone (run once, re-run when docs change)
python -m app.scripts.ingest_rag    # embeds data/docs/ → rag_docs namespace

# 8. Frontend
cd ../frontend
npm install
npm run dev                         # http://localhost:3000
```

---

## Deployment

### Backend → Render

1. Create a new **Web Service** on Render
2. Connect your repo, set root directory to `backend/`
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add all environment variables in the Render dashboard

### Frontend → Vercel

1. Import the repo on Vercel
2. Set root directory to `frontend/`
3. Add environment variable: `NEXT_PUBLIC_API_URL=https://your-render-app.onrender.com`
4. Deploy

---

## Policy Documents (`data/docs/`)

| File                   | Contents                                                                 |
| ---------------------- | ------------------------------------------------------------------------ |
| `refund_policy.txt`    | 7-day return window, unworn/unwashed with tags, 5–7 day refund, no sale returns |
| `shipping_policy.txt`  | Free shipping ₹999+, standard ₹79 (3–5 days), express ₹149 (1–2 days)  |
| `exchange_policy.txt`  | 14-day exchange window, free size swaps, one exchange per order          |
| `faq.txt`              | Order tracking, cancellation window, international shipping, support contact |

---

## Key Constraints & Rules

1. **LLM:** Only `qwen2.5-coder:1.5b` via Ollama — no OpenAI or Anthropic API calls in the app
2. **Embeddings:** Only `nomic-embed-text:latest` via Ollama — dimension must be 768 in Pinecone
3. **SQL safety:** Block all write operations. Only `SELECT`. Validate → EXPLAIN → execute
4. **Schema retrieval:** Always fetch from Pinecone first — never send the full schema to the LLM unless Pinecone fails
5. **Auth:** Manual JWT — no OAuth, no NextAuth, no third-party auth libraries
6. **Review IDs:** `push_review` must return the inserted row ID (use `RETURNING id`)
7. **Polling:** Frontend polls every 2500ms, stops as soon as status != `"pending"`
8. **Memory:** Last 2 user messages appended to SQL queries for follow-up context
9. **Pinecone index:** Single index `fashion-rag`, two namespaces: `rag_docs` + `sql_schema`
10. **PDF support:** Both `.pdf` and `.txt` files must be supported in RAG ingestion
