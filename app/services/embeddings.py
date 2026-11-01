from functools import lru_cache

from langchain_huggingface import HuggingFaceEmbeddings

from app.config import EMBEDDING_MODEL


@lru_cache(maxsize=1)
def get_embedding_model() -> HuggingFaceEmbeddings:
    """Load one CPU embedding model per app process."""
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
