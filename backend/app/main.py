from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import engine, Base
from app.auth import router as auth_router
from app.chat import router as chat_router
from app.csv_import import router as import_router
from app.review import router as review_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fashion Shop AI", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://*.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(chat_router, prefix="/chat", tags=["chat"])
app.include_router(import_router, prefix="/import", tags=["import"])
app.include_router(review_router, prefix="/review", tags=["review"])

@app.get("/health")
def health():
    return {"status": "ok"}
