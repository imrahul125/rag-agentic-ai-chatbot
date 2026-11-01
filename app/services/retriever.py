from app.config import MIN_RELEVANCE_SCORE


class DocumentRetriever:
    def __init__(self, top_k: int = 4, minimum_relevance: float = MIN_RELEVANCE_SCORE):
        self.top_k = top_k
        self.minimum_relevance = minimum_relevance

    def retrieve(self, vector_db, question: str):
        """Return only retrieved passages that clear the relevance floor."""
        if not question or not question.strip():
            return []

        matches = vector_db.similarity_search_with_relevance_scores(
            question.strip(),
            k=self.top_k,
        )
        relevant = []
        for document, score in matches:
            if score is None or score < self.minimum_relevance:
                continue
            relevant.append((document, max(0.0, min(float(score), 1.0))))
        return relevant


document_retriever = DocumentRetriever()
