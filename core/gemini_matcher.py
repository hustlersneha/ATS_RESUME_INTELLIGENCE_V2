import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def analyze_resume(resume, job_description):

    prompt = f"""
You are an expert Applicant Tracking System.

Compare the resume with the job description.

Do NOT compare keywords.

Understand meaning.

Return ONLY valid JSON.

Required format:

{{
"matched_skills": [],
"missing_skills": [],
"strengths": [],
"weaknesses": [],
"suggestions": []
}}

Resume:

{resume}

Job Description:

{job_description}
"""

    response = model.generate_content(prompt)

    text = response.text

    text = text.replace("```json", "")
    text = text.replace("```", "")

    return json.loads(text)