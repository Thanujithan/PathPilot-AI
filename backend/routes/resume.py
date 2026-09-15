from fastapi import APIRouter, UploadFile, File, HTTPException
import os

from services.resume_service import extract_text_from_pdf
from agents.resume_graph import resume_graph


router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):

    # Check PDF
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    upload_folder = "uploads"
    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(
        upload_folder,
        file.filename
    )

    # Save PDF
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Extract text
    extracted_text = extract_text_from_pdf(file_path)

    if not extracted_text.strip():
        raise HTTPException(
            status_code=400,
            detail="Could not extract text from PDF"
        )

    # Run LangGraph Resume Workflow
    result = resume_graph.invoke({
        "resume_text": extracted_text,
        "analysis": "",
        "skill_analysis": "",
        "career_analysis": "",
        "skill_gap_analysis": "",
        "roadmap": "",
        "job_matches": ""
    })

    analysis = result["analysis"]

    return {
        "filename": file.filename,
        "text_preview": extracted_text[:1000],
        "analysis": result["analysis"],
        "skill_analysis": result["skill_analysis"],
        "career_analysis": result["career_analysis"],
        "job_matches": result["job_matches"]
    }