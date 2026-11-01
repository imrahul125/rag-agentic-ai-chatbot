import os
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")

OPENROUTER_BASE_URL = os.getenv(
    "OPENROUTER_BASE_URL",
    "https://openrouter.ai/api/v1",
)
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openrouter/auto")
EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2",
)
MAX_PDF_UPLOAD_BYTES = 25 * 1024 * 1024
MAX_PDF_PAGES = 500
MAX_EXTRACTED_CHARACTERS = 10_000_000
MIN_RELEVANCE_SCORE = 0.05
DOCUMENT_TTL_SECONDS = 60 * 60
MAX_ACTIVE_DOCUMENTS = 10


def get_openrouter_api_key() -> str | None:
    """Read the API key without requiring it during application startup."""
    value = os.getenv("OPENROUTER_API_KEY", "").strip()
    return value or None
