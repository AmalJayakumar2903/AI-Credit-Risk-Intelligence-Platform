from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from backend.ai.risk_explainer import (
    generate_risk_explanation
)


class RiskState(TypedDict):

    portfolio: dict
    risk: dict
    risk_drivers: dict
    recommendations: list
    ai_explanation: str


def generate_explanation(state: RiskState):

    explanation = generate_risk_explanation(

        state["portfolio"],
        state["risk"],
        state["risk_drivers"],
        state["recommendations"]

    )

    return {
        "ai_explanation": explanation
    }


graph = StateGraph(RiskState)

graph.add_node(
    "generate_explanation",
    generate_explanation
)

graph.add_edge(
    START,
    "generate_explanation"
)

graph.add_edge(
    "generate_explanation",
    END
)

risk_graph = graph.compile()