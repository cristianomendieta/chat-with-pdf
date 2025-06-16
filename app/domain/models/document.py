"""Domain models for document processing operations."""

from pydantic import BaseModel


class DocumentProcessResult(BaseModel):
    """Result model containing document processing statistics."""

    message: str = "Documents processed successfully"
    documents_indexed: int
    total_chunks: int = 0

    class Config:
        from_attributes = True
