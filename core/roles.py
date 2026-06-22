ROLE_SKILLS = {
    "golang developer": [
        "golang", "backend", "api", "database", "sql", "system"
    ],

    "python developer": [
        "python", "django", "flask", "api", "sql", "backend"
    ],

    "data analyst": [
        "excel", "sql", "powerbi", "data", "analysis"
    ],

    "machine learning engineer": [
        "python", "machine", "learning", "ai", "data", "model"
    ]
}
def detect_role(job_text):
    job_text = job_text.lower()

    for role in ROLE_SKILLS.keys():
        if role in job_text:
            return role

    return None