import logging
import streamlit as st
from utils.pdf_processor import extract_text_from_pdf
from utils.text_utils import get_final_score

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    st.title("AI-Powered Resume Analyzer")

    st.header("Upload or Paste Your CV")
    st.write("You can either upload your CV as a PDF file or paste the text directly.")

    # CV Upload or Text Box
    uploaded_cv = st.file_uploader("Upload your CV (PDF)", type=["pdf"])
    cv_text = st.text_area("Or paste your CV text here")

    st.header("Upload or Paste the Job Description")
    st.write("You can either upload the job description as a PDF file or paste the text directly.")

    # Job Description Upload or Text Box
    uploaded_jd = st.file_uploader("Upload the Job Description (PDF)", type=["pdf"])
    jd_text = st.text_area("Or paste the Job Description text here")

    # If a PDF is uploaded, extract text from it
    if uploaded_cv is not None:
        logging.info("Uploaded CV: %s", uploaded_cv.name)
        cv_text = extract_text(uploaded_cv)

    if uploaded_jd is not None:
        logging.info("Uploaded Job Description: %s", uploaded_jd.name)
        jd_text = extract_text(uploaded_jd)

    # Ensure both CV and Job Description texts are provided
    if st.button("Analyze"):
        if not cv_text or not jd_text:
            st.error("Please provide both CV and Job Description text.")
        else:
            try:
                with st.spinner('Analyzing...'):
                    scores = get_final_score(cv_text, jd_text)
                st.success(f"Final compatibility score: {scores['final_score']}")

                st.subheader("Detailed Scores")
                st.write(f"Semantic Similarity Score: {scores['semantic_similarity_score']}")
                st.write(f"Skill Matching Score: {scores['skill_matching_score']}")
                st.write(f"Experience and Education Score: {scores['experience_education_score']}")

                st.subheader("Common Skills")
                st.write(", ".join(scores['common_skills']))

                st.subheader("Experience Comparison")
                st.write(f"CV Experience: {', '.join(scores['cv_experience'])}")
                st.write(f"Job Description Experience: {', '.join(scores['jd_experience'])}")

                st.subheader("Education Comparison")
                st.write(f"CV Education: {', '.join(scores['cv_education'])}")
                st.write(f"Job Description Education: {', '.join(scores['jd_education'])}")

                st.subheader("Suggestions for Improvement")
                if scores['semantic_similarity_score'] < 0.8:
                    st.write("Improve the semantic similarity by ensuring your CV closely matches the job description in terms of language and terminology.")
                if scores['skill_matching_score'] < 0.8:
                    st.write("Add more relevant skills to your CV that match the job description.")
                if scores['experience_education_score'] < 0.8:
                    st.write("Ensure your CV highlights relevant experience and education that match the job description.")

            except Exception as e:
                logging.error("Error processing files: %s", e)
                st.error("An error occurred while processing the files. Please try again.")

@st.cache_data
def extract_text(file):
    if file.type == "application/pdf":
        return extract_text_from_pdf(file)
    else:
        return file.read().decode("utf-8")

if __name__ == "__main__":
    main()