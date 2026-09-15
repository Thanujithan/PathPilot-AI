from typing import TypedDict
from langgraph.graph import StateGraph, END

from agents.resume_agent import analyze_resume
from agents.skill_agent import analyze_skills
from agents.career_agent import recommend_careers
from agents.skill_gap_agent import analyze_skill_gaps
from agents.roadmap_agent import generate_learning_roadmap
from agents.job_agent import match_jobs


class ResumeState(TypedDict):
    resume_text: str
    analysis: str
    skill_analysis: str
    career_analysis: str
    skill_gap_analysis: str
    roadmap: str
    job_matches: str


def analyze_resume_node(state: ResumeState):
    result = analyze_resume(state["resume_text"])
    return {
        "analysis": result
    }


def analyze_skills_node(state: ResumeState):
    result = analyze_skills(state["analysis"])
    return {
        "skill_analysis": result
    }


def analyze_career_node(state: ResumeState):
    result = recommend_careers(
        state["analysis"],
        state["skill_analysis"]
    )
    return {
        "career_analysis": result
    }


def analyze_skill_gap_node(state: ResumeState):
    result = analyze_skill_gaps(
        state["skill_analysis"],
        state["career_analysis"]
    )
    return {
        "skill_gap_analysis": result
    }


def generate_roadmap_node(state: ResumeState):
    result = generate_learning_roadmap(
        state["skill_analysis"],
        state["career_analysis"],
        state["skill_gap_analysis"]
    )
    return {
        "roadmap": result
    }


def job_matching_node(state: ResumeState):
    result = match_jobs(
        state["analysis"],
        state["skill_analysis"],
        state["career_analysis"]
    )
    return {
        "job_matches": result
    }


# Create Graph
graph = StateGraph(ResumeState)

# Add Nodes
graph.add_node("resume_analysis", analyze_resume_node)
graph.add_node("skill_analysis", analyze_skills_node)
graph.add_node("career_analysis", analyze_career_node)
graph.add_node("skill_gap_analysis", analyze_skill_gap_node)
graph.add_node("roadmap", generate_roadmap_node)
graph.add_node("job_matching", job_matching_node)

# Starting point
graph.set_entry_point("resume_analysis")

# Flow
graph.add_edge("resume_analysis", "skill_analysis")
graph.add_edge("skill_analysis", "career_analysis")
graph.add_edge("career_analysis", "skill_gap_analysis")
graph.add_edge("skill_gap_analysis", "roadmap")
graph.add_edge("roadmap", "job_matching")
graph.add_edge("job_matching", END)

# Compile
resume_graph = graph.compile()