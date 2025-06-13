from pydantic import BaseModel


class DocumentProcessResult(BaseModel):
    """
    Result of document processing operation.
    """
    message: str
    documents_indexed: int
    total_chunks: int
    
    class Config:
        # Allow creating instances from dictionaries
        from_attributes = True
