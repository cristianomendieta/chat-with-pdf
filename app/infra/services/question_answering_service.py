import logging
from typing import Any, Dict, Optional

from app.domain.interfaces.vector_store_interface import VectorStoreInterface
from app.domain.models.question import QuestionRequest, QuestionResult
from app.infra.llm.chains import RAGChain

logger = logging.getLogger(__name__)


class QuestionAnsweringService:
    """Service for handling question answering with hybrid search capabilities."""

    def __init__(self, vector_store: VectorStoreInterface):
        """
        Initialize QuestionAnsweringService.

        Args:
            vector_store: Vector store implementation for searching documents
        """
        self.vector_store = vector_store
        self.rag_chain = RAGChain()

    async def answer_question(
        self,
        request: QuestionRequest,
        search_strategy: str = "hybrid",
        max_context_documents: int = 5,
        filters: Optional[Dict[str, Any]] = None,
    ) -> QuestionResult:
        """
        Answer a question using the specified search strategy.

        Args:
            request: The question request
            search_strategy: Search strategy to use ('dense', 'sparse', 'hybrid')
            max_context_documents: Maximum number of documents to use as context
            filters: Optional filters to apply to the search

        Returns:
            QuestionResult with answer and references
        """
        try:
            # Search for relevant documents
            relevant_docs = await self.vector_store.search_similar(
                query=request.question,
                k=max_context_documents,
                strategy=search_strategy,
                filters=filters,
            )

            if not relevant_docs:
                return QuestionResult(
                    answer="Sorry, I couldn't find relevant information to answer your question in the indexed documents.",
                    references=[],
                )

            context_documents = [doc.document.content for doc in relevant_docs]
            answer = self.rag_chain.generate_answer(
                question=request.question, docs_content=context_documents
            )

            return QuestionResult(
                answer=answer,
                references=context_documents,
            )

        except Exception as e:
            logger.error(f"Error answering question: {str(e)}")
            return QuestionResult(
                answer=f"An error occurred while processing your question: {str(e)}",
                references=[],
            )
