"""Document processing service for handling PDF document operations."""

import asyncio
import io
import logging
from typing import List

import ocrmypdf
import pymupdf
import pymupdf4llm
from fastapi import UploadFile
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.domain.interfaces.vector_store_interface import VectorStoreInterface
from app.domain.models.document import DocumentProcessResult

INVALID_UNICODE = chr(0xFFFD)  # Character indicating unrecognized text by PyMuPDF

# Configure logger for this module
logger = logging.getLogger(__name__)


class DocumentProcessingService:
    """Service responsible for processing and indexing PDF documents."""

    def __init__(self, vector_store: VectorStoreInterface):
        """
        Initialize DocumentProcessingService.

        Args:
            vector_store: Vector store implementation for document storage
        """
        self.vector_store = vector_store

    def _ocr_page(self, page):
        """
        Extract text from a PDF page using OCRmyPDF.

        Based on the provided example implementation.

        Args:
            page: pymupdf.Page object

        Returns:
            OCR-ed text from the page
        """
        src = page.parent  # the page's document
        doc = pymupdf.open()  # make temporary 1-pager
        doc.insert_pdf(src, from_page=page.number, to_page=page.number)
        pdfbytes = doc.tobytes()
        inbytes = io.BytesIO(pdfbytes)  # transform to BytesIO object
        outbytes = io.BytesIO()  # let ocrmypdf store its result pdf here

        try:
            ocrmypdf.ocr(
                inbytes,
                outbytes,
                language=["por", "eng", "spa"],
                output_type="pdf",
                force_ocr=True,  # force OCR even if text is present
            )
            ocr_pdf = pymupdf.open("pdf", outbytes.getvalue())
            text = ocr_pdf[0].get_text()
            ocr_pdf.close()
            doc.close()
            return text
        except Exception as e:
            logger.error(f"OCR failed for page {page.number}: {e}")
            doc.close()
            return ""

    def _extract_text_with_full_ocr(self, doc) -> str:
        """
        Extract text from PDF using full OCR on all pages.
        This approach is used when the document has too many unrecognized characters.

        Args:
            doc: PyMuPDF document object

        Returns:
            Extracted text with OCR applied to all pages
        """
        all_text = []

        logger.info(f"Starting OCR for {doc.page_count} pages...")

        for page_num in range(doc.page_count):
            page = doc[page_num]

            try:
                ocr_text = self._ocr_page(page)
                if ocr_text.strip():
                    all_text.append(f"--- Página {page_num + 1} ---\n{ocr_text}")
                    logger.debug(f"OCR completed for page {page_num + 1}")
                else:
                    logger.warning(f"No text extracted from page {page_num + 1}")
            except Exception as e:
                logger.error(f"Failed to OCR page {page_num + 1}: {e}")
                continue

        final_text = "\n\n".join(all_text)
        logger.info(f"OCR completed. Extracted {len(final_text)} characters total.")

        return final_text

    def _should_use_ocr(self, text: str, invalid_char_threshold: float = 0.1) -> bool:
        """
        Determine if OCR should be used based on the proportion of unrecognized characters.

        Args:
            text: Extracted text from PDF
            invalid_char_threshold: Maximum proportion of invalid characters before OCR is needed (default: 10%)

        Returns:
            True if OCR should be used, False otherwise
        """
        if not text or len(text.strip()) < 50:
            return True

        # Count invalid Unicode characters (unrecognized by PyMuPDF)
        invalid_chars = text.count(INVALID_UNICODE)
        total_chars = len(text)

        if total_chars == 0:
            return True

        # Calculate proportion of invalid characters
        invalid_ratio = invalid_chars / total_chars

        # Use OCR if more than threshold% of characters are unrecognized
        return invalid_ratio > invalid_char_threshold

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
        Uses selective OCR as fallback when traditional text extraction fails.

        Args:
            file: The PDF file to process

        Returns:
            List of document chunks created from the file
        """
        file_content = await file.read()

        # Extract text content from PDF using pymupdf
        doc = pymupdf.open(stream=file_content, filetype="pdf")

        try:
            # First, try traditional text extraction
            md_text = pymupdf4llm.to_markdown(doc=doc)

            # Check if OCR is needed based on invalid character proportion
            if self._should_use_ocr(md_text):
                logger.info(
                    f"Using full OCR for {file.filename} (too many unrecognized characters)"
                )
                ocr_text = self._extract_text_with_full_ocr(doc)
                if ocr_text and len(ocr_text.strip()) > 0:
                    md_text = ocr_text
                    logger.info(f"OCR successful for {file.filename}")
                else:
                    logger.warning(
                        "OCR didn't extract any text, keeping traditional extraction"
                    )
            else:
                logger.debug(f"Traditional extraction sufficient for {file.filename}")

        finally:
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
