# app/main.py
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent.parent / "data" / ".env")

from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.langsmith_config import setup_langsmith
from app.routers import descriptions, chatbot, orders


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown logic."""
    setup_langsmith()
    print("✅ LangSmith tracing configured")
    yield
    print("👋 Shutting down Maison Beauté AI Advisor")


app = FastAPI(
    title="Maison Beauté AI Advisor",
    description="Privacy-first AI system for pre-loved luxury beauty — Modules 1, 2 & 3",
    version="1.0.0",
    lifespan=lifespan,
)

# ─── Routers ──────────────────────────────────────────────────
app.include_router(descriptions.router, prefix="/products", tags=["Module 1 — Shop Manager"])
app.include_router(chatbot.router,      prefix="/chat",     tags=["Module 2 — Beauty Advisor"])
app.include_router(orders.router,       prefix="/orders",   tags=["Module 3 — Order Concierge"])


@app.get("/", tags=["Health"])
async def root():
    return {
        "service": "Maison Beauté AI Advisor",
        "version": "1.0.0",
        "status": "running",
        "modules": ["M1 Shop Manager", "M2 Beauty Advisor", "M3 Order Concierge"],
    }


@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok"}
