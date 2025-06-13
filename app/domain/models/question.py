from pydantic import BaseModel
from typing import List


class QuestionRequest(BaseModel):
    """
    Request model for asking questions.
    """
    question: str
    
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
