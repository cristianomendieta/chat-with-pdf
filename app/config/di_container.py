import os

from kink import di

from app.controllers import DocumentController, QuestionController
from app.domain.interfaces.vector_store_interface import VectorStoreInterface
from app.infra.gateways.pinecone_client import PineconeClient
from app.infra.services import DocumentProcessingService


def di_container() -> None:
    # gateways
    di[VectorStoreInterface] = lambda di: PineconeClient(
        api_key=os.getenv("PINECONE_API_KEY", ""),
        index_name=os.getenv("PINECONE_INDEX_NAME", "pdf-chat"),
        environment=os.getenv("PINECONE_ENVIRONMENT", ""),
    )

    # services
    di[DocumentProcessingService] = lambda di: DocumentProcessingService(
        vector_store=di[VectorStoreInterface]
    )

    # controllers
    di[DocumentController] = lambda di: DocumentController(
        document_processing_service=di[DocumentProcessingService]
    )
    di[QuestionController] = lambda di: QuestionController()
