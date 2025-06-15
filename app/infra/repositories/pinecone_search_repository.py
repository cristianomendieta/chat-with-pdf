import hashlib
from collections import Counter
from typing import Any, Dict, List

from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone, ServerlessSpec
from transformers import BertTokenizerFast

from app.domain.entities.search_entities import DocumentChunk, SearchResult
from app.domain.interfaces.search_repository_interface import (
    HybridSearchService,
    SearchRepository,
)
from app.domain.models.search import (
    RerankedSearchScore,
    SearchQuery,
    SearchScore,
    SearchStrategyType,
)
from app.infra.encoders import BertTextEncoder, OpenAITextEncoder

SCORE_THRESHOLD = 0.7


class PineconeSearchRepository(SearchRepository, HybridSearchService):
    """Pinecone implementation of search repository with hybrid search capabilities."""

    def __init__(
        self,
        api_key: str,
        dense_index_name: str = "dense-chat-with-pdf",
        sparse_index_name: str = "sparse-chat-with-pdf",
        environment: str = "us-east-1",
    ):
        """
        Initialize Pinecone search repository.

        Args:
            api_key: Pinecone API key
            dense_index_name: Name of the dense vector index
            sparse_index_name: Name of the sparse vector index
            environment: Pinecone environment
        """
        self.pc = Pinecone(api_key=api_key)
        self.dense_index_name = dense_index_name
        self.sparse_index_name = sparse_index_name
        self.environment = environment

        # Ensure indexes exist
        self._ensure_indexes_exist()

        # Initialize indexes
        self.dense_index = self.pc.Index(dense_index_name)
        self.sparse_index = self.pc.Index(sparse_index_name)

        # Initialize encoders
        self.dense_encoder = OpenAITextEncoder()
        self.sparse_encoder = BertTextEncoder()

        # For query encoding
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.tokenizer = BertTokenizerFast.from_pretrained(
            "bert-base-multilingual-uncased"
        )

    def _ensure_indexes_exist(self) -> None:
        """Ensure both indexes exist."""
        if not self.pc.has_index(self.dense_index_name):
            self.pc.create_index(
                name=self.dense_index_name,
                dimension=1536,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region=self.environment),
            )

        if not self.pc.has_index(self.sparse_index_name):
            self.pc.create_index(
                name=self.sparse_index_name,
                metric="dotproduct",
                spec=ServerlessSpec(cloud="aws", region=self.environment),
            )

    async def store_documents(self, documents: List[DocumentChunk]) -> None:
        """Store document chunks in both dense and sparse indexes."""
        if not documents:
            return

        # Extract text content
        texts = [doc.content for doc in documents]

        # Encode using both strategies
        dense_encoded = await self.dense_encoder.encode_texts(texts)
        sparse_encoded = await self.sparse_encoder.encode_texts(texts)

        # Prepare vectors for upload
        dense_vectors = []
        sparse_vectors = []

        for doc, dense_vec, sparse_vec in zip(documents, dense_encoded, sparse_encoded):
            doc_id = self._generate_document_id(doc)

            metadata = {
                "chunk_text": doc.content,
                "file_name": doc.file_name or "",
                "chunk_index": doc.chunk_index,
                **doc.metadata,
            }

            dense_vectors.append(
                {"id": doc_id, "values": dense_vec["vector"], "metadata": metadata}
            )

            sparse_vectors.append(
                {
                    "id": doc_id,
                    "sparse_values": sparse_vec["vector"],
                    "metadata": metadata,
                }
            )

        # Upload in batches
        await self._upload_vectors_batch(dense_vectors, self.dense_index)
        await self._upload_vectors_batch(sparse_vectors, self.sparse_index)

    def _generate_document_id(self, doc: DocumentChunk) -> str:
        """Generate a unique ID for a document chunk."""
        if doc.id:
            return doc.id

        # Generate ID from content hash
        content_hash = hashlib.md5(doc.content.encode()).hexdigest()
        return content_hash

    async def _upload_vectors_batch(
        self,
        vectors: List[Dict[str, Any]],
        index,
        batch_size: int = 100,
    ) -> None:
        """Upload vectors in batches."""
        for i in range(0, len(vectors), batch_size):
            batch = vectors[i : i + batch_size]
            index.upsert(vectors=batch)

    async def search(self, query: SearchQuery) -> List[SearchResult]:
        """Search using the specified strategy."""
        if query.strategy == SearchStrategyType.DENSE:
            return await self._dense_search(query)
        elif query.strategy == SearchStrategyType.SPARSE:
            return await self._sparse_search(query)
        elif query.strategy == SearchStrategyType.HYBRID:
            return await self.hybrid_search(query)
        else:
            raise ValueError(f"Unsupported search strategy: {query.strategy}")

    async def _dense_search(self, query: SearchQuery) -> List[SearchResult]:
        """Perform dense vector search."""
        # Generate query embedding
        query_vector = self.embeddings.embed_query(query.text)

        # Search
        results = self.dense_index.query(
            vector=query_vector,
            top_k=query.max_results,
            include_metadata=True,
            filter=query.filters,
        )

        # Convert to domain entities
        search_results = []
        for match in results["matches"]:
            doc_chunk = DocumentChunk(
                id=match["id"],
                content=match["metadata"].get("chunk_text", ""),
                metadata=match["metadata"],
                file_name=match["metadata"].get("file_name"),
                chunk_index=match["metadata"].get("chunk_index"),
            )

            score = SearchScore(dense_score=match["score"])

            search_results.append(
                SearchResult(
                    document=doc_chunk,
                    score=score,
                    strategy_used=SearchStrategyType.DENSE,
                )
            )

        return search_results

    async def _sparse_search(self, query: SearchQuery) -> List[SearchResult]:
        """Perform sparse vector search."""
        # Generate sparse query vector
        sparse_vector = self._generate_sparse_query_vector(query.text)

        # Search
        results = self.sparse_index.query(
            sparse_vector=sparse_vector,
            top_k=query.max_results,
            include_metadata=True,
            filter=query.filters,
        )

        # Convert to domain entities
        search_results = []
        for match in results["matches"]:
            doc_chunk = DocumentChunk(
                id=match["id"],
                content=match["metadata"].get("chunk_text", ""),
                metadata=match["metadata"],
                file_name=match["metadata"].get("file_name"),
                chunk_index=match["metadata"].get("chunk_index"),
            )

            score = SearchScore(sparse_score=match["score"])

            search_results.append(
                SearchResult(
                    document=doc_chunk,
                    score=score,
                    strategy_used=SearchStrategyType.SPARSE,
                )
            )

        return search_results

    def _generate_sparse_query_vector(self, query: str) -> Dict[str, List]:
        """Generate sparse vector for query."""
        inputs = self.tokenizer([query], padding=True, truncation=True, max_length=512)[
            "input_ids"
        ][0]

        # Convert to frequency dictionary
        token_freq = dict(Counter(inputs))

        # Filter special tokens
        indices = []
        values = []
        for idx, freq in token_freq.items():
            if idx not in [101, 102, 103, 0]:
                indices.append(idx)
                values.append(float(freq))

        return {"indices": indices, "values": values}

    async def hybrid_search(
        self, query: SearchQuery, apply_reranking: bool = True, top_k: int = 5
    ) -> List[SearchResult]:
        """
        Perform hybrid search combining dense and sparse results.

        This implements the same logic as the notebook:
        1. Perform both searches
        2. Merge and deduplicate by document ID
        3. Sort by original scores
        4. Optionally apply reranking with CrossEncoder
        4. Return top k results
        """
        # Create separate queries for each strategy
        dense_query = SearchQuery(
            text=query.text,
            max_results=query.max_results,
            strategy=SearchStrategyType.DENSE,
            filters=query.filters,
        )

        sparse_query = SearchQuery(
            text=query.text,
            max_results=query.max_results,
            strategy=SearchStrategyType.SPARSE,
            filters=query.filters,
        )

        # Perform both searches
        dense_results = await self._dense_search(dense_query)
        sparse_results = await self._sparse_search(sparse_query)

        # Merge results (same logic as notebook)
        merged_results = self._merge_hybrid_results(dense_results, sparse_results)

        # # Sort by combined score
        # sorted_results = sorted(
        #     merged_results, key=lambda x: x.score.combined_score, reverse=True
        # )

        # Apply reranking if requested
        if apply_reranking:
            sorted_results = self.rerank_results(query.text, merged_results, top_k)

        return sorted_results[: query.max_results]

    def _merge_hybrid_results(
        self,
        dense_results: List[SearchResult],
        sparse_results: List[SearchResult],
    ) -> List[SearchResult]:
        """Merge dense and sparse results by deduplicating and sorting by original score."""
        results_dict = {}

        # Add all results to dict, deduplicating by document ID
        # Keep the result with the highest score for each document
        for result in dense_results + sparse_results:
            doc_id = result.document.id

            # Get the original score (dense_score or sparse_score)
            original_score = (
                result.score.dense_score
                if result.score.dense_score
                else result.score.sparse_score
            )

            if doc_id not in results_dict or original_score > self._get_original_score(
                results_dict[doc_id]
            ):
                # Create new result with original score as combined score
                new_score = SearchScore(
                    dense_score=result.score.dense_score,
                    sparse_score=result.score.sparse_score,
                    combined_score=original_score,
                )

                results_dict[doc_id] = SearchResult(
                    document=result.document,
                    score=new_score,
                    strategy_used=SearchStrategyType.HYBRID,
                )

        return list(results_dict.values())

    def _get_original_score(self, result: SearchResult) -> float:
        """Get the original score from a SearchResult."""
        return (
            result.score.dense_score
            if result.score.dense_score
            else result.score.sparse_score
        )

    def get_supported_strategies(self) -> List[str]:
        """Get list of supported search strategies."""
        return [strategy.value for strategy in SearchStrategyType]

    def rerank_results(
        self, query: str, results: List[SearchResult], top_k: int = None
    ) -> List[SearchResult]:
        """
        Rerank search results using Pinecone's reranking API for better relevance.

        Args:
            query: The search query text
            results: List of SearchResult objects to rerank
            top_k: Optional limit for number of results to return

        Returns:
            List of reranked SearchResult objects
        """
        if not results:
            return results

        # Prepare documents for Pinecone reranking API
        documents = []
        for result in results:
            documents.append(
                {
                    "_id": result.document.id,
                    "chunk_text": result.document.content,
                    "file_name": result.document.file_name or "",
                    "chunk_index": result.document.chunk_index,
                    **result.document.metadata,
                }
            )

        # Use Pinecone's reranking API
        rerank_result = self.pc.inference.rerank(
            model="bge-reranker-v2-m3",
            query=query,
            documents=documents,
            rank_fields=["chunk_text"],
            top_n=top_k or len(documents),
            return_documents=True,
            parameters={"truncate": "END"},
        )

        # Create reranked results with new scores
        reranked_results = []
        results_by_id = {result.document.id: result for result in results}

        for row in rerank_result.data:
            doc_id = row["document"]["_id"]
            original_result = results_by_id[doc_id]

            if row["score"] > SCORE_THRESHOLD:
                rerank_score = RerankedSearchScore(
                    score=row["score"],
                )

                reranked_result = SearchResult(
                    document=original_result.document,
                    score=rerank_score,
                    strategy_used=original_result.strategy_used,
                )

                reranked_results.append(reranked_result)

        return reranked_results
