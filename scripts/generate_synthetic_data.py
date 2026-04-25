import csv
import random
from pathlib import Path

SYMPTOMS = ["fever", "cough", "fatigue", "headache", "chest pain", "shortness of breath"]
DISEASES = ["influenza", "viral fever", "covid-19", "angina", "bronchitis"]
TREATMENTS = ["rest", "hydration", "paracetamol", "antiviral evaluation", "cardiology referral"]


def main(rows: int = 5000):
    target = Path("datasets/synthetic_patient_records.csv")
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["record_id", "age", "gender", "symptoms", "probable_disease", "treatment"])
        for idx in range(1, rows + 1):
            symptoms = random.sample(SYMPTOMS, k=random.randint(2, 4))
            writer.writerow(
                [
                    f"REC-{idx:05d}",
                    random.randint(1, 90),
                    random.choice(["female", "male", "other"]),
                    "; ".join(symptoms),
                    random.choice(DISEASES),
                    random.choice(TREATMENTS),
                ]
            )


if __name__ == "__main__":
    main()
