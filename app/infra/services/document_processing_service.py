"""Document processing service for handling PDF document operations."""

import asyncio
from typing import List

import pymupdf
import pymupdf4llm
from fastapi import UploadFile
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.domain.interfaces.vector_store_interface import VectorStoreInterface
from app.domain.models.document import DocumentProcessResult


class DocumentProcessingService:
    """Service responsible for processing and indexing PDF documents."""

    def __init__(self, vector_store: VectorStoreInterface):
        """
        Initialize DocumentProcessingService.

        Args:
            vector_store: Vector store implementation for document storage
        """
        self.vector_store = vector_store

    async def process_documents(self, files: List[UploadFile]) -> DocumentProcessResult:
        """
        Process and index uploaded PDF documents concurrently.

        Args:
            files: List of validated PDF files

        Returns:
            DocumentProcessResult with number of successfully processed documents
        """

        # Create concurrent tasks for each file
        tasks = [asyncio.create_task(self._process_file(file)) for file in files]

        # Execute all tasks concurrently and collect results
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Calculate processing statistics
        success_count = 0
        total_chunks = 0

        for result in results:
            if not isinstance(result, Exception):
                success_count += 1
                if isinstance(result, list):
                    total_chunks += len(result)

        return DocumentProcessResult(
            documents_indexed=success_count, total_chunks=total_chunks
        )

    async def _process_file(self, file: UploadFile) -> List:
        """
        Process a single PDF file and index its content.

        Args:
            file: The PDF file to process

        Returns:
            List of document chunks created from the file
        """
        file_content = await file.read()

        # Extract text content from PDF using pymupdf
        doc = pymupdf.open(stream=file_content, filetype="pdf")
        md_text = pymupdf4llm.to_markdown(doc=doc)
        doc.close()  # Free memory immediately

        # Split text into manageable chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            is_separator_regex=False,
        )
        texts = text_splitter.create_documents([md_text])

        # Store document chunks in vector database
        await self.vector_store.store_documents(texts, file.filename)

        return texts
