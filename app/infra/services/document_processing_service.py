from typing import List

from fastapi import UploadFile

from app.domain.models.document import DocumentProcessResult


class DocumentProcessingService:
    async def process_documents(self, files: List[UploadFile]) -> DocumentProcessResult:
        """
        Process and index uploaded PDF documents.

        Args:
            files: List of uploaded PDF files

        Returns:
            DocumentProcessResult with processing statistics
        """
        documents_indexed = len(files)  # Simulating processing
        return DocumentProcessResult(documents_indexed=documents_indexed)
