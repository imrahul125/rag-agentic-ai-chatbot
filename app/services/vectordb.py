from langchain_chroma import Chroma

from app.config import PROJECT_ROOT
from app.services.embeddings import get_embedding_model


DB_PATH = PROJECT_ROOT / "chroma_db"
COLLECTION_NAME = "agentic_ai_ebook"


def get_vector_db(collection_name: str = COLLECTION_NAME):
    """Open the optional, locally built sample index."""
    return Chroma(
        collection_name=collection_name,
        persist_directory=str(DB_PATH),
        embedding_function=get_embedding_model(),
    )
