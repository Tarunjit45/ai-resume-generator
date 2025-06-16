# AI Resume Generator

This project is a simple AI-powered resume generator built with Streamlit. It allows users to input their personal and professional details and generates a PDF resume.

## File Structure

- `app.py`: Streamlit app interface
- `resume_generator.py`: Core logic for generating PDF resumes
- `utils.py`: Helper functions such as keyword extraction
- `templates/resume_template.txt`: Prompt template for GPT (can be used for AI enhancements)
- `generated/`: Directory where generated resumes are saved
- `requirements.txt`: Python dependencies
- `README.md`: Project documentation

## Installation

Install dependencies:

```
pip install -r requirements.txt
```

## Usage

Run the Streamlit app:

```
streamlit run app.py
```

Enter your details and generate your resume.

## License

MIT License
