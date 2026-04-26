import argparse
import csv
from pathlib import Path


def stage_symptom2disease(source_csv: Path, output_csv: Path) -> int:
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with source_csv.open("r", encoding="utf-8", newline="") as src, output_csv.open(
        "w", encoding="utf-8", newline=""
    ) as dst:
        reader = csv.DictReader(src)
        writer = csv.DictWriter(dst, fieldnames=["label", "text", "source"])
        writer.writeheader()
        for row in reader:
            label = (row.get("label") or "").strip()
            text = (row.get("text") or "").strip()
            if not label or not text:
                continue
            writer.writerow({"label": label, "text": text, "source": "Symptom2Disease"})
            count += 1
    return count


def main() -> None:
    parser = argparse.ArgumentParser(description="Stage medical datasets into datasets/raw.")
    parser.add_argument(
        "--source",
        default="datasets/Symptom2Disease.csv",
        help="Path to Symptom2Disease CSV file.",
    )
    parser.add_argument(
        "--out",
        default="datasets/raw/symptom2disease_raw.csv",
        help="Output path for staged raw dataset.",
    )
    args = parser.parse_args()

    source_csv = Path(args.source)
    output_csv = Path(args.out)
    if not source_csv.exists():
        raise FileNotFoundError(f"Source file not found: {source_csv}")

    print(f"[load] staging dataset from {source_csv}")
    rows = stage_symptom2disease(source_csv, output_csv)
    print(f"[load] wrote {rows} rows to {output_csv}")


if __name__ == "__main__":
    main()
