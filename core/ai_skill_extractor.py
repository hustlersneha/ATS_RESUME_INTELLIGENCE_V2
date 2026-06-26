def extract_skills(text):
    text = text.lower()

    known_skills = [
        "python", "java", "javascript", "react", "django", "flask",
        "sql", "html", "css", "api", "backend", "frontend",
        "machine learning", "git", "docker"
    ]

    found = []

    for skill in known_skills:
        if skill in text:
            found.append(skill)

    return list(set(found))