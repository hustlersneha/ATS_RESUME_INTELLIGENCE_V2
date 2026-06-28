from sentence_transformers import SentenceTransformer, util
import re

model = SentenceTransformer("all-MiniLM-L6-v2")


def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def get_semantic_score(resume_text, job_text):
    resume_text = clean_text(resume_text)
    job_text = clean_text(job_text)

    resume_embedding = model.encode(
        resume_text,
        convert_to_tensor=True
    )

    job_embedding = model.encode(
        job_text,
        convert_to_tensor=True
    )

    similarity = util.cos_sim(
        resume_embedding,
        job_embedding
    ).item()

    score = max(0, similarity) * 100

    return round(score, 2)


def ai_match(resume_text, job_text):
    semantic_score = get_semantic_score(resume_text, job_text)

    return {
        "semantic_score": semantic_score
    }