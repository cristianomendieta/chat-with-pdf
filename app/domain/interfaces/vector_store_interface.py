"""Abstract interface for vector storage operations."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class VectorStoreInterface(ABC):
    """Abstract interface for vector storage and retrieval operations."""

    @abstractmethod
    async def store_documents(
        self, documents: List[Dict[str, Any]], file_name: str
    ) -> None:
        """
        Store documents in the vector database.

        Args:
            documents: List of documents with content and metadata
            file_name: Name of the original file for metadata tracking
        """
        pass

    @abstractmethod
    async def search_similar(
        self,
        query: str,
        k: int = 5,
        strategy: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search for similar documents using the specified strategy.

        Args:
            query: The search query text
            k: Number of documents to return
            strategy: Search strategy ('dense', 'sparse', 'hybrid')
            filters: Optional filters to apply to the search

        Returns:
            List of similar documents with relevance scores
        """
        pass

    @abstractmethod
    def set_search_strategy(self, strategy_name: str, **kwargs) -> None:
        """
        Configure the search strategy to use.

        Args:
            strategy_name: Name of the strategy to use
            **kwargs: Additional configuration parameters
        """
        pass

    @abstractmethod
    def get_available_strategies(self) -> List[str]:
        """
        Get list of available search strategies.

        Returns:
            List of available strategy names
        """
        pass
