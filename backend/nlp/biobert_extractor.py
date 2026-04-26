from __future__ import annotations

import re

from models.schemas import ExtractedEntities
from nlp.entity_extractor import extract_tokens
from nlp.symptom_mapper import map_severity, map_symptoms

BODY_SYSTEMS = {
    "cardiovascular": ["chest pain", "palpitations", "hypertension"],
    "respiratory": ["shortness of breath", "cough", "wheezing"],
    "endocrine": ["diabetes", "thirst", "polyuria"],
}


def extract_entities(text: str) -> ExtractedEntities:
    entities = ExtractedEntities()
    entities.symptoms = map_symptoms(text)

    ner = extract_tokens(text)
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

    entities.severity_terms = map_severity(text)
    entities.temporal_patterns = re.findall(r"\b(\d+\s*(?:days?|weeks?|months?|years?))\b", normalized)
    return entities
