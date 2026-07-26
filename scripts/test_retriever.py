from app.services.vectordb import get_vector_db

db = get_vector_db()

query = "What is Agentic AI?"

results = db.similarity_search_with_score(query, k=3)

for i, (doc, score) in enumerate(results, 1):
    print("=" * 80)
    print(f"Result {i}")
    print(f"Score: {score:.4f}")
    print(doc.page_content[:500])