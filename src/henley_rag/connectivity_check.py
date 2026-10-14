import os

import httpx
import psycopg
from dotenv import load_dotenv
from qdrant_client import QdrantClient

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]
QDRANT_URL = os.environ["QDRANT_URL"]
OLLAMA_URL = os.environ["OLLAMA_URL"]
OLLAMA_MODEL = os.environ["OLLAMA_MODEL"]


def check_postgres():
    with psycopg.connect(DATABASE_URL) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
            result = cursor.fetchone()

    print(f"PostgreSQL: OK {result}")


def check_qdrant():
    client = QdrantClient(url=QDRANT_URL)
    collections = client.get_collections()

    print(f"Qdrant: OK {collections}")


def check_ollama():
    response = httpx.get(f"{OLLAMA_URL}/api/tags")
    response.raise_for_status()

    models = response.json()
    print(f"Ollama: OK {models}")


if __name__ == "__main__":
    check_postgres()
    check_qdrant()
    check_ollama()