from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(
    title="Agentic AI RAG Chatbot",
    description="RAG chatbot built with LangGraph, ChromaDB and OpenRouter. Answers are grounded strictly on the Agentic AI eBook.",
    version="1.0.0"
)

app.include_router(router)

@app.get("/")
def home():
    return {
    "status": "healthy",
    "application": "Agentic AI RAG Chatbot",
    "version": "1.0.0",
    "docs": "/docs"
}