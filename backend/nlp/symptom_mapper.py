from __future__ import annotations

import re


SYMPTOM_LEXICON = {
    "fever",
    "cough",
    "fatigue",
    "headache",
    "chest pain",
    "shortness of breath",
    "rash",
    "joint pain",
}

SEVERITY_TERMS = {"mild", "moderate", "severe", "acute", "chronic", "worsening"}


def map_symptoms(text: str) -> list[str]:
    lowered = text.lower()
    return sorted({item for item in SYMPTOM_LEXICON if item in lowered})


def map_severity(text: str) -> list[str]:
    lowered = text.lower()
    return sorted({term for term in SEVERITY_TERMS if re.search(rf"\b{term}\b", lowered)})
