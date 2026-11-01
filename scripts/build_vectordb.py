import hashlib

from langchain_chroma import Chroma

from app.config import PROJECT_ROOT
from app.services.embeddings import get_embedding_model
from app.services.ingest import load_and_split_pdf
from app.services.vectordb import COLLECTION_NAME, DB_PATH


def main():
    sample_pdf = PROJECT_ROOT / "data" / "Ebook-Agentic-AI.pdf"
    chunks = load_and_split_pdf(sample_pdf)
    stable_ids = [
        hashlib.sha256(
            f"{chunk.metadata.get('page')}:{index}:{chunk.page_content}".encode("utf-8")
        ).hexdigest()
        for index, chunk in enumerate(chunks)
    ]
    Chroma.from_documents(
        documents=chunks,
        embedding=get_embedding_model(),
        ids=stable_ids,
        collection_name=COLLECTION_NAME,
        persist_directory=str(DB_PATH),
    )
    print(f"Indexed {len(chunks)} chunks from {sample_pdf.name}.")


if __name__ == "__main__":
    main()
