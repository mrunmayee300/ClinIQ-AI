from __future__ import annotations

from collections import Counter

from models.schemas import DiseaseRank, TreatmentRecommendation


DISEASE_RULES = {
    "influenza": {"fever", "fatigue", "cough"},
    "viral fever": {"fever", "fatigue", "headache"},
    "covid-19": {"fever", "shortness of breath", "cough", "fatigue"},
    "angina": {"chest pain", "shortness of breath"},
}


def symptom_analysis_agent(state):
    entities = state.get("extracted_entities", {})
    trace = state.get("agent_trace", [])
    trace.append({"agent": "Symptom Analysis Agent", "status": "completed", "symptom_count": len(entities.get("symptoms", []))})
    state["agent_trace"] = trace
    return state


def medical_knowledge_retrieval_agent(state):
    trace = state.get("agent_trace", [])
    trace.append(
        {"agent": "Medical Knowledge Retrieval Agent", "status": "completed", "documents": len(state.get("retrieval_context", []))}
    )
    state["agent_trace"] = trace
    return state


def disease_ranking_agent(state):
    symptoms = set(state.get("extracted_entities", {}).get("symptoms", []))
    scores = Counter()
    for disease, disease_symptoms in DISEASE_RULES.items():
        overlap = symptoms.intersection(disease_symptoms)
        if overlap:
            scores[disease] = len(overlap) / max(len(disease_symptoms), 1)

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:5]
    state["disease_ranking"] = [
        DiseaseRank(disease=d, confidence=round(c, 3), reasoning=f"Matched {int(c * len(DISEASE_RULES[d]))} key symptoms.").model_dump()
        for d, c in ranked
    ]
    state.setdefault("agent_trace", []).append({"agent": "Disease Ranking Agent", "status": "completed", "ranked_count": len(ranked)})
    return state


def risk_assessment_agent(state):
    severity_terms = state.get("extracted_entities", {}).get("severity_terms", [])
    risk = "medium"
    if "severe" in severity_terms or "worsening" in severity_terms:
        risk = "high"
    elif "mild" in severity_terms and "moderate" not in severity_terms:
        risk = "low"
    state["risk_level"] = risk
    state.setdefault("agent_trace", []).append({"agent": "Risk Assessment Agent", "status": "completed", "risk_level": risk})
    return state


def treatment_recommendation_agent(state):
    risk = state.get("risk_level", "medium")
    recommendation = TreatmentRecommendation(
        medications=["Paracetamol (if clinically appropriate)"],
        lifestyle_advice=["Hydration", "Adequate rest", "Monitor symptoms every 6-8 hours"],
        specialist_referral="Internal Medicine",
        emergency_flags=["Persistent chest pain", "Severe breathing difficulty"] if risk == "high" else [],
    )
    state["treatment_recommendations"] = recommendation.model_dump()
    state.setdefault("agent_trace", []).append({"agent": "Treatment Recommendation Agent", "status": "completed"})
    return state


def clinical_summary_agent(state):
    state["clinical_summary"] = {
        "observed_symptoms": state.get("extracted_entities", {}).get("symptoms", []),
        "probable_diagnosis": state.get("disease_ranking", []),
        "risk_level": state.get("risk_level", "medium"),
        "suggested_next_steps": [
            "Schedule physician consultation within 24 hours.",
            "Run CBC/CRP and basic vitals review.",
            "Escalate to emergency care if red-flag symptoms appear.",
        ],
        "treatment_plan": state.get("treatment_recommendations", {}),
    }
    state.setdefault("agent_trace", []).append({"agent": "Clinical Summary Agent", "status": "completed"})
    return state
