from typing import Any, Dict, List, Optional

from app.domain.entities.search_entities import DocumentChunk
from app.domain.interfaces.vector_store_interface import VectorStoreInterface
from app.domain.models.search import SearchQuery, SearchStrategyType
from app.environment import get_env
from app.infra.repositories.pinecone_search_repository import PineconeSearchRepository

env = get_env()


class PineconeClient(VectorStoreInterface):
    def __init__(
        self,
        environment: str = "us-east-1",
    ):
        """
        Initialize Pinecone client.

        Args:
            environment: Pinecone environment/region (defaults to 'us-east-1' if not provided)
        """
        self.repository = PineconeSearchRepository(
            api_key=env.PINECONE_API_KEY,
            dense_index_name=env.PINECONE_DENSE_INDEX_NAME,
            sparse_index_name=env.PINECONE_SPARSE_INDEX_NAME,
            environment=environment,
        )

        self.current_strategy = SearchStrategyType.HYBRID

    async def store_documents(
        self, documents: List[Dict[str, Any]], file_name: str
    ) -> None:
        """
        Store documents in the vector store.

        Args:
            documents: List of document dictionaries with 'content' and metadata
            file_name: Name of the source file
        """
        # Convert dict format to DocumentChunk entities
        doc_chunks = []
        for i, doc in enumerate(documents):
            chunk = DocumentChunk(
                id=f"{file_name}_{i}",
                content=doc.page_content,
                metadata=doc.metadata or {},
                file_name=file_name,
                chunk_index=i,
            )
            doc_chunks.append(chunk)

        # Store using the repository
        await self.repository.store_documents(doc_chunks)

    async def search_similar(
        self,
        query: str,
        k: int = 5,
        strategy: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search for similar documents.

        Args:
            query: The search query
            k: Number of documents to return
            strategy: Search strategy to use ('dense', 'sparse', 'hybrid')
            filters: Optional filters to apply

        Returns:
            List of search results in dictionary format
        """
        # Determine strategy to use
        if strategy:
            try:
                search_strategy = SearchStrategyType(strategy)
            except ValueError:
                search_strategy = self.current_strategy
        else:
            search_strategy = self.current_strategy

        # Create search query
        search_query = SearchQuery(
            text=query, max_results=k, strategy=search_strategy, filters=filters
        )

        # Perform search
        results = await self.repository.search(search_query)

        return results

    def set_search_strategy(self, strategy_name: str, **kwargs) -> None:
        """
        Set the current search strategy.

        Args:
            strategy_name: Name of the strategy ('dense', 'sparse', 'hybrid')
            **kwargs: Additional arguments (ignored for now)
        """
        try:
            self.current_strategy = SearchStrategyType(strategy_name)
        except ValueError:
            raise ValueError(
                f"Unknown strategy: {strategy_name}. "
                f"Available: {self.get_available_strategies()}"
            )

    def get_available_strategies(self) -> List[str]:
        """
        Get list of available search strategies.

        Returns:
            List of strategy names
        """
        return [strategy.value for strategy in SearchStrategyType]

    async def get_index_stats(self) -> Dict[str, Any]:
        """Get statistics about the search indexes."""
        return await self.repository.get_index_stats()
