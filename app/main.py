from fastapi import FastAPI

from app.api.routes import router


app = FastAPI(
    title="Document Chat API",
    description="Upload a PDF, then ask questions grounded in its text.",
    version="2.0.0",
)
app.include_router(router)


@app.get("/", tags=["Health"])
def home():
    return {
        "status": "ok",
        "application": "Document Chat",
        "version": "2.0.0",
        "docs": "/docs",
    }
