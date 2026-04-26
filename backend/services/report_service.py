from __future__ import annotations

from io import BytesIO

from pypdf import PdfReader


class ReportService:
    @staticmethod
    def extract_pdf_text(content: bytes) -> str:
        extracted = []
        try:
            import pdfplumber

            with pdfplumber.open(BytesIO(content)) as pdf:
                extracted.extend((page.extract_text() or "") for page in pdf.pages)
        except Exception:
            extracted = []

        if not "".join(extracted).strip():
            try:
                import fitz

                doc = fitz.open(stream=content, filetype="pdf")
                extracted = [page.get_text("text") or "" for page in doc]
                doc.close()
            except Exception:
                extracted = []

        if not "".join(extracted).strip():
            reader = PdfReader(BytesIO(content))
            extracted = [page.extract_text() or "" for page in reader.pages]

        return "\n".join(extracted).strip()
