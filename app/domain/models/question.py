"""Domain models for question handling operations."""

from typing import List, Optional

from pydantic import BaseModel


class QuestionRequest(BaseModel):
    """Request model for asking questions about documents."""

    question: str
    search_strategy: Optional[str] = "hybrid"  # dense, sparse, or hybrid
    max_documents: Optional[int] = 5

    class Config:
        from_attributes = True


class QuestionResult(BaseModel):
    """Result model containing answer and metadata from question processing."""

    answer: str
    references: List[str] = []

    class Config:
        from_attributes = True
