"""Dependency injection container configuration."""

from kink import di

from app.controllers import DocumentController, QuestionController
from app.domain.interfaces.vector_store_interface import VectorStoreInterface
from app.infra.gateways.pinecone_client import PineconeClient
from app.infra.services import DocumentProcessingService
from app.infra.services.question_answering_service import QuestionAnsweringService


def di_container() -> None:
    """Configure dependency injection container with service bindings."""

    # Gateway implementations
    di[VectorStoreInterface] = lambda di: PineconeClient()

    # Business services
    di[DocumentProcessingService] = lambda di: DocumentProcessingService(
        vector_store=di[VectorStoreInterface]
    )

    di[QuestionAnsweringService] = lambda di: QuestionAnsweringService(
        vector_store=di[VectorStoreInterface]
    )

    # API controllers
    di[DocumentController] = lambda di: DocumentController(
        document_processing_service=di[DocumentProcessingService]
    )

    di[QuestionController] = lambda di: QuestionController(
        question_answering_service=di[QuestionAnsweringService]
    )
