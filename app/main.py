from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(
    title="Agentic AI RAG Chatbot",
    version="1.0"
)

app.include_router(router)


@app.get("/")
def home():
    return {
        "message": "Agentic AI RAG Chatbot is running!"
    }