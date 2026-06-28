import streamlit as st
from core.ai_matcher import ai_match

st.set_page_config(
    page_title="AI ATS Resume Matcher",
    layout="centered"
)

st.title("AI ATS Resume Matcher")
st.write("Semantic Resume Matching using AI")

resume = st.text_area("Paste Resume", height=250)
job = st.text_area("Paste Job Description", height=250)

if st.button("Analyze Resume"):

    if resume.strip() == "" or job.strip() == "":
        st.warning("Please enter both resume and job description.")

    else:
        with st.spinner("AI is analyzing your resume..."):
            result = ai_match(resume, job)

        st.markdown("---")
        st.subheader("ATS Result")

        st.metric(
            "Semantic Matching Score",
            f"{result['semantic_score']}%"
        )

        st.markdown("---")
        st.subheader("AI Suggested Missing Skills")

        if result["missing_skills"]:
            for skill in result["missing_skills"]:
                st.error(skill)
        else:
            st.success("No major missing skills found.")