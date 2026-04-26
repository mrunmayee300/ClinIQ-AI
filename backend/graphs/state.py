from typing import Any, TypedDict


class ClinicalState(TypedDict, total=False):
    patient_input: dict[str, Any]
    symptoms: list[str]
    extracted_entities: dict[str, Any]
    retrieved_docs: list[dict[str, Any]]
    retrieval_context: list[dict[str, Any]]
    disease_scores: dict[str, float]
    disease_ranking: list[dict[str, Any]]
    risk_level: str
    recommendations: list[str]
    treatment_recommendations: dict[str, Any]
    summary: str
    clinical_summary: dict[str, Any]
    agent_trace: list[dict[str, Any]]


DiagnosisState = ClinicalState
