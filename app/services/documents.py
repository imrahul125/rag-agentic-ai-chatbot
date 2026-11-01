from dataclasses import dataclass
from threading import RLock
from time import time
from uuid import uuid4

from langchain_chroma import Chroma

from app.config import (
    DOCUMENT_TTL_SECONDS,
    MAX_ACTIVE_DOCUMENTS,
)
from app.services.embeddings import get_embedding_model
from app.services.ingest import load_and_split_pdf_bytes


@dataclass
class DocumentRecord:
    document_id: str
    filename: str
    page_count: int
    chunk_count: int
    size_bytes: int
    vector_db: Chroma
    last_accessed: float


class DocumentStore:
    """Process-local, per-upload indexes with an inactivity expiry."""

    def __init__(
        self,
        ttl_seconds: int = DOCUMENT_TTL_SECONDS,
        max_documents: int = MAX_ACTIVE_DOCUMENTS,
    ):
        self.ttl_seconds = ttl_seconds
        self.max_documents = max_documents
        self._documents: dict[str, DocumentRecord] = {}
        self._lock = RLock()

    def add_pdf(self, pdf_bytes: bytes, filename: str) -> DocumentRecord:
        safe_name = filename.rsplit("/", 1)[-1].rsplit("\\", 1)[-1]
        safe_name = safe_name.strip() or "document.pdf"
        chunks = load_and_split_pdf_bytes(pdf_bytes, safe_name)
        document_id = uuid4().hex
        collection_name = f"document_{document_id}"
        vector_db = Chroma.from_documents(
            documents=chunks,
            embedding=get_embedding_model(),
            collection_name=collection_name,
            collection_metadata={"hnsw:space": "cosine"},
        )
        pages = {
            chunk.metadata.get("page")
            for chunk in chunks
            if chunk.metadata.get("page") is not None
        }
        record = DocumentRecord(
            document_id=document_id,
            filename=safe_name,
            page_count=len(pages),
            chunk_count=len(chunks),
            size_bytes=len(pdf_bytes),
            vector_db=vector_db,
            last_accessed=time(),
        )

        with self._lock:
            self._purge_expired_locked()
            self._documents[document_id] = record
            while len(self._documents) > self.max_documents:
                oldest_id = min(
                    self._documents,
                    key=lambda key: self._documents[key].last_accessed,
                )
                self._delete_locked(oldest_id)
        return record

    def get(self, document_id: str) -> DocumentRecord | None:
        with self._lock:
            self._purge_expired_locked()
            record = self._documents.get(document_id)
            if record is not None:
                record.last_accessed = time()
            return record

    def delete(self, document_id: str) -> bool:
        with self._lock:
            self._purge_expired_locked()
            return self._delete_locked(document_id)

    def _purge_expired_locked(self):
        cutoff = time() - self.ttl_seconds
        expired_ids = [
            document_id
            for document_id, record in self._documents.items()
            if record.last_accessed < cutoff
        ]
        for document_id in expired_ids:
            self._delete_locked(document_id)

    def _delete_locked(self, document_id: str) -> bool:
        record = self._documents.pop(document_id, None)
        if record is None:
            return False
        try:
            record.vector_db.delete_collection()
        except Exception:
            # Expired records should not prevent the rest of the app from running.
            pass
        return True


document_store = DocumentStore()
