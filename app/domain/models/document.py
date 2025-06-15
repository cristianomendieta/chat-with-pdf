from pydantic import BaseModel


class DocumentProcessResult(BaseModel):
    """
    Result of document processing operation.
    """

    message: str = "Documents processed successfully"
    documents_indexed: int
    total_chunks: int = 0

    class Config:
        # Allow creating instances from dictionaries
        from_attributes = True
