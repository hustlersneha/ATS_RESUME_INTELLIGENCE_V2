from core.roles import ROLE_SKILLS, detect_role

def get_match_score(resume_tokens, job_text):

    role = detect_role(job_text)

    if role is None:
        return 0, [], ["role not found"]

    required_skills = ROLE_SKILLS[role]

    resume_set = set(resume_tokens)

    matched = []
    missing = []

    score = 0

    for skill in required_skills:
        if skill in resume_set:
            matched.append(skill)
            score += 1
        else:
            missing.append(skill)

    final_score = (score / len(required_skills)) * 100

    return round(final_score, 2), matched, missing