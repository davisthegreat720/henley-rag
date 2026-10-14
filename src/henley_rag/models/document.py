from dataclasses import dataclass
from datetime import datetime


@dataclass
class SourceDocument:
    source_system: str
    source_document_id: str
    filename: str
    source_path: str | None = None
    content_type: str | None = None
    checksum: str | None = None
    modified_at: datetime | None = None
    content: bytes | None = None