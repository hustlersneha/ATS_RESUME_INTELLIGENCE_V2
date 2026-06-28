from sentence_transformers import SentenceTransformer, util
from keybert import KeyBERT
import re

model = SentenceTransformer("all-MiniLM-L6-v2")
kw_model = KeyBERT(model=model)


def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9+#.\n ]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def split_into_chunks(text):
    text = text.replace("•", "\n")
    text = text.replace("-", "\n")
    text = text.replace(":", "\n")
    text = text.replace("/", " ")

    chunks = re.split(r"\n|\.|,", text)

    final_chunks = []

    for chunk in chunks:
        chunk = clean_text(chunk)

        # allow single-word skills also: sql, git, react, flask
        if len(chunk) >= 2 and len(chunk.split()) <= 20:
            final_chunks.append(chunk)

    return final_chunks

def semantic_score(resume_text, job_text):
    resume_embedding = model.encode(
        resume_text,
        convert_to_tensor=True
    )

    job_embedding = model.encode(
        job_text,
        convert_to_tensor=True
    )

    whole_similarity = util.cos_sim(
        resume_embedding,
        job_embedding
    ).item()

    resume_chunks = split_into_chunks(resume_text)
    job_chunks = split_into_chunks(job_text)

    if resume_chunks and job_chunks:
        resume_chunk_embeddings = model.encode(
            resume_chunks,
            convert_to_tensor=True
        )

        job_chunk_embeddings = model.encode(
            job_chunks,
            convert_to_tensor=True
        )

        similarities = util.cos_sim(
            job_chunk_embeddings,
            resume_chunk_embeddings
        )

        chunk_score = similarities.max(dim=1).values.mean().item()

        final_score = (0.6 * whole_similarity) + (0.4 * chunk_score)

    else:
        final_score = whole_similarity

    final_score = max(0, final_score) * 100

    return round(final_score, 2)

def extract_job_requirements(job_text):
    job_text = clean_text(job_text)

    keywords = kw_model.extract_keywords(
        job_text,
        keyphrase_ngram_range=(1, 2),
        stop_words="english",
        top_n=20,
        use_mmr=True,
        diversity=0.4
    )

    bad_words = {
    "developer", "engineer", "senior", "junior",
    "responsibilities", "responsibility",
    "candidate", "hiring", "required", "requirements",
    "skills", "experience", "develop", "using",
    "write", "collaborate", "applications",
    "frontend", "backend", "full", "stack",
    "looking", "good", "strong"
}

    requirements = []

    for phrase, score in keywords:
        phrase = phrase.lower().strip()

        words = phrase.split()

        if any(word in bad_words for word in words):
            continue

        if len(phrase) < 3:
            continue

        requirements.append(phrase)

    return list(dict.fromkeys(requirements))


def find_missing_skills(resume_text, job_text, threshold=0.55):
    resume_chunks = split_into_chunks(resume_text)
    job_requirements = extract_job_requirements(job_text)

    if not resume_chunks or not job_requirements:
        return []

    resume_clean = clean_text(resume_text)

    resume_embeddings = model.encode(
        resume_chunks,
        convert_to_tensor=True
    )

    requirement_embeddings = model.encode(
        job_requirements,
        convert_to_tensor=True
    )

    similarities = util.cos_sim(
        requirement_embeddings,
        resume_embeddings
    )

    missing = []

    for index, skill in enumerate(job_requirements):
        skill = skill.strip().lower()
        best_score = similarities[index].max().item()

        if skill in resume_clean:
            continue

        if best_score < threshold:
            missing.append(skill)

    # remove duplicates and overlapping phrases
    final_missing = []

    for skill in sorted(missing, key=len):
        already_exists = False

        for existing in final_missing:
            if existing in skill or skill in existing:
                already_exists = True
                break

        if not already_exists:
            final_missing.append(skill)

    return final_missing[:8]

def ai_match(resume_text, job_text):
    score = semantic_score(resume_text, job_text)
    missing = find_missing_skills(resume_text, job_text)

    return {
        "semantic_score": score,
        "missing_skills": missing
    }