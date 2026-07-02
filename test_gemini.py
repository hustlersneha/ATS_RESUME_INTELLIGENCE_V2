from core.gemini_matcher import analyze_resume

resume = """
Python developer with Django, React, SQL, REST API and Git experience.
"""

job = """
We need a Python full stack developer with Django, React, SQL, REST API, Docker and AWS.
"""

result = analyze_resume(resume, job)

print(result)