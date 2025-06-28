import os
import re
from pdfminer.high_level import extract_text
from docx import Document

SECTION_HEADERS = [
    "experience", "education", "projects", "skills",
    "certifications", "interests", "objective", "summary"
]

def extract_text_from_resume(file_path: str) -> str:
    if file_path.endswith(".pdf"):
        return extract_text(file_path)
    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        return "Unsupported file type."

def detect_sections(text: str) -> dict:
    found = []
    missing = []
    for section in SECTION_HEADERS:
        pattern = r"\b" + re.escape(section) + r"\b"
        if re.search(pattern, text, re.IGNORECASE):
            found.append(section)
        else:
            missing.append(section)
    return {"found_sections": found, "missing_sections": missing}

def match_keywords(text: str, job_description: str) -> list:
    text = text.lower()
    job_description = job_description.lower()
    
    job_keywords = set(re.findall(r"\b\w+\b", job_description))
    resume_words = set(re.findall(r"\b\w+\b", text))

    matched = list(resume_words.intersection(job_keywords))
    return matched


def score_resume(sections_result, matched_keywords, total_keywords):
    found_sections = sections_result["found_sections"]
    missing_sections = sections_result["missing_sections"]

    # Handle edge cases
    total_sections = len(found_sections) + len(missing_sections)
    section_score = len(found_sections) / total_sections if total_sections > 0 else 0
    keyword_score = len(matched_keywords) / total_keywords if total_keywords > 0 else 0

    # You can tune these weights
    section_weight = 0.3
    keyword_weight = 0.7

    final_score = (section_score * section_weight) + (keyword_score * keyword_weight)

    # More detailed rating tiers
    if final_score >= 0.9:
        rating = "Excellent"
    elif final_score >= 0.75:
        rating = "Very Good"
    elif final_score >= 0.6:
        rating = "Good"
    elif final_score >= 0.45:
        rating = "Needs Improvement"
    else:
        rating = "Poor"

    return {
        "section_score": round(section_score * 100, 2),
        "keyword_score": round(keyword_score * 100, 2),
        "score": round(final_score * 100, 2),
        "rating": rating
    }






def generate_feedback(missing_sections: list, matched_keywords: list, job_keywords: set) -> list:
    feedback = []

    # 1. Missing sections
    if missing_sections:
        feedback.append(
            f"Your resume is missing the following key sections: {', '.join(missing_sections)}. "
            f"Consider adding them to make your resume more complete."
        )
    else:
        feedback.append("Great! Your resume includes all standard sections.")

    # 2. Matched vs Unmatched keywords
    unmatched_keywords = job_keywords - set(matched_keywords)
    if unmatched_keywords:
        feedback.append(
            f"Consider including the following job-specific terms in your resume: {', '.join(unmatched_keywords)}. "
            f"This could help your resume pass automated screenings."
        )
    else:
        feedback.append("Nice work! Your resume already includes all the relevant keywords from the job description.")

    # 3. General tips (optional)
    feedback.append(
        "Make sure your resume uses action verbs, highlights achievements with metrics, and is tailored to the specific job."
    )

    return feedback


