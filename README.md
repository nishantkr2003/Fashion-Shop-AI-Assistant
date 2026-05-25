# Fashion Shop AI Assistant — Master Build Prompt

## Project Identity

Build a full-stack AI assistant for a fashion e-commerce shop called **Folio**. The system answers customer questions by routing them to the correct agent: SQL for product data, RAG for policies and FAQs, and Chat for general conversation. All AI runs locally via Ollama. Vectors are stored in Pinecone. The database is Neon (PostgreSQL).

---

## Tech Stack

### Backend
- **Runtime:** Python 3.11+
- **Framework:** FastAPI
- **ORM:** SQLAlchemy (async with asyncpg)
- **Database:** Neon (PostgreSQL, serverless) — `DATABASE_URL` in `.env`
- **LLM:** Ollama — `qwen2.5-coder:1.5b` for all generation and routing
- **Embeddings:** Ollama — `nomic-embed-text:latest`
- **Vector Store:** Pinecone (Serverless, AWS us-east-1)
- **Auth:** Manual JWT — `python-jose`, `passlib[bcrypt]`
- **AI framework:** LangChain (agents, RAG, text splitters)
- **PDF loading:** `pypdf`, `langchain-community` PyPDFLoader
- **CSV import:** `pandas`
- **Env:** `python-dotenv`

### Frontend
- **Framework:** Next.js 14 (App Router)
- **State:** Zustand
- **UI components:** ShadCN UI
- **Styling:** Tailwind CSS
- **HTTP:** native fetch with streaming (ReadableStream)

### Models (Ollama — must be pulled before running)
```
ollama pull qwen2.5-coder:1.5b
ollama pull nomic-embed-text:latest
```

---

## Environment Variables

### Backend `.env`
```
DATABASE_URL=postgresql+asyncpg://user:pass@host/dbname   # Neon connection string
JWT_SECRET=your_random_secret_here
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX=fashion-rag
PINECONE_CLOUD=aws
PINECONE_REGION=us-east-1
OLLAMA_BASE_URL=http://localhost:11434
```

### Frontend `.env.local`
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

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
└── README.md
```

---

## Database Schema (Neon / PostgreSQL)

```sql
CREATE TABLE users (
    id          SERIAL PRIMARY KEY,
    full_name   VARCHAR NOT NULL,
    email       VARCHAR UNIQUE NOT NULL,
    password_hash VARCHAR NOT NULL,
    created_at  TIMESTAMP DEFAULT NOW()
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

### Products CSV format (`data/products.csv`)
```
name,category,price,brand,color,stock
Air Sprint Low,Shoes,2499,Nike,Black,15
...
```
Generate at least 50 real-sounding products across: Shoes, Hoodies, Jackets, Jeans, T-Shirts, Bags. Use believable Indian prices (₹500–₹8000). Mix in-stock and out-of-stock items.

---

## Auth System (Manual JWT)

### `app/auth.py`
- `hash_password(password: str) -> str` — bcrypt via passlib, reject if > 72 bytes
- `verify_password(plain: str, hashed: str) -> bool`
- `create_token(data: dict) -> str` — HS256 JWT, 24-hour expiry, uses `JWT_SECRET`

### `app/routes/auth.py`
- `POST /auth/register` — validate email uniqueness, hash password, create user, return JWT + user
- `POST /auth/login` — verify credentials, return JWT + user
- Schemas: `RegisterInput(full_name, email, password: min_length=8, max_length=72)`, `LoginInput(email, password)`
- Return shape: `{ access_token, token_type: "bearer", user: { id, email, full_name } }`

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
| Namespace     | Contents                                 | Used by         |
|---------------|------------------------------------------|-----------------|
| `rag_docs`    | Chunked text from PDFs and TXT files     | RAG agent       |
| `sql_schema`  | Per-table schema descriptions as docs    | SQL agent       |

### Embeddings
Use `OllamaEmbeddings(model="nomic-embed-text:latest")` for all embedding operations.

---

## SQL Agent (`app/sql_agent.py`)

This is the core fix. The original agent sent the raw full schema to the LLM every time. The new flow uses Pinecone semantic search to retrieve only the relevant tables before generation.

### Flow
```
User question
    ↓
retrieve_relevant_schema(question, k=4)   ← Pinecone similarity search on sql_schema namespace
    ↓
LLM prompt: question + relevant schema chunks → generates SQL
    ↓
validate_sql()   ← blocks DELETE/UPDATE/DROP/ALTER/TRUNCATE/INSERT, SELECT only
    ↓
verify_sql()     ← runs EXPLAIN {sql} against Neon, catches syntax errors early
    ↓
execute_sql()    ← runs query, returns list[dict]
    ↓ (on failure, up to 2 retries)
repair_sql()     ← LLM re-generates with error message + relevant schema
```

### Key functions

```python
def ingest_schema():
    """Call once after migrations. Embeds each table as a Document into sql_schema namespace."""
    schema = read_schema()  # reads from information_schema.columns
    docs = [
        Document(
            page_content=f"Table: {table}\nColumns:\n" + "\n".join(f"  - {c}" for c in cols),
            metadata={"table": table}
        )
        for table, cols in schema.items()
    ]
    store = PineconeVectorStore(index_name=PINECONE_INDEX, embedding=embeddings, namespace="sql_schema")
    store.add_documents(docs)

def retrieve_relevant_schema(question: str, k: int = 4) -> str:
    """Semantic search → returns formatted schema string for the most relevant tables."""
    store = PineconeVectorStore(...)
    results = store.similarity_search(question, k=k)
    return "\n\n".join(r.page_content for r in results)
    # Falls back to full schema string if Pinecone fails

def generate_sql(question: str) -> str:
    relevant_schema = retrieve_relevant_schema(question)
    prompt = f"""
You are a PostgreSQL expert.
Generate a single valid PostgreSQL SELECT statement.

Relevant schema:
{relevant_schema}

STRICT RULES:
- Use ONLY columns from the schema above.
- Do NOT invent joins or foreign keys.
- If one table is sufficient, do NOT join.
- Use ILIKE for text search.
- Always add LIMIT 10.
- Return ONLY the raw SQL — no explanation, no markdown.

Question: {question}
"""
    sql = clean_sql(llm.invoke(prompt).content)
    validate_sql(sql)
    return sql
```

### Blocked operations
```python
BLOCKED = {"delete", "update", "drop", "alter", "truncate", "insert"}
```

---

## RAG Agent (`app/rag.py`)

### Ingestion
```python
def ingest():
    """Loads all .pdf and .txt from data/docs/, chunks, embeds, stores in rag_docs namespace."""
    for file in Path("data/docs").iterdir():
        if file.suffix == ".pdf":
            loader = PyPDFLoader(str(file))
        elif file.suffix == ".txt":
            loader = TextLoader(str(file), encoding="utf-8")
        raw = loader.load()
        chunks = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50).split_documents(raw)
        store.add_documents(chunks)
```

### Retrieval
```python
def retrieve(query: str, k: int = 3) -> list:
    store = PineconeVectorStore(
        index_name=PINECONE_INDEX,
        embedding=embeddings,
        namespace="rag_docs",
        pinecone_api_key=PINECONE_API_KEY
    )
    return store.similarity_search(query, k=k)
```

### Agent prompt
```
Answer ONLY from the context below.
If the answer is not in the context, say: "Information not available."

Context:
{context}

Question: {question}
```

---

## Router Agent (`app/agents.py`)

Uses `qwen2.5-coder:1.5b` via `ChatOllama`. Returns one of: `sql`, `rag`, `chat`.

### Prompt
```
Classify the query. Return EXACTLY ONE word: sql, rag, or chat.

sql  → product data, price, inventory, stock, filter, show, compare
rag  → refund, shipping, exchange, FAQ, policy, delivery, return
chat → greetings, general conversation, small talk

Query: {query}
```

### Logic
```python
result = llm.invoke(prompt).content.lower().strip()
if "rag"  in result: return {"agent": "rag",  "confidence": 0.95}
if "sql"  in result: return {"agent": "sql",  "confidence": 0.95}
return                        {"agent": "chat", "confidence": 0.90}
```

---

## Chat Route (`app/routes/chat.py`)

### `POST /chat/send`

```python
@router.post("/send")
def send(payload: ChatRequest):
    session = 1   # replace with JWT user ID when auth is wired
    route = router_agent(payload.message)

    try:
        if route["agent"] == "sql":
            memory  = load(session)
            history = memory.get("history", [])
            context = "\n".join(history[-2:])          # last 2 turns for context
            query   = (context + "\n" + payload.message).strip()

            result     = sql_agent(query)
            rows       = result["rows"]
            confidence = evaluate(rows)
            formatted  = format_result(rows)
            save(session, payload.message)

            return {"message": formatted, "review": False, "confidence": confidence}

        if route["agent"] == "rag":
            answer = rag_agent(payload.message)
            return {"message": answer, "review": False}

        reply = chat_agent(payload.message)
        return {"message": reply, "review": False}

    except Exception as e:
        review_id = push_review(payload.message, str(e), "execution_error")
        return {
            "message":   "Your question has been queued for human review.",
            "review":    True,
            "review_id": review_id,
        }
```

### `GET /chat/review/status/{review_id}` — Human-in-the-loop polling

```python
@router.get("/review/status/{review_id}")
def review_status(review_id: int):
    row = conn.execute("SELECT status, response FROM review_queue WHERE id = :id")
    status = row["status"]

    if status == "pending":
        return {"status": "pending", "review": True,  "message": "Awaiting review…"}
    if status == "rejected":
        return {"status": "rejected","review": False, "message": "Sorry, I couldn't answer that."}
    # approved or edited:
    return {"status": status, "review": False, "message": row["response"]}
```

---

## Review Routes (`app/routes/review.py`)

| Endpoint | Description | Returns |
|---|---|---|
| `GET /review/queue` | All pending items | `[{id, query, response, reason, status}]` |
| `POST /review/approve/{id}` | Set status=approved | `{success, id, status, message, query}` |
| `POST /review/reject/{id}` | Set status=rejected | `{success, id, status, message}` |
| `POST /review/edit/{id}` | Update response, set status=edited | `{success, id, status, message}` |

**Critical:** `approve` and `edit` must return `message` (the resolved response) in the body so the frontend can display it immediately after the poller fires — no second round-trip needed.

---

## Memory (`app/memory.py`)

Simple in-memory dict keyed by session ID. Stores last N user messages for multi-turn context.

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

The SQL agent uses `history[-2:]` (last 2 user messages) to resolve follow-up queries like "only black ones".

---

## Human-in-the-Loop Flow

```
User sends message
    ↓
Exception raised (SQL error, routing failure, etc.)
    ↓
push_review(query, error, "execution_error") → returns review_id
    ↓
Response: { message: "Queued for review", review: true, review_id: 42 }
    ↓
Frontend shows "Awaiting review" banner with pulsing dots
    ↓
Frontend polls GET /chat/review/status/42 every 2500ms
    ↓
Admin opens Review Panel → sees queue → clicks Approve
    ↓
POST /review/approve/42 → returns { message: "resolved answer" }
    ↓
Poller receives status != "pending" → resolves banner to message bubble
    ↓
Review panel refreshes queue count
```

---

## Frontend Architecture (Next.js 14)

### Zustand store (`store/chatStore.ts`)
```typescript
interface ChatStore {
  sessions: Session[]
  activeSession: number | null
  messages: Record<number, Message[]>
  reviewItems: ReviewItem[]
  isStreaming: boolean

  addMessage: (sessionId: number, msg: Message) => void
  setStreaming: (v: boolean) => void
  loadReviewQueue: () => Promise<void>
  resolveReviewMessage: (reviewId: number, text: string) => void
}
```

### API layer (`lib/api.ts`)
```typescript
export const sendMessage   = (msg: string)   => fetch(`${API}/chat/send`, { method: 'POST', ... })
export const pollStatus    = (id: number)    => fetch(`${API}/chat/review/status/${id}`)
export const getQueue      = ()              => fetch(`${API}/review/queue`)
export const approveItem   = (id: number)   => fetch(`${API}/review/approve/${id}`, { method: 'POST' })
export const rejectItem    = (id: number)   => fetch(`${API}/review/reject/${id}`,  { method: 'POST' })
```

### Message types
| `agent` value | Render as |
|---|---|
| `sql` | Parse `\n\n`-separated blocks → Product card grid |
| `rag` | Plain text bubble |
| `chat` | Plain text bubble |
| `review: true` | "Awaiting review" banner, starts polling |

### Product card parsing
SQL `format_result()` returns blocks like:
```
Name: Air Sprint Low
Category: Shoes
Price: ₹2499
Brand: Nike
Color: Black
Stock: 15
```
Parse each block by splitting on `\n`, then `:` to get key-value pairs. Render as cards with category emoji, price in gold, stock indicator dot.

### Streaming
Use `ReadableStream` on `POST /chat/send`. The current backend returns a full JSON response, not a stream. To add streaming, wrap `stream.py`'s `StreamingResponse` around the final formatted text. Frontend reads chunks via `reader.read()` in a loop and appends tokens to the message.

---

## Setup & Run Sequence

```bash
# 1. Pull models
ollama pull qwen2.5-coder:1.5b
ollama pull nomic-embed-text:latest

# 2. Backend dependencies
cd backend
pip install fastapi uvicorn sqlalchemy asyncpg python-jose passlib[bcrypt] \
    python-dotenv langchain langchain-community langchain-ollama \
    langchain-pinecone langchain-text-splitters pinecone-client pypdf pandas

# 3. Run database migrations (auto via SQLAlchemy on startup)
# Tables created by Base.metadata.create_all(bind=engine) in main.py

# 4. Seed products
python -m app.scripts.seed          # imports data/products.csv → Neon products table

# 5. Ingest schema into Pinecone (run once after seeding)
python -m app.scripts.ingest_schema # embeds table schemas → sql_schema namespace

# 6. Ingest RAG documents into Pinecone (run once, re-run when docs change)
python -m app.scripts.ingest_rag    # embeds data/docs/ → rag_docs namespace

# 7. Start backend
uvicorn app.main:app --reload --port 8000

# 8. Frontend
cd ../frontend
npm install
npm run dev                         # http://localhost:3000
```

---

## Policy Documents to Create (`data/docs/`)

Create realistic brand-style documents for a fashion shop called Folio.

### `refund_policy.pdf` or `refund_policy.txt`
- 7-day return window from delivery date
- Items must be unworn, unwashed, with original tags
- Refund processed within 5–7 business days to original payment method
- Sale items are non-refundable
- Process: raise return request on website → receive return label → ship back

### `shipping_policy.txt`
- Free shipping on orders above ₹999
- Standard shipping: ₹79, 3–5 business days
- Express shipping: ₹149, 1–2 business days
- No delivery to PO boxes
- Orders placed before 2pm dispatched same day

### `exchange_policy.txt`
- Exchange allowed within 14 days
- Size exchanges are free
- Style exchanges subject to price difference
- Only one exchange per order

### `faq.txt`
- How do I track my order? → Check email for tracking link
- Can I cancel after placing? → Within 1 hour of placing
- Do you ship internationally? → Not currently
- How do I contact support? → support@folio.in or WhatsApp +91-XXXXXXXXXX

---

## Key Constraints & Rules

1. **LLM:** Only `qwen2.5-coder:1.5b` via Ollama — no OpenAI, no Anthropic API calls in the app
2. **Embeddings:** Only `nomic-embed-text:latest` via Ollama — dimension must be 768 in Pinecone
3. **SQL safety:** Block all write operations. Only `SELECT`. Validate before EXPLAIN, EXPLAIN before execute
4. **Schema retrieval:** Always fetch from Pinecone first — never send the full schema string to the LLM unless Pinecone fails
5. **Auth:** Manual JWT — no OAuth, no NextAuth, no third-party auth library
6. **Review IDs:** `push_review` must return the inserted row ID (use `RETURNING id`)
7. **Polling:** Frontend polls every 2500ms, stops as soon as status != "pending"
8. **Memory:** Last 2 user messages appended to SQL queries for follow-up context
9. **Pinecone index:** Single index `fashion-rag`, two namespaces `rag_docs` + `sql_schema`
10. **PDF support:** Both `.pdf` and `.txt` files must be supported in RAG ingestion
