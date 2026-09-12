from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(
    prefix="/profile",
    tags=["Profile"]
)


class ProfileRequest(BaseModel):
    name: str
    education: str
    university: str
    skills: list[str]
    career_goal: str
    experience: str = ""
    projects: list[str] = []
    preferred_job_role: str


@router.post("/")
def create_profile(data: ProfileRequest):

    from main import db

    profile = {
        "name": data.name,
        "education": data.education,
        "university": data.university,
        "skills": data.skills,
        "career_goal": data.career_goal,
        "experience": data.experience,
        "projects": data.projects,
        "preferred_job_role": data.preferred_job_role
    }

    result = db.profiles.insert_one(profile)

    return {
        "message": "Profile created successfully",
        "profile_id": str(result.inserted_id)
    }
@router.get("/{profile_id}")
def get_profile(profile_id: str):

    from main import db
    from bson import ObjectId

    profile = db.profiles.find_one({
        "_id": ObjectId(profile_id)
    })

    if not profile:
        return {
            "message": "Profile not found"
        }

    profile["_id"] = str(profile["_id"])

    return profile
@router.put("/{profile_id}")
def update_profile(profile_id: str, data: ProfileRequest):

    from main import db
    from bson import ObjectId

    updated_profile = {
        "name": data.name,
        "education": data.education,
        "university": data.university,
        "skills": data.skills,
        "career_goal": data.career_goal,
        "experience": data.experience,
        "projects": data.projects,
        "preferred_job_role": data.preferred_job_role
    }

    result = db.profiles.update_one(
        {"_id": ObjectId(profile_id)},
        {"$set": updated_profile}
    )

    if result.matched_count == 0:
        return {
            "message": "Profile not found"
        }

    return {
        "message": "Profile updated successfully"
    }