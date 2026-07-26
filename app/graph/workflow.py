from typing import TypedDict

from langgraph.graph import StateGraph, END

from app.services.rag import rag


class GraphState(TypedDict):
    question: str
    answer: str
    confidence: float
    sources: list


def retrieve_and_answer(state: GraphState):
    result = rag.ask(state["question"])

    return {
        "answer": result["answer"],
        "confidence": result["confidence"],
        "sources": result["sources"],
    }


builder = StateGraph(GraphState)

builder.add_node("rag", retrieve_and_answer)

builder.set_entry_point("rag")

builder.add_edge("rag", END)

graph = builder.compile()