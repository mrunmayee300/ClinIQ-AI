from typing import Any, TypedDict


class DiagnosisState(TypedDict, total=False):
    patient_input: dict[str, Any]
    extracted_entities: dict[str, Any]
    retrieval_context: list[dict[str, Any]]
    disease_ranking: list[dict[str, Any]]
    risk_level: str
    treatment_recommendations: dict[str, Any]
    clinical_summary: dict[str, Any]
    agent_trace: list[dict[str, Any]]
