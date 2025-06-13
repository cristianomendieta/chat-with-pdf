import hashlib
from typing import Any, Dict, List

from pinecone import Pinecone
from sentence_transformers import SentenceTransformer

from app.domain.interfaces.vector_store_interface import VectorStoreInterface


class PineconeClient(VectorStoreInterface):
    """Pinecone implementation of the vector store interface."""

    def __init__(self, api_key: str, index_name: str, environment: str):
        """
        Initialize Pinecone client.

        Args:
            api_key: Pinecone API key
            index_name: Name of the Pinecone index
            environment: Pinecone environment
        """
        self.pc = Pinecone(api_key=api_key)
        self.index_name = index_name
        self.index = self.pc.Index(index_name)
        # Initialize embedding model
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    async def store_documents(
        self, documents: List[Dict[str, Any]], file_name: str
    ) -> None:
        """
        Store documents in Pinecone.

        Args:
            documents: List of documents with content and metadata
            file_name: Name of the original file for metadata
        """
        vectors_to_upsert = []

        for i, doc in enumerate(documents):
            # Extract content from document
            content = doc.get("page_content", "") if isinstance(doc, dict) else str(doc)

            # Generate embeddings
            embedding = self.embedding_model.encode(content).tolist()

            # Create unique ID using content hash and index
            content_hash = hashlib.md5(content.encode()).hexdigest()
            doc_id = f"{file_name}_{content_hash}_{i}"

            # Prepare metadata
            metadata = {
                "content": content,
                "file_name": file_name,
                "chunk_index": i,
                "chunk_size": len(content),
            }

            # Add any existing metadata from the document
            if isinstance(doc, dict) and "metadata" in doc:
                metadata.update(doc["metadata"])

            vectors_to_upsert.append(
                {"id": doc_id, "values": embedding, "metadata": metadata}
            )

        # Upsert vectors to Pinecone in batches
        batch_size = 100
        for i in range(0, len(vectors_to_upsert), batch_size):
            batch = vectors_to_upsert[i : i + batch_size]
            self.index.upsert(vectors=batch)

    async def search_similar(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar documents in Pinecone.

        Args:
            query: The search query
            k: Number of documents to return

        Returns:
            List of similar documents with metadata
        """
        # Generate query embedding
        query_embedding = self.embedding_model.encode(query).tolist()

        # Search in Pinecone
        results = self.index.query(
            vector=query_embedding, top_k=k, include_metadata=True
        )

        # Format results
        documents = []
        for match in results["matches"]:
            documents.append(
                {
                    "id": match["id"],
                    "score": match["score"],
                    "content": match["metadata"].get("content", ""),
                    "metadata": match["metadata"],
                }
            )

        return documents
