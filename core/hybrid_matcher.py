from core.preprocess import preprocess
from core.matcher import get_match_score
from core.semantic_matcher import semantic_score


def hybrid_score(resume_text, job_text):

    # Rule-based ATS
    resume_tokens = preprocess(resume_text)

    skill_score, matched, missing = get_match_score(
        resume_tokens,
        job_text
    )

    # AI ATS
    ai_score = semantic_score(
        resume_text,
        job_text
    )

    # Final Hybrid Score
    final_score = (
        0.4 * skill_score
        +
        0.6 * ai_score
    )

    return {
        "skill_score": round(skill_score, 2),
        "semantic_score": round(ai_score, 2),
        "final_score": round(final_score, 2),
        "matched": matched,
        "missing": missing
    }