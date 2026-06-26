from core.ai_skill_extractor import extract_skills
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')


def ai_match(resume_text, job_text):

    # STEP 1: Extract skills
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_text)

    resume_set = set(skill.lower().strip() for skill in resume_skills)
    job_set = set(skill.lower().strip() for skill in job_skills)

    # STEP 2: Skill matching (normalized)
    matched = list(resume_set & job_set)
    missing = list(job_set - resume_set)

    # STEP 3: Semantic similarity
    emb1 = model.encode(resume_text, convert_to_tensor=True)
    emb2 = model.encode(job_text, convert_to_tensor=True)

    cos_sim = util.pytorch_cos_sim(emb1, emb2).item()

    # normalize cosine similarity (important fix)
    semantic_score = max(0, cos_sim) * 100

    # STEP 4: Skill score
    skill_score = (len(matched) / len(job_set)) * 100 if job_set else 0

    # STEP 5: Weighted final score
    final_score = 0.6 * semantic_score + 0.4 * skill_score

    return {
        "semantic_score": round(semantic_score, 2),
        "skill_score": round(skill_score, 2),
        "final_score": round(final_score, 2),
        "matched": matched,
        "missing": missing,
        "resume_skills": list(resume_set),
        "job_skills": list(job_set)
    }