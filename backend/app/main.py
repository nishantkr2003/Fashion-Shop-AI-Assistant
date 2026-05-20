from fastapi import FastAPI
from app.routes.auth_routes import router
from app.routes.profile_routes import router as profile_router
from app.routes.chat_routes import (
    router as chat_router
)
from fastapi.middleware.cors import (
    CORSMiddleware
)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000"
        
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(router)
app.include_router(profile_router)
app.include_router(chat_router)
@app.get("/health")
async def health():
    return {
        "status": "ok"
    }