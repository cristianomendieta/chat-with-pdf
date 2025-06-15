from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class SearchStrategyType(str, Enum):
    """Enumeration of available search strategy types."""

    DENSE = "dense"
    SPARSE = "sparse"
    HYBRID = "hybrid"


class SearchScore(BaseModel):
    """Value object representing search relevance scores."""

    dense_score: Optional[float] = None
    sparse_score: Optional[float] = None
    combined_score: Optional[float] = None
    rerank_score: Optional[float] = None

    @property
    def is_hybrid(self) -> bool:
        """Check if this result came from hybrid search."""
        return self.dense_score > 0 and self.sparse_score > 0


class RerankedSearchScore(BaseModel):
    score: float


class SearchQuery(BaseModel):
    """Value object representing a search query."""

    text: str = Field(min_length=1, max_length=1000)
    max_results: int = Field(default=5, ge=1, le=20)
    strategy: SearchStrategyType = Field(default=SearchStrategyType.HYBRID)
    filters: Optional[dict] = None

    class Config:
        use_enum_values = True
