import argparse
from pathlib import Path

from app.graph.workflow import graph
from app.services.documents import document_store
from app.services.ingest import DEFAULT_PDF_PATH


def main():
    parser = argparse.ArgumentParser(description="Ask a question about a local PDF.")
    parser.add_argument("--pdf", type=Path, default=DEFAULT_PDF_PATH)
    parser.add_argument("--question", default="What is Agentic AI?")
    args = parser.parse_args()

    record = document_store.add_pdf(args.pdf.read_bytes(), args.pdf.name)
    try:
        result = graph.invoke(
            {"question": args.question, "vector_db": record.vector_db}
        )
        print(result["answer"])
        for source in result["sources"]:
            print(f"\nPage {source['page']} ({source['relevance']:.0%} match)")
            print(source["text"])
    finally:
        document_store.delete(record.document_id)


if __name__ == "__main__":
    main()
