from fastapi import APIRouter, UploadFile, File
import os

from services.resume_service import extract_text_from_pdf

router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):

    upload_folder = "uploads"

    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(upload_folder, file.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    extracted_text = extract_text_from_pdf(file_path)

    return {
        "filename": file.filename,
        "text_preview": extracted_text[:1000]
    }