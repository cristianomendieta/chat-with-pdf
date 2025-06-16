"""Domain models for search operations and strategies."""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class SearchStrategyType(str, Enum):
    """Available search strategy types for document retrieval."""

    DENSE = "dense"
    SPARSE = "sparse"
    HYBRID = "hybrid"


class SearchScore(BaseModel):
    """Relevance scores from different search strategies."""

    dense_score: Optional[float] = None
    sparse_score: Optional[float] = None
    combined_score: Optional[float] = None
    rerank_score: Optional[float] = None

    @property
    def is_hybrid(self) -> bool:
        """Check if this result came from hybrid search."""
        return self.dense_score is not None and self.sparse_score is not None


class RerankedSearchScore(BaseModel):
    score: float


class SearchQuery(BaseModel):
    text: str = Field(min_length=1, max_length=1000)
    max_results: int = Field(default=5, ge=1, le=20)
    strategy: SearchStrategyType = Field(default=SearchStrategyType.HYBRID)
    filters: Optional[dict] = None

    class Config:
        use_enum_values = True
