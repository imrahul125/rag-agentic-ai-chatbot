from app.services.embeddings import get_embedding_model


def main():
    embedding_model = get_embedding_model()
    vector = embedding_model.embed_query("What is in this document?")
    print(f"Vector dimension: {len(vector)}")
    print(vector[:10])


if __name__ == "__main__":
    main()
