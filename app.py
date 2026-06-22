from core.preprocess import preprocess
from core.matcher import get_match_score

resume = "Python SQL API experience"
job = "Golang Developer required with backend API and database knowledge"

resume_tokens = preprocess(resume)

score, matched, missing = get_match_score(resume_tokens, job)

print("Score:", score, "%")
print("Matched:", matched)
print("Missing:", missing)