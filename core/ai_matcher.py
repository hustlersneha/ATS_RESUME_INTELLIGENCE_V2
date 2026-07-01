from sentence_transformers import SentenceTransformer, util
from core.gemini_matcher import analyze_resume
import re

model = SentenceTransformer("all-MiniLM-L6-v2")


def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def get_semantic_score(resume_text, job_text):
    resume_text = clean_text(resume_text)
    job_text = clean_text(job_text)

    resume_embedding = model.encode(resume_text, convert_to_tensor=True)
    job_embedding = model.encode(job_text, convert_to_tensor=True)

    similarity = util.cos_sim(resume_embedding, job_embedding).item()
    score = max(0, similarity) * 100

    return round(score, 2)


def ai_match(resume_text, job_text):
    semantic_score = get_semantic_score(resume_text, job_text)

    ai_analysis = analyze_resume(
        resume=resume_text,
        job_description=job_text
    )

    return {
        "semantic_score": semantic_score,
        "matched_skills": ai_analysis.get("matched_skills", []),
        "missing_skills": ai_analysis.get("missing_skills", []),
        "strengths": ai_analysis.get("strengths", []),
        "weaknesses": ai_analysis.get("weaknesses", []),
        "suggestions": ai_analysis.get("suggestions", [])
    }