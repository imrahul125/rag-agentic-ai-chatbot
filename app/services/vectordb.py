from langchain_chroma import Chroma
from app.services.embeddings import get_embedding_model

DB_PATH = "chroma_db"

embedding_model = get_embedding_model()


def get_vector_db():
    return Chroma(
        persist_directory=DB_PATH,
        embedding_function=embedding_model
    )