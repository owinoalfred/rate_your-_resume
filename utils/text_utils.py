import spacy
from transformers import DistilBertTokenizer, DistilBertModel
import torch
from sklearn.metrics.pairwise import cosine_similarity

# Load spaCy model for NER and text preprocessing
nlp = spacy.load("en_core_web_sm")

# Load pre-trained DistilBERT model and tokenizer
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = DistilBertModel.from_pretrained('distilbert-base-uncased')

def preprocess_text(text):
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
    return " ".join(tokens)

def compute_semantic_similarity(text1, text2):
    inputs1 = tokenizer(text1, return_tensors='pt', truncation=True, padding=True)
    inputs2 = tokenizer(text2, return_tensors='pt', truncation=True, padding=True)
    
    with torch.no_grad():
        outputs1 = model(**inputs1)
        outputs2 = model(**inputs2)
    
    vec1 = outputs1.last_hidden_state.mean(dim=1).numpy()
    vec2 = outputs2.last_hidden_state.mean(dim=1).numpy()
    
    similarity = cosine_similarity(vec1, vec2)[0][0]
    return similarity

def extract_skills(text):
    doc = nlp(text)
    skills = [ent.text for ent in doc.ents if ent.label_ == "SKILL"]
    return skills

def compute_skill_matching_score(cv_skills, jd_skills):
    common_skills = set(cv_skills) & set(jd_skills)
    score = len(common_skills) / len(jd_skills) if jd_skills else 0
    return score, common_skills

def extract_experience_education(text):
    doc = nlp(text)
    experience = []
    education = []
    
    for ent in doc.ents:
        if ent.label_ == "DATE":
            experience.append(ent.text)
        elif ent.label_ == "ORG":
            education.append(ent.text)
    
    return experience, education

def compute_experience_education_score(cv_text, jd_text):
    cv_experience, cv_education = extract_experience_education(cv_text)
    jd_experience, jd_education = extract_experience_education(jd_text)
    
    experience_score = len(set(cv_experience) & set(jd_experience)) / len(jd_experience) if jd_experience else 0
    education_score = len(set(cv_education) & set(jd_education)) / len(jd_education) if jd_education else 0
    
    # Combine experience and education scores with equal weight
    final_score = (experience_score + education_score) / 2 if (experience_score + education_score) > 0 else 0
    return final_score, cv_experience, jd_experience, cv_education, jd_education

def get_final_score(cv_text, jd_text):
    preprocessed_cv = preprocess_text(cv_text)
    preprocessed_jd = preprocess_text(jd_text)
    
    semantic_similarity_score = compute_semantic_similarity(preprocessed_cv, preprocessed_jd)
    cv_skills = extract_skills(cv_text)
    jd_skills = extract_skills(jd_text)
    skill_matching_score, common_skills = compute_skill_matching_score(cv_skills, jd_skills)
    experience_education_score, cv_experience, jd_experience, cv_education, jd_education = compute_experience_education_score(cv_text, jd_text)
    
    final_score = (0.5 * semantic_similarity_score +
                   0.3 * skill_matching_score +
                   0.2 * experience_education_score)
    
    return {
        "final_score": final_score,
        "semantic_similarity_score": semantic_similarity_score,
        "skill_matching_score": skill_matching_score,
        "experience_education_score": experience_education_score,
        "common_skills": common_skills,
        "cv_experience": cv_experience,
        "jd_experience": jd_experience,
        "cv_education": cv_education,
        "jd_education": jd_education
    }