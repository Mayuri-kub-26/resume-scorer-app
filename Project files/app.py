import streamlit as st
from pdfminer.high_level import extract_text as extract_pdf_text
import docx2txt
import re

# -----------------------
# Functions
# -----------------------
def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_pdf_text(uploaded_file)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return docx2txt.process(uploaded_file)
    else:
        return "Unsupported file type. Please upload a PDF or DOCX."

def score_resume(text):
    score = 0
    feedback = []

    # Keywords to check
    keywords = ['python', 'java', 'sql', 'aws', 'html', 'css', 'javascript', 'machine learning', 'data analysis']
    found_keywords = [kw for kw in keywords if kw.lower() in text.lower()]
    score += len(found_keywords) * 10

    if len(found_keywords) < 3:
        feedback.append("Include more relevant technical keywords to improve your chances.")

    # Contact Info Checks
    if re.search(r'\b\d{10}\b', text):
        score += 5
    else:
        feedback.append("Phone number not detected. Make sure to include contact info.")

    if re.search(r'\S+@\S+', text):
        score += 5
    else:
        feedback.append("Email address missing or not detected.")

    # Basic structure checks
    if "project" in text.lower():
        score += 5
    else:
        feedback.append("Consider adding a 'Projects' section.")

    if "experience" in text.lower():
        score += 5
    else:
        feedback.append("Mention your work experience, internships, or freelancing.")

    # Cap score at 100
    score = min(score, 100)

    return score, found_keywords, feedback

# -----------------------
# Streamlit UI
# -----------------------
st.set_page_config(page_title="Resume Scorer", layout="centered")
st.title("📄 Real-Time Resume Scorer")
st.write("Upload your resume to get an instant score and feedback.")

uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])

if uploaded_file is not None:
    resume_text = extract_text_from_file(uploaded_file)
    
    with st.expander("📃 Extracted Resume Text"):
        st.write(resume_text[:1500] + '...')  # Show first 1500 characters
    
    score, found_keywords, feedback = score_resume(resume_text)

    st.subheader(f"🎯 Resume Score: {score} / 100")

    st.markdown("**✅ Keywords Detected:**")
    st.write(", ".join(found_keywords) if found_keywords else "None")

    st.markdown("**📝 Feedback:**")
    for item in feedback:
        st.write(f"- {item}")
