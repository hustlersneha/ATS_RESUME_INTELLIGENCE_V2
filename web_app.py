import streamlit as st
from core.ai_matcher import ai_match
from core.pdf_parser import extract_text_from_pdf

st.set_page_config(
    page_title="ATS Resume Intelligence",
    layout="centered"
)

st.title("ATS Resume Intelligence")
st.write("AI-powered resume analysis using semantic similarity and Gemini AI")

uploaded_resume = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)

resume_text_input = st.text_area(
    "Or Paste Resume Text",
    height=180
)

job_description = st.text_area(
    "Paste Job Description",
    height=220
)

if st.button("Analyze Resume"):

    resume_text = ""

    if uploaded_resume is not None:
        resume_text = extract_text_from_pdf(uploaded_resume)
    else:
        resume_text = resume_text_input

    if resume_text.strip() == "" or job_description.strip() == "":
        st.warning("Please upload/paste resume and enter job description.")

    else:
        with st.spinner("AI is analyzing your resume..."):
            result = ai_match(resume_text, job_description)

        st.markdown("---")
        st.subheader("ATS Result")

        st.metric(
            "Semantic Matching Score",
            f"{result['semantic_score']}%"
        )

        st.markdown("---")

        st.subheader("Matched Skills")
        if result["matched_skills"]:
            for skill in result["matched_skills"]:
                st.success(skill)
        else:
            st.info("No matched skills found.")

        st.subheader("Missing Skills")
        if result["missing_skills"]:
            for skill in result["missing_skills"]:
                st.error(skill)
        else:
            st.success("No major missing skills found.")

        st.subheader("Strengths")
        for strength in result["strengths"]:
            st.write("✅", strength)

        st.subheader("Weaknesses")
        for weakness in result["weaknesses"]:
            st.write("⚠️", weakness)

        st.subheader("Suggestions")
        for suggestion in result["suggestions"]:
            st.write("💡", suggestion)

        with st.expander("Extracted Resume Text"):
            st.write(resume_text)