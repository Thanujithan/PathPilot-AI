import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)


def analyze_skills(resume_analysis: str):

    prompt = f"""
You are a professional Skill Analysis AI Agent.

Analyze the following resume analysis and identify the candidate's
technical skills and skill levels.

Return ONLY valid JSON.
Do not add markdown.
Do not add ```json.
Do not add explanations outside the JSON.

Use exactly this structure:

{{
    "strong_skills": [],
    "intermediate_skills": [],
    "weak_skills": [],
    "programming_languages": [],
    "frameworks": [],
    "databases": [],
    "ai_ml_skills": [],
    "devops_cloud_skills": [],
    "recommended_skills": []
}}

Resume Analysis:

{resume_analysis}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text