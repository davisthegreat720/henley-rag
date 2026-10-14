import uuid

import psycopg

from henley_rag.models.document import SourceDocument


def upsert_document(connection: psycopg.Connection, document: SourceDocument) -> None:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO documents (
                id,
                source_system,
                source_document_id,
                source_path,
                filename,
                content_type,
                checksum,
                source_modified_at,
                ingestion_status
            )
            VALUES (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                'pending'
            )
            ON CONFLICT (source_system, source_document_id)
            DO UPDATE SET
                source_path = EXCLUDED.source_path,
                filename = EXCLUDED.filename,
                content_type = EXCLUDED.content_type,
                checksum = EXCLUDED.checksum,
                source_modified_at = EXCLUDED.source_modified_at,
                updated_at = NOW()
            """,
            (
                uuid.uuid4(),
                document.source_system,
                document.source_document_id,
                document.source_path,
                document.filename,
                document.content_type,
                document.checksum,
                document.modified_at,
            ),
        )