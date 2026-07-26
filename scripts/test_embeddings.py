from app.services.embeddings import get_embedding_model

embedding_model = get_embedding_model()

vector = embedding_model.embed_query("What is Agentic AI?")

print(f"Vector Dimension: {len(vector)}")
print(vector[:10])  # Print the first 10 values