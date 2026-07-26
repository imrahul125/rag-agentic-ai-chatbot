from app.services.vectordb import get_vector_db
from app.services.llm import llm


class RAGService:
    def __init__(self):
        self.db = get_vector_db()

    def ask(self, question: str):
        results = self.db.similarity_search_with_score(
            question,
            k=3
        )

        context = "\n\n".join(
            [doc.page_content for doc, _ in results]
        )

        prompt = f"""
You are an expert AI assistant.

Use ONLY the information provided in the context below.

Rules:
- Do not use outside knowledge.
- If the answer is not present in the context, reply exactly:
  "I could not find the answer in the provided document."
- Answer in 3-6 complete sentences.
- Be clear and professional.
- Do not mention that you are using context.

Context:
{context}

Question:
{question}

Answer:
"""

        answer = llm.generate(prompt)

        confidence = round(
            max(
                0,
                1 - results[0][1]
            ),
            2,
        )

        return {
            "answer": answer,
            "confidence": confidence,
            "sources": [
                {
                    "score": round(1 - score, 2),
                    "text": doc.page_content
                }
                for doc, score in results
            ],
        }


rag = RAGService()