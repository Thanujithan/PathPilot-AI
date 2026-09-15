import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)


def generate_learning_roadmap(
    skill_analysis: str,
    career_analysis: str,
    skill_gap_analysis: str
):

    prompt = f"""
You are a professional AI Learning Roadmap Agent.

Create a practical learning roadmap for the candidate based on:
1. Current skills
2. Recommended career
3. Identified skill gaps

The roadmap should help the candidate progress from their current
level toward being job-ready.

Return ONLY valid JSON.
Do not add markdown.
Do not add ```json.
Do not add explanations outside the JSON.

Use exactly this structure:

{{
    "target_career": "",
    "roadmap": [
        {{
            "phase": "",
            "duration": "",
            "skills": [],
            "topics": [],
            "projects": [],
            "practice": []
        }}
    ],
    "portfolio_projects": [],
    "interview_preparation": [],
    "job_preparation": []
}}

Important:
- Make the roadmap practical and realistic.
- Order the learning topics logically.
- Include hands-on projects.
- Include interview preparation.
- Include job application preparation.
- Avoid unrealistic timelines.

Current Skill Analysis:

{skill_analysis}

Career Analysis:

{career_analysis}

Skill Gap Analysis:

{skill_gap_analysis}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text