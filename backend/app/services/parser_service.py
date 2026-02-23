import fitz  # PyMuPDF
from docx import Document
from fastapi import UploadFile
import logging
import re
from io import BytesIO

logger = logging.getLogger(__name__)


class ResumeParser:

    @staticmethod
    async def extract_text(file: UploadFile) -> str:
        """
        Extract text from uploaded PDF or DOCX file.
        """

        filename = file.filename.lower()

        if filename.endswith(".pdf"):
            raw_text = await ResumeParser._extract_pdf(file)

        elif filename.endswith(".docx"):
            raw_text = await ResumeParser._extract_docx(file)

        else:
            raise ValueError("Unsupported file format. Only PDF and DOCX allowed.")

        # Clean and normalize extracted text
        cleaned_text = ResumeParser._clean_text(raw_text)
        return cleaned_text


    @staticmethod
    async def _extract_pdf(file: UploadFile) -> str:
        try:
            content = await file.read()
            pdf = fitz.open(stream=content, filetype="pdf")

            text = ""
            for page in pdf:
                text += page.get_text()

            return text

        except Exception as e:
            logger.error(f"PDF extraction failed: {e}")
            raise


    @staticmethod
    async def _extract_docx(file: UploadFile) -> str:
        try:
            content = await file.read()
            doc = Document(BytesIO(content))

            text = "\n".join([para.text for para in doc.paragraphs])
            return text

        except Exception as e:
            logger.error(f"DOCX extraction failed: {e}")
            raise


    @staticmethod
    def _clean_text(text: str) -> str:
        """
        Normalize extracted text to reduce formatting differences.
        """

        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)

        # Remove strange unicode characters
        text = text.encode("ascii", "ignore").decode()

        # Lowercase for consistency
        text = text.lower().strip()

        return text
