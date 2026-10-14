import os

import httpx
import psycopg
from fastapi import FastAPI
from qdrant_client import QdrantClient

app = FastAPI(title="Henley RAG API")

DATABASE_URL = os.environ["DATABASE_URL"]
QDRANT_URL = os.environ["QDRANT_URL"]
OLLAMA_URL = os.environ["OLLAMA_URL"]


@app.get("/health")
def health():
    status = {
        "api": "ok",
        "postgres": "unknown",
        "qdrant": "unknown",
        "ollama": "unknown",
    }

    try:
        with psycopg.connect(DATABASE_URL) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1;")
        status["postgres"] = "ok"
    except Exception as exc:
        status["postgres"] = f"error: {exc}"

    try:
        client = QdrantClient(url=QDRANT_URL)
        client.get_collections()
        status["qdrant"] = "ok"
    except Exception as exc:
        status["qdrant"] = f"error: {exc}"

    try:
        response = httpx.get(f"{OLLAMA_URL}/api/tags", timeout=5.0)
        response.raise_for_status()
        status["ollama"] = "ok"
    except Exception as exc:
        status["ollama"] = f"error: {exc}"

    return status