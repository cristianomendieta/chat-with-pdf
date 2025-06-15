from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class VectorStoreInterface(ABC):
    """Abstract interface for vector store operations."""

    @abstractmethod
    async def store_documents(
        self, documents: List[Dict[str, Any]], file_name: str
    ) -> None:
        """
        Store documents in the vector database.

        Args:
            documents: List of documents to store (with content and metadata)
            file_name: Name of the original file for metadata
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
        Search for similar documents using specified strategy.

        Args:
            query: The search query
            k: Number of documents to return
            strategy: Search strategy to use ('dense', 'sparse', 'hybrid')
            filters: Optional filters to apply to the search

        Returns:
            List of similar documents
        """
        pass

    @abstractmethod
    def set_search_strategy(self, strategy_name: str, **kwargs) -> None:
        """
        Set the search strategy to use.

        Args:
            strategy_name: Name of the strategy to use
            **kwargs: Additional configuration for the strategy
        """
        pass

    @abstractmethod
    def get_available_strategies(self) -> List[str]:
        """
        Get list of available search strategies.

        Returns:
            List of strategy names
        """
        pass
