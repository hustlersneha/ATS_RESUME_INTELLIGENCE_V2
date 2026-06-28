from core.ai_matcher import ai_match

resume = """
Python developer with SQL, API and backend experience.
I have worked with Django REST Framework and React.
"""

job = """
We are hiring a frontend developer.
The candidate should have experience with React, JavaScript,
HTML, CSS, API integration and responsive UI development.
"""

result = ai_match(resume, job)

print("\n----- AI ATS REPORT -----")
print("Semantic Score:", result["semantic_score"], "%")
print("Missing Skills:", result["missing_skills"])