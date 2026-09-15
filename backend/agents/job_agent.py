import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)


def match_jobs(
    resume_analysis: str,
    skill_analysis: str,
    career_analysis: str
):

    prompt = f"""
You are a professional Job Matching AI Agent.

Analyze the candidate's resume, skills, and career recommendations.

Recommend suitable job roles or internship roles based on the
candidate's profile.

Return ONLY valid JSON.
Do not add markdown.
Do not add ```json.
Do not add explanations outside the JSON.

Use exactly this structure:

{{
    "recommended_roles": [
        {{
            "job_title": "",
            "job_type": "Internship",
            "match_percentage": 0,
            "matching_skills": [],
            "missing_skills": [],
            "reason": ""
        }}
    ],
    "top_role": "",
    "application_advice": []
}}

Important:
- Recommend up to 5 suitable roles.
- Do not invent specific companies.
- Do not invent specific job vacancies.
- Recommend role types only.
- match_percentage is an AI-generated estimate.
- Focus on realistic roles for the candidate.
- Consider both technical skills and career direction.

Resume Analysis:

{resume_analysis}

Skill Analysis:

{skill_analysis}

Career Analysis:

{career_analysis}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text