import argparse
import csv
import re
from pathlib import Path


STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "been",
    "but",
    "by",
    "for",
    "from",
    "have",
    "i",
    "in",
    "is",
    "it",
    "my",
    "of",
    "on",
    "or",
    "that",
    "the",
    "this",
    "to",
    "was",
    "with",
}


def normalize_text(text: str) -> str:
    lowered = text.lower().strip()
    lowered = re.sub(r"\s+", " ", lowered)
    return lowered


def infer_symptoms(notes: str) -> str:
    tokens = re.findall(r"[a-zA-Z][a-zA-Z\-']+", notes.lower())
    kept = [token for token in tokens if token not in STOPWORDS and len(token) > 2]
    # Deduplicate while preserving order and keep a compact symptom field
    unique_tokens = list(dict.fromkeys(kept))[:25]
    return "; ".join(unique_tokens)


def preprocess_records(input_csv: Path, output_csv: Path) -> int:
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    dedupe = set()
    written = 0

    with input_csv.open("r", encoding="utf-8", newline="") as src, output_csv.open(
        "w", encoding="utf-8", newline=""
    ) as dst:
        reader = csv.DictReader(src)
        writer = csv.DictWriter(dst, fieldnames=["symptoms", "diagnosis", "medications", "notes", "source"])
        writer.writeheader()

        for row in reader:
            diagnosis = normalize_text((row.get("label") or row.get("diagnosis") or "unknown"))
            notes = normalize_text((row.get("text") or row.get("notes") or ""))
            if not notes:
                continue
            source = normalize_text((row.get("source") or "symptom2disease"))
            symptoms = infer_symptoms(notes)
            medications = normalize_text((row.get("medications") or "unknown"))

            dedupe_key = (diagnosis, notes)
            if dedupe_key in dedupe:
                continue
            dedupe.add(dedupe_key)

            writer.writerow(
                {
                    "symptoms": symptoms if symptoms else "unknown",
                    "diagnosis": diagnosis if diagnosis else "unknown",
                    "medications": medications if medications else "unknown",
                    "notes": notes,
                    "source": source,
                }
            )
            written += 1
            if written % 250 == 0:
                print(f"[preprocess] processed {written} records...")

    return written


def main() -> None:
    parser = argparse.ArgumentParser(description="Preprocess clinical records into normalized schema.")
    parser.add_argument(
        "--input",
        default="datasets/raw/symptom2disease_raw.csv",
        help="Input raw CSV path.",
    )
    parser.add_argument(
        "--output",
        default="datasets/processed/clinical_records.csv",
        help="Output processed CSV path.",
    )
    args = parser.parse_args()

    input_csv = Path(args.input)
    output_csv = Path(args.output)
    if not input_csv.exists():
        raise FileNotFoundError(f"Input file not found: {input_csv}")

    print(f"[preprocess] reading {input_csv}")
    total = preprocess_records(input_csv, output_csv)
    print(f"[preprocess] wrote {total} normalized records to {output_csv}")


if __name__ == "__main__":
    main()
