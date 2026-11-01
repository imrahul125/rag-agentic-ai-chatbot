from app.config import MIN_RELEVANCE_SCORE


class DocumentRetriever:
    def __init__(self, top_k: int = 8, minimum_relevance: float = MIN_RELEVANCE_SCORE):
        self.top_k = top_k
        self.minimum_relevance = minimum_relevance

    def retrieve(self, vector_db, question: str):
        """Return cosine-ranked passages above a low recall-oriented floor."""
        if not question or not question.strip():
            return []

        # The collections created by DocumentStore use Chroma's cosine metric.
        # Its raw score is cosine distance, so 1 - distance is cosine similarity.
        matches = vector_db.similarity_search_with_score(
            question.strip(),
            k=self.top_k,
        )
        relevant = []
        for document, distance in matches:
            if distance is None:
                continue
            similarity = 1.0 - float(distance)
            if similarity < self.minimum_relevance:
                continue
            relevant.append((document, max(0.0, min(similarity, 1.0))))
        return relevant


document_retriever = DocumentRetriever()
