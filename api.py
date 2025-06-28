from fastapi import APIRouter, UploadFile, File
from app.utils.parser import extract_text_from_resume
import os
import re


from app.utils.parser import (
    extract_text_from_resume,
    detect_sections,
    match_keywords,
    score_resume,
    generate_feedback
)


router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload-resume/")
async def upload_resume(file: UploadFile = File(...)):
    contents = await file.read()

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(contents)

    # Extract text using our utility
    extracted_text = extract_text_from_resume(file_path)

    return {"filename": file.filename, "text_snippet": extracted_text[:500]}


from fastapi import APIRouter, UploadFile, File, Form
from app.utils.parser import extract_text_from_resume, detect_sections, match_keywords
import os

router = APIRouter()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/analyze-resume/")
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    contents = await file.read()
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(contents)

    text = extract_text_from_resume(file_path)
    sections_result = detect_sections(text)
    matched_keywords = match_keywords(text, job_description)

    # Count keywords from job description
    job_keywords = set(re.findall(r"\b\w+\b", job_description.lower()))
    scoring = score_resume(sections_result, matched_keywords, len(job_keywords))
    feedback = generate_feedback(
        missing_sections=sections_result["missing_sections"],
        matched_keywords=matched_keywords,
        job_keywords=job_keywords
    )

    return {
        "filename": file.filename,
        "score": scoring,
        "sections": sections_result,
        "matched_keywords": matched_keywords,
        "text_snippet": text[:500],
        "feedback":feedback
    }


