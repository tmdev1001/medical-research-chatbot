from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.chat import router as chat_router
from backend.config import get_settings

settings = get_settings()

app = FastAPI(
    title="Clinical Research RAG Chatbot",
    version="0.1.0",
    description="MVP Retrieval-Augmented Generation chatbot for clinical research studies.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


app.include_router(chat_router, prefix="/api")


@app.on_event("startup")
def on_startup() -> None:
    _ = settings

