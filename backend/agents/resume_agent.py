import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)


def analyze_resume(resume_text: str):

    prompt = f"""
You are a professional Resume Analysis AI Agent.

Analyze the following resume carefully.

Return ONLY valid JSON.
Do not add markdown.
Do not add ```json.
Do not add explanations outside the JSON.

The JSON must have this structure:

{{
    "personal_information": {{
        "name": "",
        "email": "",
        "phone": "",
        "location": ""
    }},
    "education": [],
    "technical_skills": [],
    "projects": [],
    "experience": [],
    "career_interests": [],
    "skill_level": {{
        "programming": "",
        "web_development": "",
        "database": "",
        "ai_ml": "",
        "other": ""
    }},
    "weak_skills": [],
    "recommended_skills": [],
    "career_recommendations": []
}}

Resume:

{resume_text}
"""

    response = client.models.generate_content(
       model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text