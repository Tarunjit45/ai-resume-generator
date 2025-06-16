from fpdf import FPDF
import os
import openai
import re
import uuid

# Optional: Use env variable or paste your key directly
openai.api_key = "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"

def extract_keywords(job_desc):
    # Simple keyword extractor: split by space and remove small words
    words = re.findall(r'\b\w{3,}\b', job_desc.lower())
    keywords = list(set(words))
    return keywords

def generate_ai_content(name, email, skills, experience, job_desc):
    # FAKE AI OUTPUT for demo without OpenAI
    content = f"""
{name}
Email: {email}

OBJECTIVE:
Passionate and results-driven Computer Science student seeking to apply my skills in a challenging internship role aligned with {', '.join(skills.split(','))}.

SKILLS:
{skills}

EXPERIENCE:
{experience}

MATCHED JOB DESCRIPTION INSIGHTS:
This resume was tailored based on the following JD:
{job_desc[:300]}...

PROJECTS:
- AI Spam Detection System using Machine Learning
- Resume Generator from JD using Streamlit (this one 😉)

EDUCATION:
B.Tech in Computer Science Engineering (2022–2026)

---
Generated with ❤️ using Python + Streamlit
"""
    return content

def generate_pdf(content, name):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    # Filter only Latin-1 compatible characters
    safe_content = content.encode('latin-1', 'ignore').decode('latin-1')

    for line in safe_content.split('\n'):
        pdf.multi_cell(0, 10, line)

    filename = f"generated/resume_{name}_{uuid.uuid4().hex[:6]}.pdf"
    os.makedirs("generated", exist_ok=True)
    pdf.output(filename)
    return filename


def generate_resume(name, email, skills, experience, job_desc):
    content = generate_ai_content(name, email, skills, experience, job_desc)
    pdf_path = generate_pdf(content, name)
    return pdf_path
