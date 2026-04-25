from __future__ import annotations

import re
from functools import lru_cache

from transformers import pipeline

from models.schemas import ExtractedEntities


SYMPTOM_LEXICON = {
    "fever",
    "chest pain",
    "hypertension",
    "diabetes",
    "fatigue",
    "shortness of breath",
    "cough",
    "headache",
}

BODY_SYSTEMS = {
    "cardiovascular": ["chest pain", "palpitations", "hypertension"],
    "respiratory": ["shortness of breath", "cough", "wheezing"],
    "endocrine": ["diabetes", "thirst", "polyuria"],
}

SEVERITY_TERMS = {"mild", "moderate", "severe", "acute", "chronic", "worsening"}


@lru_cache(maxsize=1)
def _ner_pipeline():
    return pipeline(
        "token-classification",
        model="dmis-lab/biobert-base-cased-v1.2",
        aggregation_strategy="simple",
    )


def _match_lexicon(text: str) -> list[str]:
    lowered = text.lower()
    found = [token for token in SYMPTOM_LEXICON if token in lowered]
    return sorted(set(found))


def extract_entities(text: str) -> ExtractedEntities:
    entities = ExtractedEntities()
    entities.symptoms = _match_lexicon(text)

    ner = _ner_pipeline()(text)
    diseases, meds = set(), set()
    for item in ner:
        token = item.get("word", "").strip()
        group = item.get("entity_group", "").upper()
        if not token:
            continue
        if group in {"DISEASE", "DISORDER"}:
            diseases.add(token.lower())
        if group in {"CHEMICAL", "DRUG"}:
            meds.add(token.lower())

    entities.diseases_mentioned = sorted(diseases)
    entities.medications = sorted(meds)

    normalized = text.lower()
    systems = []
    for system, triggers in BODY_SYSTEMS.items():
        if any(trigger in normalized for trigger in triggers):
            systems.append(system)
    entities.body_systems = systems

    entities.severity_terms = sorted({word for word in SEVERITY_TERMS if re.search(rf"\b{word}\b", normalized)})
    entities.temporal_patterns = re.findall(r"\b(\d+\s*(?:days?|weeks?|months?|years?))\b", normalized)
    return entities
