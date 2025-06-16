"""Abstract interfaces for search repository operations."""

from abc import ABC, abstractmethod
from typing import List

from app.domain.entities.search_entities import DocumentChunk, SearchResult
from app.domain.models.search import SearchQuery


class SearchRepository(ABC):
    """Abstract interface for document search and storage operations."""

    @abstractmethod
    async def store_documents(self, documents: List[DocumentChunk]) -> None:
        """
        Store document chunks in the search index.

        Args:
            documents: List of document chunks to store
        """
        pass

    @abstractmethod
    async def search(self, query: SearchQuery) -> List[SearchResult]:
        """
        Search for documents matching the query criteria.

        Args:
            query: Search query with parameters and strategy

        Returns:
            List of search results ordered by relevance
        """
        pass


class HybridSearchService(ABC):
    """Abstract interface for hybrid search capabilities combining multiple strategies."""

    @abstractmethod
    async def hybrid_search(self, query: SearchQuery) -> List[SearchResult]:
        """
        Perform hybrid search combining dense and sparse vector strategies.

        Args:
            query: Search query parameters

        Returns:
            Combined and reranked search results
        """
        pass

    @abstractmethod
    def get_supported_strategies(self) -> List[str]:
        """Get list of supported search strategies."""
        pass
