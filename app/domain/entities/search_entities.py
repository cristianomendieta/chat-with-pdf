"""Domain entities for search operations."""

from typing import Any, Dict, Optional, Union

from pydantic import BaseModel, Field

from app.domain.models.search import (
    RerankedSearchScore,
    SearchScore,
    SearchStrategyType,
)


class DocumentChunk(BaseModel):
    """Entity representing a chunk of document content."""

    id: str = Field(description="Unique identifier for the chunk")
    content: str = Field(description="Text content of the chunk")
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )
    file_name: Optional[str] = Field(default=None, description="Original file name")

    def __str__(self) -> str:
        return f"DocumentChunk(id={self.id}, content_length={len(self.content)})"


class SearchResult(BaseModel):
    """Entity representing a search result with document and relevance information."""

    document: DocumentChunk
    score: Union[SearchScore, RerankedSearchScore]
    strategy_used: SearchStrategyType

    class Config:
        use_enum_values = True

    @property
    def relevance_score(self) -> float:
        """Get the primary relevance score for ranking purposes."""
        if (
            hasattr(self.score, "combined_score")
            and self.score.combined_score is not None
        ):
            return self.score.combined_score
        elif hasattr(self.score, "score"):
            return self.score.score
        return 0.0

    def __str__(self) -> str:
        return f"SearchResult(doc={self.document.id}, score={self.relevance_score:.3f}, strategy={self.strategy_used})"
