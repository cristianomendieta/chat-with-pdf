from typing import List, Optional

from pydantic import BaseModel


class QuestionRequest(BaseModel):
    """
    Request model for asking questions.
    """

    question: str
    search_strategy: Optional[str] = "hybrid"  # dense, sparse, or hybrid
    max_documents: Optional[int] = 5

    class Config:
        from_attributes = True


class QuestionResult(BaseModel):
    """
    Result of question processing operation.
    """

    answer: str
    references: List[str] = []

    class Config:
        from_attributes = True
