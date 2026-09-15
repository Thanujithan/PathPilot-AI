import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)


def recommend_careers(resume_analysis: str, skill_analysis: str):

    prompt = f"""
You are a professional Career Recommendation AI Agent.

Analyze the candidate's resume analysis and skill analysis.
Recommend suitable career paths based on their current skills,
experience, education, and interests.

Return ONLY valid JSON.
Do not add markdown.
Do not add ```json.
Do not add explanations outside the JSON.

Use exactly this structure:

{{
    "top_career": {{
        "title": "",
        "reason": "",
        "match_percentage": 0
    }},
    "alternative_careers": [
        {{
            "title": "",
            "reason": "",
            "match_percentage": 0
        }}
    ],
    "skills_needed_for_top_career": [],
    "next_steps": []
}}

Important:
- match_percentage is an AI-generated estimate.
- Do not claim it is a formal professional assessment.
- Recommend realistic career paths.
- Do not invent specific companies or job vacancies.

Resume Analysis:

{resume_analysis}

Skill Analysis:

{skill_analysis}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text