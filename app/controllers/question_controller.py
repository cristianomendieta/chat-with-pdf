import logging

from fastapi import HTTPException

from app.domain.models.question import QuestionRequest, QuestionResult

logger = logging.getLogger(__name__)


class QuestionController:
    """
    Controller responsible for handling question answering operations.
    """

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

            # For now, return a mock answer until the service layer is implemented
            result = QuestionResult(
                answer=f"This is a mock answer for your question: '{validated_request.question}'. The actual implementation will use AI to process documents and provide relevant answers.",
                references=["Mock reference 1", "Mock reference 2"],
            )

            logger.info(f"Successfully answered question: '{request.question[:50]}...'")

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

        return QuestionRequest(question=question)

    async def get_question_service_status(self) -> dict:
        """
        Get the current status of the question answering service.

        Returns:
            Dictionary with service status information
        """
        try:
            return {
                "status": "ready",
                "message": "Question answering service is operational (mock implementation)",
            }
        except Exception as e:
            logger.error(f"Failed to get question service status: {str(e)}")
            return {
                "status": "error",
                "message": "Question answering service is experiencing issues",
            }
