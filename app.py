import streamlit as st
from src.helper import extract_text_from_pdf, ask_gemini

st.set_page_config(
    page_title="JOB Recommender",
    layout="wide"
)

st.title("AI Job recommender")

st.markdown("Upload your resume and get job recommendations based on your skills and experience from naukri and linkedin")

uploaded_file = st.file_uploader("Upload  Your resume (PDF)",type=["pdf"])

if uploaded_file:
    with st.spinner("Extracting text from resume"):
        resume_text = extract_text_from_pdf(uploaded_file=uploaded_file)

    with st.spinner("Summarizing your resume..."):
        summary = ask_gemini("Summarize this resume highighting the skills, education and experiences :\n {resume_text}",max_token=500)

    with st.spinner("Finding skills gaps..."):
        skill_gaps = ask_gemini("Analyze this resume and highlight missing skills, certification , and experience needed or better job opportunities : \n\n {resume_text}", max_token=500)

    
    
