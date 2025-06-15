from typing import List, Optional

from fastapi import APIRouter, Depends, File, UploadFile
from kink import di
from pydantic import BaseModel

from app.controllers import DocumentController, QuestionController
from app.domain.models.question import QuestionRequest

api = APIRouter()


class DocumentUploadResponse(BaseModel):
    message: str
    documents_indexed: int
    total_chunks: int


class QuestionResponse(BaseModel):
    answer: str
    references: List[str] = []
    search_strategy: Optional[str] = None
    documents_found: Optional[int] = 0
    context_used: Optional[int] = 0


@api.post("/documents", response_model=DocumentUploadResponse)
async def upload_documents(
    files: List[UploadFile] = File(...),
    controller: DocumentController = Depends(lambda: di[DocumentController]),
):
    """
    Upload one or more PDF documents to be indexed.

    Args:
        files: List of PDF files to be processed and indexed
        controller: Injected document controller

    Returns:
        DocumentUploadResponse with processing statistics
    """
    result = await controller.upload_documents(files)

    return DocumentUploadResponse(
        message=result.message,
        documents_indexed=result.documents_indexed,
        total_chunks=result.total_chunks,
    )


@api.post("/question", response_model=QuestionResponse)
async def ask_question(
    request: QuestionRequest,
    controller: QuestionController = Depends(lambda: di[QuestionController]),
):
    """
    Ask a question about the uploaded PDF documents.

    Args:
        request: Question request containing the user's question and search preferences
        controller: Injected question controller

    Returns:
        QuestionResponse with answer and source references
    """
    result = await controller.ask_question(request)

    return QuestionResponse(
        answer=result.answer,
        references=result.references,
        search_strategy=result.search_strategy,
        documents_found=result.documents_found,
        context_used=result.context_used,
    )


@api.get("/question/status")
async def get_question_service_status(
    controller: QuestionController = Depends(lambda: di[QuestionController]),
):
    """
    Get the current status of the question answering service.

    Args:
        controller: Injected question controller

    Returns:
        Service status information including available search strategies
    """
    return await controller.get_question_service_status()
