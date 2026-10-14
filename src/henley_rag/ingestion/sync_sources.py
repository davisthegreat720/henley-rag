import os

import psycopg
from dotenv import load_dotenv

from henley_rag.connectors.dropbox import DropboxSource
from henley_rag.storage.documents import upsert_document


load_dotenv()


def sync_dropbox_documents():
    source = DropboxSource()
    documents = source.list_documents()

    database_url = os.environ["DATABASE_URL"]

    with psycopg.connect(database_url) as connection:
        for document in documents:
            upsert_document(connection, document)

        connection.commit()

    print(f"Registered {len(documents)} Dropbox documents.")


if __name__ == "__main__":
    sync_dropbox_documents()