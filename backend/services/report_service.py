from __future__ import annotations

from io import BytesIO

from pypdf import PdfReader


class ReportService:
    @staticmethod
    def extract_pdf_text(content: bytes) -> str:
        reader = PdfReader(BytesIO(content))
        return "\n".join(page.extract_text() or "" for page in reader.pages).strip()
