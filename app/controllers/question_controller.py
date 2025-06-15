import logging

from fastapi import HTTPException

from app.domain.models.question import QuestionRequest, QuestionResult
from app.infra.services.question_answering_service import QuestionAnsweringService

logger = logging.getLogger(__name__)


class QuestionController:
    """
    Controller responsible for handling question answering operations.
    """

    def __init__(self, question_answering_service: QuestionAnsweringService):
        """
        Initialize QuestionController.

        Args:
            question_answering_service: Service for processing questions
        """
        self.question_answering_service = question_answering_service

    async def ask_question(self, request: QuestionRequest) -> QuestionResult:
        """
        Process a question and generate an answer based on indexed documents.

        Args:
            request: The question request containing the user's question

        Returns:
            QuestionResult with the generated answer and source references

        Raises:
            HTTPException: If processing fails or no documents are available
        """
        try:
            # Validate the question
            validated_request = self._validate_question_request(request)

            # Process the question using the service
            result = await self.question_answering_service.answer_question(
                validated_request,
                search_strategy=validated_request.search_strategy or "hybrid",
                max_context_documents=validated_request.max_documents or 5,
            )

            logger.info(
                f"Successfully answered question using {result.search_strategy} strategy: '{request.question[:50]}...'"
            )

            return result

        except ValueError as e:
            logger.error(f"Question validation failed: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            logger.error(f"Question processing failed: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Internal server error during question processing",
            )

    def _validate_question_request(self, request: QuestionRequest) -> QuestionRequest:
        """
        Validate the question request.

        Args:
            request: The question request to validate

        Returns:
            Validated question request

        Raises:
            ValueError: If the request is invalid
        """
        if not request.question or not request.question.strip():
            raise ValueError("Question cannot be empty")

        # Trim whitespace and check minimum length
        question = request.question.strip()
        if len(question) < 3:
            raise ValueError("Question must be at least 3 characters long")

        # Check maximum length to prevent abuse
        if len(question) > 1000:
            raise ValueError("Question is too long. Maximum length is 1000 characters")

        # Validate search strategy
        valid_strategies = ["dense", "sparse", "hybrid"]
        if request.search_strategy and request.search_strategy not in valid_strategies:
            raise ValueError(
                f"Invalid search strategy. Must be one of: {valid_strategies}"
            )

        # Validate max_documents
        if request.max_documents and (
            request.max_documents < 1 or request.max_documents > 20
        ):
            raise ValueError("max_documents must be between 1 and 20")

        return QuestionRequest(
            question=question,
            search_strategy=request.search_strategy or "hybrid",
            max_documents=request.max_documents or 5,
        )

    async def get_question_service_status(self) -> dict:
        """
        Get the current status of the question answering service.

        Returns:
            Dictionary with service status information
        """
        try:
            stats = await self.question_answering_service.get_search_statistics()
            return {
                "status": "ready",
                "message": "Question answering service is operational with hybrid search",
                "available_strategies": stats.get("available_strategies", []),
                "index_statistics": stats.get("index_statistics", {}),
            }
        except Exception as e:
            logger.error(f"Failed to get question service status: {str(e)}")
            return {
                "status": "error",
                "message": "Question answering service is experiencing issues",
                "error": str(e),
            }
