import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)


def analyze_skill_gaps(skill_analysis: str, career_analysis: str):

    prompt = f"""
You are a professional Skill Gap Analysis AI Agent.

Analyze the candidate's current skills and recommended career path.

Identify the skills the candidate is missing or needs to improve
to become job-ready for the target career.

Return ONLY valid JSON.
Do not add markdown.
Do not add ```json.
Do not add explanations outside the JSON.

Use exactly this structure:

{{
    "target_career": "",
    "skill_gaps": [
        {{
            "skill": "",
            "current_level": "",
            "required_level": "",
            "priority": "",
            "reason": ""
        }}
    ],
    "soft_skill_gaps": [],
    "learning_order": [],
    "job_readiness_percentage": 0
}}

Important:
- job_readiness_percentage is an AI-generated estimate.
- Do not claim it is a formal professional assessment.
- Use realistic skill levels such as Beginner, Intermediate, Advanced.
- Priority should be High, Medium, or Low.
- Recommend realistic skills based on the target career.

Current Skill Analysis:

{skill_analysis}

Career Analysis:

{career_analysis}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text