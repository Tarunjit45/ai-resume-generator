# ✅ STEP 1: Install required libraries before running (in terminal)
# pip install streamlit keybert sentence-transformers jinja2 pdfkit
# For pdfkit to work, install wkhtmltopdf and add it to PATH: https://wkhtmltopdf.org/downloads.html

import streamlit as st
from keybert import KeyBERT
from sentence_transformers import SentenceTransformer
from jinja2 import Template
import pdfkit
import uuid
import os
import pdfkit

# ✅ Manually specify the path to wkhtmltopdf
path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

# Initialize model
model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')

kw_model = KeyBERT(model)


# HTML template for PDF generation
html_template = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        h1 { color: #333; }
        h2 { color: #444; margin-top: 30px; }
        p, li { font-size: 14px; color: #111; line-height: 1.6; }
    </style>
</head>
<body>
    <h1>{{ name }}</h1>
    <p><strong>Email:</strong> {{ email }}</p>
    <h2>Professional Summary</h2>
    <p>{{ summary }}</p>

    <h2>Skills Matched with Job Description</h2>
    <ul>
        {% for kw in matched_keywords %}
            <li>{{ kw }}</li>
        {% endfor %}
    </ul>

    <h2>Experience</h2>
    <p>{{ experience }}</p>
</body>
</html>
"""

# Function to extract keywords from job description
def extract_keywords(text, top_n=10):
    keywords = kw_model.extract_keywords(text, stop_words='english', top_n=top_n)
    return [kw[0] for kw in keywords]

# Generate resume HTML -> PDF
def generate_resume_pdf(name, email, skills, experience, job_desc):
    keywords = extract_keywords(job_desc)
    matched = [kw for kw in keywords if kw.lower() in skills.lower() or kw.lower() in experience.lower()]

    summary = f"A highly motivated candidate with relevant experience in {', '.join(matched)}. Adept at delivering impactful results and aligning well with the job description."

    context = {
        'name': name,
        'email': email,
        'summary': summary,
        'matched_keywords': matched,
        'experience': experience
    }

    html = Template(html_template).render(context)

    os.makedirs("generated", exist_ok=True)
    filename = f"generated/resume_{uuid.uuid4().hex[:6]}.pdf"
    pdfkit.from_string(html, filename, configuration=config)
    return filename

# Streamlit UI
st.set_page_config(page_title="AI Resume Generator", layout="centered")
st.title("📄 AI Resume Generator (Smart JD Matching)")

name = st.text_input("Your Full Name")
email = st.text_input("Email")
skills = st.text_area("Your Skills (comma-separated)")
experience = st.text_area("Your Experience Summary")
job_desc = st.text_area("Paste the Job Description Here")

if st.button("🚀 Generate Resume"):
    if not name or not email or not skills or not experience or not job_desc:
        st.error("Please fill in all fields.")
    else:
        with st.spinner("Generating your smart resume PDF..."):
            pdf_file = generate_resume_pdf(name, email, skills, experience, job_desc)
            st.success("🎉 Resume Generated!")
            with open(pdf_file, "rb") as file:
                st.download_button(label="📥 Download Resume PDF", data=file, file_name=pdf_file.split("/")[-1], mime="application/pdf")
