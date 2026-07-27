from fastapi import APIRouter
from pydantic import BaseModel
from app.api.models import ChatResponse
from app.graph.workflow import graph

router = APIRouter(
    tags=["Chat"]
)


class ChatRequest(BaseModel):
    question: str


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    result = graph.invoke(
        {
            "question": request.question
        }
    )

    return {
        "answer": result["answer"],
        "confidence": result["confidence"],
        "sources": result["sources"]
    }