from fastapi import APIRouter, File, HTTPException, UploadFile
from openai import APIError
from starlette.concurrency import run_in_threadpool

from app.api.models import ChatRequest, ChatResponse, Source, UploadResponse
from app.config import MAX_PDF_UPLOAD_BYTES
from app.graph.workflow import graph
from app.services.documents import document_store


router = APIRouter(tags=["Documents"])


@router.post(
    "/documents",
    response_model=UploadResponse,
    status_code=201,
    summary="Upload and index a PDF",
)
async def upload_document(file: UploadFile = File(...)):
    contents = await file.read(MAX_PDF_UPLOAD_BYTES + 1)
    await file.close()
    if len(contents) > MAX_PDF_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="PDF files must be 25 MB or smaller.")

    try:
        record = await run_in_threadpool(
            document_store.add_pdf,
            contents,
            file.filename or "document.pdf",
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail="The PDF could not be indexed. Please try again.",
        ) from exc

    return UploadResponse(
        document_id=record.document_id,
        filename=record.filename,
        pages_indexed=record.page_count,
        chunks_indexed=record.chunk_count,
        size_bytes=record.size_bytes,
    )


@router.post("/chat", response_model=ChatResponse, summary="Ask about an uploaded PDF")
def chat(request: ChatRequest):
    record = document_store.get(request.document_id)
    if record is None:
        raise HTTPException(
            status_code=404,
            detail="That PDF session has expired. Upload the PDF again.",
        )
    try:
        result = graph.invoke(
            {
                "question": request.question,
                "vector_db": record.vector_db,
            }
        )
    except ValueError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except APIError as exc:
        raise HTTPException(
            status_code=502,
            detail="The language model request failed. Please try again.",
        ) from exc
    return ChatResponse(
        answer=result["answer"],
        sources=[Source(**source) for source in result["sources"]],
    )


@router.delete("/documents/{document_id}", status_code=204, summary="Delete a PDF session")
def delete_document(document_id: str):
    if not document_store.delete(document_id):
        raise HTTPException(status_code=404, detail="PDF session not found.")
    return None
