import streamlit as st
from core.ai_matcher import ai_match
from core.pdf_parser import extract_text_from_pdf

st.set_page_config(
    page_title="ATS Resume Intelligence",
    layout="centered"
)

st.title("ATS Resume Intelligence")
st.write("AI-powered resume analysis using semantic similarity")

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
        with st.spinner("Analyzing resume..."):
            result = ai_match(resume_text, job_description)

        st.markdown("---")
        st.subheader("ATS Result")

        st.metric(
            "Semantic Matching Score",
            f"{result['semantic_score']}%"
        )

        with st.expander("Extracted Resume Text"):
            st.write(resume_text)