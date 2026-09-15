from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import asyncio

from services.resume_service import extract_text_from_pdf
from agents.resume_graph import resume_graph


router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):

    # ==========================================
    # 1. VALIDATE FILE
    # ==========================================

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file selected"
        )

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    # ==========================================
    # 2. CREATE UPLOAD FOLDER
    # ==========================================

    upload_folder = "uploads"
    os.makedirs(upload_folder, exist_ok=True)

    # Use only the filename, not a supplied path
    safe_filename = os.path.basename(file.filename)

    file_path = os.path.join(
        upload_folder,
        safe_filename
    )

    try:

        # ==========================================
        # 3. SAVE PDF
        # ==========================================

        file_content = await file.read()

        if not file_content:
            raise HTTPException(
                status_code=400,
                detail="The uploaded PDF is empty"
            )

        # 10 MB limit
        max_file_size = 10 * 1024 * 1024

        if len(file_content) > max_file_size:
            raise HTTPException(
                status_code=400,
                detail="PDF must be smaller than 10 MB"
            )

        with open(file_path, "wb") as buffer:
            buffer.write(file_content)

        # ==========================================
        # 4. EXTRACT TEXT
        # ==========================================

        extracted_text = extract_text_from_pdf(
            file_path
        )

        if (
            not extracted_text
            or not extracted_text.strip()
        ):
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from PDF"
            )

        # ==========================================
        # 5. RUN CAREPLANIX AI WORKFLOW
        # ==========================================

        max_retries = 3
        result = None

        for attempt in range(max_retries):

            try:

                print(
                    f"CarePlanix AI analysis attempt "
                    f"{attempt + 1}/{max_retries}"
                )

                result = resume_graph.invoke({
                    "resume_text": extracted_text,
                    "analysis": "",
                    "skill_analysis": "",
                    "career_analysis": "",
                    "skill_gap_analysis": "",
                    "roadmap": "",
                    "job_matches": ""
                })

                # Successful analysis
                break

            except Exception as e:

                error_message = str(e)

                print(
                    f"AI attempt {attempt + 1} failed:",
                    error_message
                )

                # ==================================
                # TEMPORARY AI PROVIDER ERROR
                # ==================================

                temporary_error = (
                    "503" in error_message
                    or "UNAVAILABLE" in error_message.upper()
                    or "HIGH DEMAND" in error_message.upper()
                )

                if temporary_error:

                    # Retry if attempts remain
                    if attempt < max_retries - 1:

                        wait_time = 3 * (
                            attempt + 1
                        )

                        print(
                            f"AI service unavailable. "
                            f"Retrying in {wait_time} seconds..."
                        )

                        await asyncio.sleep(
                            wait_time
                        )

                        continue

                    # All retries failed
                    raise HTTPException(
                        status_code=503,
                        detail=(
                            "CarePlanix AI is currently "
                            "experiencing high demand. "
                            "Please wait a few moments "
                            "and try again."
                        )
                    )

                # ==================================
                # OTHER AI ERRORS
                # ==================================

                raise

        # ==========================================
        # 6. CHECK RESULT
        # ==========================================

        if result is None:
            raise HTTPException(
                status_code=500,
                detail=(
                    "CarePlanix AI could not "
                    "complete the resume analysis."
                )
            )

        # ==========================================
        # 7. RETURN COMPLETE RESULT
        # ==========================================

        return {
            "filename": safe_filename,

            "text_preview":
                extracted_text[:1000],

            "analysis":
                result.get(
                    "analysis",
                    ""
                ),

            "skill_analysis":
                result.get(
                    "skill_analysis",
                    ""
                ),

            "career_analysis":
                result.get(
                    "career_analysis",
                    ""
                ),

            "skill_gap_analysis":
                result.get(
                    "skill_gap_analysis",
                    ""
                ),

            "roadmap":
                result.get(
                    "roadmap",
                    ""
                ),

            "job_matches":
                result.get(
                    "job_matches",
                    ""
                )
        }

    # ==========================================
    # FASTAPI ERRORS
    # ==========================================

    except HTTPException:
        raise

    # ==========================================
    # UNEXPECTED ERRORS
    # ==========================================

    except Exception as e:

        print(
            "Resume analysis error:",
            str(e)
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Resume analysis failed: "
                + str(e)
            )
        )

    # ==========================================
    # CLEANUP
    # ==========================================

    finally:

        # Delete uploaded CV after analysis.
        # This avoids permanently storing
        # users' resumes on the server.

        try:
            if os.path.exists(file_path):
                os.remove(file_path)

        except Exception as cleanup_error:
            print(
                "Could not remove uploaded file:",
                cleanup_error
            )