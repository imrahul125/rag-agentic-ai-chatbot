from app.services.ingest import load_and_split_pdf

chunks = load_and_split_pdf()

print(f"Total Chunks : {len(chunks)}")

print()

print(chunks[0].page_content[:500])