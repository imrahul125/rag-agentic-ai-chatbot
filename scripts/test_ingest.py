import argparse

from app.services.ingest import DEFAULT_PDF_PATH, load_and_split_pdf


def main():
    parser = argparse.ArgumentParser(description="Inspect PDF text chunking.")
    parser.add_argument("--pdf", type=str, default=str(DEFAULT_PDF_PATH))
    args = parser.parse_args()

    chunks = load_and_split_pdf(args.pdf)
    print(f"Total chunks: {len(chunks)}")
    if chunks:
        print()
        print(chunks[0].page_content[:500])


if __name__ == "__main__":
    main()
