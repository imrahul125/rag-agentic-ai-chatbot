from typing import Any, TypedDict

from langgraph.graph import END, StateGraph

from app.services.rag import rag


class GraphState(TypedDict, total=False):
    question: str
    vector_db: Any
    answer: str
    sources: list


def retrieve_and_answer(state: GraphState):
    return rag.ask(state["vector_db"], state["question"])


builder = StateGraph(GraphState)
builder.add_node("rag", retrieve_and_answer)
builder.set_entry_point("rag")
builder.add_edge("rag", END)
graph = builder.compile()
