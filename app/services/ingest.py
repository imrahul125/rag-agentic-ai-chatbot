from io import BytesIO
from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader

from app.config import (
    MAX_EXTRACTED_CHARACTERS,
    MAX_PDF_PAGES,
    MAX_PDF_UPLOAD_BYTES,
    PROJECT_ROOT,
)


DEFAULT_PDF_PATH = PROJECT_ROOT / "data" / "Ebook-Agentic-AI.pdf"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 180


def load_and_split_pdf_bytes(pdf_bytes: bytes, filename: str = "document.pdf"):
    """Validate and split a text-searchable PDF without saving its contents."""
    if not pdf_bytes:
        raise ValueError("The uploaded PDF is empty.")
    if len(pdf_bytes) > MAX_PDF_UPLOAD_BYTES:
        limit_mb = MAX_PDF_UPLOAD_BYTES // (1024 * 1024)
        raise ValueError(f"PDF files must be {limit_mb} MB or smaller.")
    if b"%PDF-" not in pdf_bytes[:1024]:
        raise ValueError("The uploaded file is not a valid PDF.")

    try:
        reader = PdfReader(BytesIO(pdf_bytes), strict=False)
        if reader.is_encrypted and not reader.decrypt(""):
            raise ValueError("Password-protected PDFs are not supported.")
        if len(reader.pages) > MAX_PDF_PAGES:
            raise ValueError(
                f"PDFs may contain no more than {MAX_PDF_PAGES} pages."
            )

        documents = []
        extracted_characters = 0
        safe_filename = Path(filename).name or "document.pdf"
        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            extracted_characters += len(text)
            if extracted_characters > MAX_EXTRACTED_CHARACTERS:
                raise ValueError("The extracted PDF text is too large to process.")
            if text.strip():
                documents.append(
                    Document(
                        page_content=text,
                        metadata={"source": safe_filename, "page": page_number},
                    )
                )
    except ValueError:
        raise
    except Exception as exc:
        raise ValueError("The PDF could not be read. Try a different PDF file.") from exc

    if not documents:
        raise ValueError(
            "No selectable text was found. Scanned PDFs need OCR before upload."
        )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    return splitter.split_documents(documents)


def load_and_split_pdf(pdf_path: str | Path | None = None):
    """Load a local PDF; the bundled sample is an optional CLI default only."""
    path = Path(pdf_path) if pdf_path else DEFAULT_PDF_PATH
    try:
        return load_and_split_pdf_bytes(path.read_bytes(), path.name)
    except OSError as exc:
        raise FileNotFoundError(f"Could not read PDF at {path}") from exc
