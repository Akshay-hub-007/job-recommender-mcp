import streamlit as st
from src.helper import extract_text_from_pdf, ask_gemini
from src.job_api import fetch_linkedin_jobs, fetch_naukri_jobs

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="AI Job Recommender",
    page_icon="💼",
    layout="wide"
)

# ---------------- Custom CSS ----------------
st.markdown("""
<style>
.card {
    background-color: #FFFFFF;
    padding: 18px;
    border-radius: 12px;
    margin-bottom: 15px;
}
.job-card {
    background-color: #111827;
    padding: 16px;
    border-radius: 10px;
    margin-bottom: 12px;
}
.tag {
    display: inline-block;
    background-color: #2563eb;
    padding: 4px 10px;
    border-radius: 20px;
    margin: 4px;
    font-size: 12px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- Sidebar ----------------
with st.sidebar:
    st.title("📄 Resume Upload")
    uploaded_file = st.file_uploader(
        "Upload Resume (PDF only)",
        type=["pdf"]
    )
    st.info("AI-powered resume analysis & job matching")

# ---------------- Main Title ----------------
st.title("💼 AI Job Recommender")
st.caption("Upload your resume → Get insights → Find jobs from LinkedIn & Naukri")

# ---------------- Resume Processing ----------------
if uploaded_file:
    with st.spinner("🔍 Extracting resume text..."):
        resume_text = extract_text_from_pdf(uploaded_file)

    with st.spinner("🧠 Analyzing resume..."):
        summary = ask_gemini(
            f"""
You are an experienced technical recruiter.

Summarize the resume below in clear bullet points with:
- Core Skills
- Education
- Work Experience
- Tools & Technologies

Resume:
{resume_text}
""",
            max_tokens=500
        )

    with st.spinner("🛠 Identifying skill gaps..."):
        skill_gaps = ask_gemini(
            f"""
You are a career mentor.

Analyze the resume and list:
- Missing skills
- Certifications needed
- Experience gaps
- Improvement suggestions

Resume:
{resume_text}
""",
            max_tokens=500
        )

    with st.spinner("🚀 Building career roadmap..."):
        roadmap = ask_gemini(
            f"""
You are a senior career advisor.

Create a 6–12 month roadmap including:
- Skills
- Certifications
- Projects
- Job roles

Resume:
{resume_text}
""",
            max_tokens=400
        )

    # ---------------- Results ----------------
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📑 Resume Summary")
        st.markdown(f"<div class='card'>{summary}</div>", unsafe_allow_html=True)

    with col2:
        st.subheader("🛠 Skill Gaps")
        print(skill_gaps)
        st.markdown(f"<div class='card'>{skill_gaps}</div>", unsafe_allow_html=True)

    st.subheader("🚀 Career Roadmap")
    st.markdown(f"<div>{roadmap}</div>", unsafe_allow_html=True)

    st.success("✅ Resume analysis completed!")

    # ---------------- Job Recommendation ----------------
    if st.button("🔍 Get Job Recommendations"):
        with st.spinner("📌 Generating job keywords..."):
            keywords = ask_gemini(
                f"""
Extract best job titles and keywords from below summary.
Return only comma-separated values.

Summary:
{summary}
""",
                max_tokens=100
            )

        search_keywords = keywords.replace("\n", "").strip()
        st.success(f"🔑 Keywords: {search_keywords}")

        with st.spinner("🌐 Fetching jobs..."):
            linkedin_jobs = fetch_linkedin_jobs(search_keywords, rows=40)
            naukri_jobs = fetch_naukri_jobs(search_keywords, rows=40)

        # ---------------- LinkedIn Jobs ----------------
        st.subheader("💼 LinkedIn Jobs")
        if linkedin_jobs:
            for job in linkedin_jobs:
                st.markdown(f"""
                <div class="job-card">
                    <b>{job.get('title')}</b><br>
                    {job.get('companyName')}<br>
                    📍 {job.get('location')}<br>
                    🔗 <a href="{job.get('link')}" target="_blank">View Job</a>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No LinkedIn jobs found.")

        # ---------------- Naukri Jobs ----------------
        st.subheader("💼 Naukri Jobs (India)")
        if naukri_jobs:
            for job in naukri_jobs:
                st.markdown(f"""
                <div class="job-card">
                    <b>{job.get('title')}</b><br>
                    {job.get('companyName')}<br>
                    📍 {job.get('location')}<br>
                    🔗 <a href="{job.get('url')}" target="_blank">View Job</a>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No Naukri jobs found.")
