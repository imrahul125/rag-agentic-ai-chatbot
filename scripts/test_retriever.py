import argparse
from pathlib import Path
from uuid import uuid4

from langchain_chroma import Chroma

from app.services.embeddings import get_embedding_model
from app.services.ingest import DEFAULT_PDF_PATH, load_and_split_pdf
from app.services.retriever import document_retriever


def main():
    parser = argparse.ArgumentParser(description="Inspect PDF retrieval results.")
    parser.add_argument("--pdf", type=Path, default=DEFAULT_PDF_PATH)
    parser.add_argument("--question", default="What is Agentic AI?")
    args = parser.parse_args()

    chunks = load_and_split_pdf(args.pdf)
    vector_db = Chroma.from_documents(
        chunks,
        embedding=get_embedding_model(),
        collection_name=f"smoke_{uuid4().hex}",
        collection_metadata={"hnsw:space": "cosine"},
    )
    for index, (document, relevance) in enumerate(
        document_retriever.retrieve(vector_db, args.question),
        start=1,
    ):
        page = document.metadata.get("page", "unknown")
        print(f"{index}. Page {page} · {relevance:.0%} match")
        print(document.page_content[:500])


if __name__ == "__main__":
    main()
