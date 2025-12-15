import streamlit as st
from src.helper import extract_text_from_pdf, ask_gemini
from src.job_api import fetch_linkedin_jobs, fetch_naukri_jobs

st.set_page_config(page_title="JOB Recommender", layout="wide")
st.title("AI Job Recommender")

st.markdown(
    "Upload your resume and get job recommendations based on your skills and experience from Naukri and LinkedIn"
)

uploaded_file = st.file_uploader("Upload Your Resume (PDF)", type=["pdf"])

if uploaded_file:
    with st.spinner("Extracting text from resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)

    with st.spinner("Summarizing your resume..."):
        summary = ask_gemini(
            f"Summarize this resume highlighting skills, education and experience:\n\n{resume_text}",
            max_tokens=500
        )

    with st.spinner("Finding skill gaps..."):
        skill_gaps = ask_gemini(
            f"Analyze this resume and highlight missing skills, certifications, or experience needed:\n\n{resume_text}",
            max_tokens=500
        )

    with st.spinner("Creating future roadmap..."):
        roadmap = ask_gemini(
            f"Based on this resume, suggest a future career roadmap:\n\n{resume_text}",
            max_tokens=400
        )

    st.markdown("---")
    st.header("📑 Resume Summary")
    st.markdown(
        f"<div style='background-color:#1e1e1e;padding:15px;border-radius:10px;color:white;'>{summary}</div>",
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.header("🛠️ Skill Gaps & Missing Areas")
    st.markdown(
        f"<div style='background-color:#1e1e1e;padding:15px;border-radius:10px;color:white;'>{skill_gaps}</div>",
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.header("🚀 Future Roadmap")
    st.markdown(
        f"<div style='background-color:#1e1e1e;padding:15px;border-radius:10px;color:white;'>{roadmap}</div>",
        unsafe_allow_html=True
    )

    st.success("✅ Analysis Completed Successfully!")

    if st.button("Get Job Recommendation"):
        with st.spinner("Generating job keywords..."):
            keywords = ask_gemini(
                f"Based on this resume summary, suggest best job titles and keywords. "
                f"Give comma-separated list only.\n\n{summary}",
                max_tokens=100
            )

        search_keywords_clean = keywords.replace("\n", "").strip()

        st.header("💼 Top LinkedIn Jobs")
        st.success(f"Extracted Job Keywords: {search_keywords_clean}")

        with st.spinner("Fetching jobs from LinkedIn and Naukri..."):
            linkedin_jobs = fetch_linkedin_jobs(search_keywords_clean, rows=60)
            naukri_jobs = fetch_naukri_jobs(search_keywords_clean, rows=60)

        if linkedin_jobs:
            for job in linkedin_jobs:
                st.markdown(f"**{job.get('title')}** at *{job.get('companyName')}*")
                st.markdown(f"- 📍 {job.get('location')}")
                st.markdown(f"- 🔗 [View Job]({job.get('link')})")
                st.markdown("---")
        else:
            st.warning("No LinkedIn jobs found.")

        st.header("💼 Top Naukri Jobs (India)")
        if naukri_jobs:
            for job in naukri_jobs:
                st.markdown(f"**{job.get('title')}** at *{job.get('companyName')}*")
                st.markdown(f"- 📍 {job.get('location')}")
                st.markdown(f"- 🔗 [View Job]({job.get('url')})")
                st.markdown("---")
        else:
            st.warning("No Naukri jobs found.")
