"""Document controller for handling PDF upload and processing operations."""

import logging
from typing import List

from fastapi import HTTPException, UploadFile

from app.domain.models.document import DocumentProcessResult
from app.infra.services.document_processing_service import DocumentProcessingService

logger = logging.getLogger(__name__)

# Maximum file size allowed for PDF uploads (in MB)
MAX_FILE_SIZE_MB = 50


class DocumentController:
    """Controller responsible for handling document upload and processing operations."""

    def __init__(self, document_processing_service: DocumentProcessingService):
        """
        Initialize DocumentController.

        Args:
            document_processing_service: Service for processing documents
        """
        self.document_processing_service = document_processing_service

    async def upload_documents(self, files: List[UploadFile]) -> DocumentProcessResult:
        """
        Process and index uploaded PDF documents.

        Args:
            files: List of uploaded PDF files

        Returns:
            DocumentProcessResult with processing statistics

        Raises:
            HTTPException: If validation fails or processing errors occur
        """
        try:
            # Validate uploaded files
            validated_files = await self._validate_pdf_files(files)

            result = await self.document_processing_service.process_documents(
                validated_files
            )

            logger.info(f"Successfully processed {result.documents_indexed} documents")

            return result

        except ValueError as e:
            logger.error(f"Document validation failed: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            logger.error(f"Document processing failed: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Internal server error during document processing",
            )

    async def _validate_pdf_files(self, files: List[UploadFile]) -> List[UploadFile]:
        """
        Validate that all uploaded files are PDF documents.

        Args:
            files: List of uploaded files to validate

        Returns:
            List of validated PDF files

        Raises:
            ValueError: If any file is not a valid PDF
        """
        if not files:
            raise ValueError("No files provided for upload")

        pdf_files = []
        max_file_size_bytes = MAX_FILE_SIZE_MB * 1024 * 1024

        for file in files:
            # Check file extension and content type
            if not (
                file.content_type == "application/pdf"
                or (file.filename and file.filename.lower().endswith(".pdf"))
            ):
                raise ValueError(
                    f"File '{file.filename}' is not a PDF. Only PDF files are allowed."
                )

            if file.size and file.size > max_file_size_bytes:
                raise ValueError(
                    f"File '{file.filename}' is too large. Maximum size is {MAX_FILE_SIZE_MB}MB."
                )

            pdf_files.append(file)

        return pdf_files
