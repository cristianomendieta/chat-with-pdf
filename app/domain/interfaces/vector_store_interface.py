from abc import ABC, abstractmethod
from typing import Any, Dict, List


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
    async def search_similar(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar documents.

        Args:
            query: The search query
            k: Number of documents to return

        Returns:
            List of similar documents
        """
        pass
