CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY,
    source_system TEXT NOT NULL,
    source_document_id TEXT NOT NULL,
    source_path TEXT,
    filename TEXT NOT NULL,
    content_type TEXT,
    checksum TEXT,
    source_modified_at TIMESTAMPTZ,
    last_indexed_at TIMESTAMPTZ,
    ingestion_status TEXT NOT NULL DEFAULT 'pending',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (source_system, source_document_id)
);