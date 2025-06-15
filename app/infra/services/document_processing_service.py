import asyncio
from typing import List

import pymupdf
import pymupdf4llm
from fastapi import UploadFile
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.domain.interfaces.vector_store_interface import VectorStoreInterface
from app.domain.models.document import DocumentProcessResult


class DocumentProcessingService:
    def __init__(self, vector_store: VectorStoreInterface):
        self.vector_store = vector_store

    async def process_documents(self, files: List[UploadFile]) -> DocumentProcessResult:
        """
        Process and index uploaded PDF documents concurrently.

        Args:
            files: List of validated PDF files

        Returns:
            DocumentProcessResult with number of successfully processed documents
        """

        # Create a task for each file
        tasks = [asyncio.create_task(self._process_file(file)) for file in files]
        # Run all tasks concurrently and wait for completion
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Count successful processes and total chunks
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

    async def _process_file(self, file: UploadFile) -> None:
        """
        Process a single PDF file and index its content.

        Args:
            file: The PDF file to process
        """
        file_content = await file.read()

        doc = pymupdf.open(stream=file_content, filetype="pdf")
        md_text = pymupdf4llm.to_markdown(doc=doc)

        # Close the document to free memory
        doc.close()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100,
            length_function=len,
            is_separator_regex=False,
        )
        texts = text_splitter.create_documents([md_text])

        # Store documents in vector database
        await self.vector_store.store_documents(texts, file.filename)

        return texts
