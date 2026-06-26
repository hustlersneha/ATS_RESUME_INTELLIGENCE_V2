import streamlit as st
from core.ai_matcher import ai_match

# Page config
st.set_page_config(
    page_title="ATS Resume Intelligence",
    layout="centered"
)

# Title
st.title(" ATS Resume Intelligence System V2")
st.write("Analyze Resume vs Job Description using AI + NLP")

# Inputs
resume = st.text_area("Paste Resume", height=200)
job = st.text_area(" Paste Job Description", height=200)

# Button
if st.button(" Analyze Resume"):

    if resume.strip() == "" or job.strip() == "":
        st.warning("Please fill both Resume and Job Description")
    else:
        result = ai_match(resume, job)

        st.markdown("---")
        st.subheader(" ATS Results")

        # Metrics
        col1, col2, col3 = st.columns(3)

        col1.metric("Skill Score", f"{result['skill_score']}%")
        col2.metric("Semantic Score", f"{result['semantic_score']}%")
        col3.metric("Final Score", f"{result['final_score']}%")

        st.markdown("---")

        # Matched Skills
        st.subheader("✔ Matched Skills")
        st.success(", ".join(result["matched"]) if result["matched"] else "No matches found")

        # Missing Skills
        st.subheader(" Missing Skills")
        st.error(", ".join(result["missing"]) if result["missing"] else "None ")