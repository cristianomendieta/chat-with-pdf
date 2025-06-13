from fastapi import APIRouter, UploadFile, File, Depends
from pydantic import BaseModel
from typing import List

from app.controllers import DocumentController, QuestionController
from kink import di

api = APIRouter()

class DocumentUploadResponse(BaseModel):
    message: str
    documents_indexed: int
    total_chunks: int

class QuestionRequest(BaseModel):
    question: str

class QuestionResponse(BaseModel):
    answer: str
    references: List[str] = []


@api.post("/documents", response_model=DocumentUploadResponse)
async def upload_documents(
    files: List[UploadFile] = File(...),
    controller: DocumentController = Depends(lambda: di[DocumentController])
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
        total_chunks=result.total_chunks
    )

@api.post("/question", response_model=QuestionResponse)
async def ask_question(
    request: QuestionRequest,
    controller: QuestionController = Depends(lambda: di[QuestionController])
):
    """
    Ask a question about the uploaded PDF documents.
    
    Args:
        request: Question request containing the user's question
        controller: Injected question controller
        
    Returns:
        QuestionResponse with answer and source references
    """
    result = await controller.ask_question(request)
    
    return QuestionResponse(
        answer=result.answer,
        references=result.references
    )