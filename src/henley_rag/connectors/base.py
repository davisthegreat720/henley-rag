from abc import ABC, abstractmethod

from henley_rag.models.document import SourceDocument


class DocumentSource(ABC):

    @abstractmethod
    def list_documents(self) -> list[SourceDocument]:
        """Return documents available from the source."""
        pass

    @abstractmethod
    def fetch_document(self, document_id: str) -> SourceDocument:
        """Fetch one document and its content."""
        pass