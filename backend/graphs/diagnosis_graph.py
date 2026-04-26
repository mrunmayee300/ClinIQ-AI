from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from agents.medical_agents import (
    clinical_summary_agent,
    disease_ranking_agent,
    medical_knowledge_retrieval_agent,
    risk_assessment_agent,
    symptom_analysis_agent,
    treatment_recommendation_agent,
)
from graphs.state import ClinicalState


def build_diagnosis_graph():
    graph = StateGraph(ClinicalState)
    graph.add_node("symptom_analysis_agent_node", symptom_analysis_agent)
    graph.add_node("knowledge_retrieval_agent_node", medical_knowledge_retrieval_agent)
    graph.add_node("disease_ranking_agent_node", disease_ranking_agent)
    graph.add_node("risk_assessment_agent_node", risk_assessment_agent)
    graph.add_node("treatment_recommendation_agent_node", treatment_recommendation_agent)
    graph.add_node("clinical_summary_agent_node", clinical_summary_agent)

    graph.add_edge(START, "symptom_analysis_agent_node")
    graph.add_edge("symptom_analysis_agent_node", "knowledge_retrieval_agent_node")
    graph.add_edge("knowledge_retrieval_agent_node", "disease_ranking_agent_node")
    graph.add_edge("disease_ranking_agent_node", "risk_assessment_agent_node")
    graph.add_edge("risk_assessment_agent_node", "treatment_recommendation_agent_node")
    graph.add_edge("treatment_recommendation_agent_node", "clinical_summary_agent_node")
    graph.add_edge("clinical_summary_agent_node", END)

    return graph.compile()
