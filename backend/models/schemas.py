from typing import Any

from pydantic import BaseModel, Field


class LifestyleIndicators(BaseModel):
    smoking: bool = False
    alcohol: bool = False
    activity_level: str = "moderate"


class PatientInput(BaseModel):
    symptoms_text: str = Field(..., min_length=5, max_length=4000)
    age: int = Field(..., ge=0, le=120)
    gender: str = Field(..., min_length=1, max_length=32)
    medical_history: list[str] = Field(default_factory=list)
    medications: list[str] = Field(default_factory=list)
    severity: str = Field(default="moderate")
    lifestyle: LifestyleIndicators = Field(default_factory=LifestyleIndicators)


class ExtractedEntities(BaseModel):
    symptoms: list[str] = Field(default_factory=list)
    diseases_mentioned: list[str] = Field(default_factory=list)
    medications: list[str] = Field(default_factory=list)
    body_systems: list[str] = Field(default_factory=list)
    severity_terms: list[str] = Field(default_factory=list)
    temporal_patterns: list[str] = Field(default_factory=list)


class DiseaseRank(BaseModel):
    disease: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    reasoning: str


class TreatmentRecommendation(BaseModel):
    medications: list[str] = Field(default_factory=list)
    lifestyle_advice: list[str] = Field(default_factory=list)
    specialist_referral: str = ""
    emergency_flags: list[str] = Field(default_factory=list)


class ClinicalSummary(BaseModel):
    observed_symptoms: list[str]
    probable_diagnosis: list[DiseaseRank]
    risk_level: str
    suggested_next_steps: list[str]
    treatment_plan: TreatmentRecommendation
    disclaimer: str = "This system is AI-assisted and not a substitute for professional medical advice."


class AnalyzeSymptomsResponse(BaseModel):
    extracted_entities: ExtractedEntities
    normalized_text: str


class DiagnoseResponse(BaseModel):
    disease_ranking: list[DiseaseRank]
    summary: ClinicalSummary
    agent_trace: list[dict[str, Any]]
    retrieval_context: list[dict[str, Any]]
    retrieval_latency_ms: float = 0.0
    total_latency_ms: float = 0.0


class HealthResponse(BaseModel):
    status: str
    service: str
