from typing import TypedDict
from langgraph.graph import StateGraph, END

from agents.master_agent import analyze_complete_career_profile


class ResumeState(TypedDict):
    resume_text: str
    analysis: str
    skill_analysis: str
    career_analysis: str
    skill_gap_analysis: str
    roadmap: str
    job_matches: str


def complete_analysis_node(state: ResumeState):

    result = analyze_complete_career_profile(
        state["resume_text"]
    )

    return {
        "analysis": result.get(
            "analysis",
            {}
        ),

        "skill_analysis": result.get(
            "skill_analysis",
            {}
        ),

        "career_analysis": result.get(
            "career_analysis",
            {}
        ),

        "skill_gap_analysis": result.get(
            "skill_gap_analysis",
            {}
        ),

        "roadmap": result.get(
            "roadmap",
            {}
        ),

        "job_matches": result.get(
            "job_matches",
            {}
        ),
    }


# ==========================================
# CREATE CAREPLANIX GRAPH
# ==========================================

graph = StateGraph(ResumeState)


# ==========================================
# ADD NODE
# ==========================================

graph.add_node(
    "complete_career_analysis",
    complete_analysis_node
)


# ==========================================
# ENTRY POINT
# ==========================================

graph.set_entry_point(
    "complete_career_analysis"
)


# ==========================================
# END
# ==========================================

graph.add_edge(
    "complete_career_analysis",
    END
)


# ==========================================
# COMPILE
# ==========================================

resume_graph = graph.compile()