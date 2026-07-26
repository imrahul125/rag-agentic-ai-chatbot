from app.services.ingest import load_and_split_pdf
from app.services.embeddings import get_embedding_model
from langchain_chroma import Chroma

DB_PATH = "chroma_db"

chunks = load_and_split_pdf("data/Ebook-Agentic-AI.pdf")

embedding_model = get_embedding_model()

db = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    persist_directory=DB_PATH
)

print(f"Stored {len(chunks)} chunks.")