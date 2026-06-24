from core.semantic_matcher import semantic_score

resume = """
Python developer with backend API experience.
Worked with SQL and Django.
"""

job = """
Software engineer required with backend development experience.
"""

score = semantic_score(resume, job)

print("Semantic Match Score:", score, "%") 
