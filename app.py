from core.hybrid_matcher import hybrid_score

resume = """
Python developer with SQL, API and backend experience.
"""

job = """
We are hiring a Golang Developer.
"""

result = hybrid_score(resume, job)

print("\n----- ATS REPORT -----")
print("Skill Score:", result["skill_score"], "%")
print("Semantic Score:", result["semantic_score"], "%")
print("Final Score:", result["final_score"], "%")
print("Matched Skills:", result["matched"])
print("Missing Skills:", result["missing"])