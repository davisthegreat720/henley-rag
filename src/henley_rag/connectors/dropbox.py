import os

import dropbox
from dropbox.files import FileMetadata
from dotenv import load_dotenv

from henley_rag.connectors.base import DocumentSource
from henley_rag.models.document import SourceDocument


load_dotenv()


class DropboxSource(DocumentSource):
    def __init__(self):
        self.client = dropbox.Dropbox(os.environ["DROPBOX_ACCESS_TOKEN"])
        self.root_path = os.getenv("DROPBOX_ROOT_PATH", "")

    def list_documents(self) -> list[SourceDocument]:
        result = self.client.files_list_folder(
            self.root_path,
            recursive=True,
        )

        documents = []

        while True:
            for entry in result.entries:
                if isinstance(entry, FileMetadata):
                    documents.append(
                        SourceDocument(
                            source_system="dropbox",
                            source_document_id=entry.id,
                            filename=entry.name,
                            source_path=entry.path_display,
                            checksum=entry.content_hash,
                            modified_at=entry.server_modified,
                        )
                    )

            if not result.has_more:
                break

            result = self.client.files_list_folder_continue(result.cursor)

        return documents

    def fetch_document(self, document_id: str) -> SourceDocument:
        metadata, response = self.client.files_download(document_id)

        return SourceDocument(
            source_system="dropbox",
            source_document_id=metadata.id,
            filename=metadata.name,
            source_path=metadata.path_display,
            checksum=metadata.content_hash,
            modified_at=metadata.server_modified,
            content=response.content,
        )