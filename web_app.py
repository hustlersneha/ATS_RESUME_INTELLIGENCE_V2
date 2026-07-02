import streamlit as st
from core.ai_matcher import ai_match
from core.pdf_parser import extract_text_from_pdf

st.set_page_config(
    page_title="ATS Resume Intelligence",
    layout="wide"
)

st.markdown(
    """
    <style>
    .main-title {
        font-size: 42px;
        font-weight: 800;
        text-align: center;
        color: #1f2937;
        margin-bottom: 5px;
    }

    .sub-title {
        text-align: center;
        color: #6b7280;
        font-size: 18px;
        margin-bottom: 30px;
    }

    .score-card {
        background: linear-gradient(135deg, #2563eb, #9333ea);
        padding: 30px;
        border-radius: 18px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }

    .score-number {
        font-size: 56px;
        font-weight: 800;
    }

    .section-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 14px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 18px;
    }

    .badge-green {
        display: inline-block;
        background-color: #dcfce7;
        color: #166534;
        padding: 8px 12px;
        border-radius: 20px;
        margin: 5px;
        font-weight: 600;
        font-size: 14px;
    }

    .badge-red {
        display: inline-block;
        background-color: #fee2e2;
        color: #991b1b;
        padding: 8px 12px;
        border-radius: 20px;
        margin: 5px;
        font-weight: 600;
        font-size: 14px;
    }

    .insight-box {
        background-color: #f9fafb;
        padding: 12px 15px;
        border-left: 5px solid #2563eb;
        border-radius: 10px;
        margin-bottom: 10px;
        color: #374151;
    }

    .warning-box {
        background-color: #fff7ed;
        padding: 12px 15px;
        border-left: 5px solid #f97316;
        border-radius: 10px;
        margin-bottom: 10px;
        color: #7c2d12;
    }

    .suggestion-box {
        background-color: #f0fdf4;
        padding: 12px 15px;
        border-left: 5px solid #22c55e;
        border-radius: 10px;
        margin-bottom: 10px;
        color: #14532d;
    }
    </style>
    """,
    unsafe_allow_html=True
)


def show_badges(items, badge_class):
    if items:
        html = ""
        for item in items:
            html += f"<span class='{badge_class}'>{item}</span>"
        st.markdown(html, unsafe_allow_html=True)
    else:
        st.info("No data available.")


def show_list(items, box_class):
    if items:
        for item in items:
            st.markdown(
                f"<div class='{box_class}'>{item}</div>",
                unsafe_allow_html=True
            )
    else:
        st.info("No data available.")


st.markdown("<div class='main-title'>ATS Resume Intelligence</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='sub-title'>AI-powered resume analysis using Semantic Similarity + Gemini AI</div>",
    unsafe_allow_html=True
)

left_col, right_col = st.columns([1, 1])

with left_col:
    st.markdown("###  Resume Input")

    uploaded_resume = st.file_uploader(
        "Upload Resume PDF",
        type=["pdf"]
    )

    resume_text_input = st.text_area(
        "Or Paste Resume Text",
        height=250
    )

with right_col:
    st.markdown("###  Job Description")

    job_description = st.text_area(
        "Paste Job Description",
        height=345
    )

analyze_btn = st.button("Analyze Resume", use_container_width=True)

if analyze_btn:

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

        score = result.get("semantic_score", 0)

        score_col, summary_col = st.columns([1, 2])

        with score_col:
            st.markdown(
                f"""
                <div class="score-card">
                    <div>Semantic Match Score</div>
                    <div class="score-number">{score}%</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.progress(min(int(score), 100))

        with summary_col:
            st.markdown("###  Resume Analysis Summary")

            if score >= 80:
                st.success("Strong semantic match for this job description.")
            elif score >= 60:
                st.info("Good match, but there are some improvement areas.")
            elif score >= 40:
                st.warning("Moderate match. Resume needs improvement for this role.")
            else:
                st.error("Low match. Resume is not strongly aligned with this job.")

        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<div class='section-card'>", unsafe_allow_html=True)
            st.subheader(" Matched Skills")
            show_badges(result.get("matched_skills", []), "badge-green")
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='section-card'>", unsafe_allow_html=True)
            st.subheader(" Missing Skills")
            show_badges(result.get("missing_skills", []), "badge-red")
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")

        col3, col4 = st.columns(2)

        with col3:
            st.subheader(" Strengths")
            show_list(result.get("strengths", []), "insight-box")

        with col4:
            st.subheader(" Weaknesses")
            show_list(result.get("weaknesses", []), "warning-box")

        st.markdown("---")

        st.subheader(" Resume Improvement Suggestions")
        show_list(result.get("suggestions", []), "suggestion-box")

        with st.expander(" View Extracted Resume Text"):
            st.write(resume_text)