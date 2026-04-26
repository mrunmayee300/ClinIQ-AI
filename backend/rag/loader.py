from __future__ import annotations

import csv
from pathlib import Path

from pypdf import PdfReader


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def _read_pdf(path: Path) -> str:
    reader = PdfReader(str(path))
    return "\n".join((page.extract_text() or "") for page in reader.pages).strip()


def _read_csv_rows(path: Path) -> list[dict]:
    records = []
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            notes = (row.get("notes") or row.get("text") or "").strip()
            if not notes:
                continue
            records.append(
                {
                    "text": notes,
                    "source": str(path),
                    "disease": (row.get("diagnosis") or row.get("label") or "unknown").strip().lower(),
                    "section": "clinical_record",
                }
            )
    return records


def load_documents(source_dir: str) -> list[dict]:
    docs: list[dict] = []
    for path in Path(source_dir).glob("**/*"):
        if not path.is_file():
            continue
        suffix = path.suffix.lower()
        if suffix == ".txt":
            text = _read_text(path).strip()
            if text:
                docs.append({"text": text, "source": str(path), "disease": "unknown", "section": "text"})
        elif suffix == ".pdf":
            text = _read_pdf(path).strip()
            if text:
                docs.append({"text": text, "source": str(path), "disease": "unknown", "section": "pdf"})
        elif suffix == ".csv":
            docs.extend(_read_csv_rows(path))
    return docs
