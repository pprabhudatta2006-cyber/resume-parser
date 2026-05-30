import spacy
import re
from typing import Dict, List, Any

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_md")
except:
    # Fallback if model not downloaded yet
    nlp = None

class NLPService:
    def __init__(self):
        self.nlp = nlp

    def extract_entities(self, text: str) -> Dict[str, Any]:
        if not self.nlp:
            return {}
        
        doc = self.nlp(text)
        entities = {
            "name": "",
            "emails": re.findall(r'[\w\.-]+@[\w\.-]+', text),
            "phones": re.findall(r'[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}', text),
            "links": re.findall(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', text),
            "skills": self._extract_skills(text),
            "education": [],
            "experience": [],
        }

        # Simple name extraction from first few lines or PERSON entity
        for ent in doc.ents:
            if ent.label_ == "PERSON" and not entities["name"]:
                entities["name"] = ent.text
                break
        
        return entities

    def _extract_skills(self, text: str) -> List[str]:
        # A small predefined list of skills for demonstration. 
        # In production, this would be a larger dictionary or mapped via NER.
        skill_db = [
            'Python', 'Django', 'Flask', 'FastAPI', 'Java', 'Spring', 'React', 'Angular', 'Vue',
            'Javascript', 'Typescript', 'SQL', 'PostgreSQL', 'MongoDB', 'AWS', 'Azure', 'GCP',
            'Docker', 'Kubernetes', 'CI/CD', 'Machine Learning', 'AI', 'NLP', 'Data Science',
            'PyTorch', 'TensorFlow', 'UI/UX', 'Figma', 'Solidity', 'Blockchain'
        ]
        
        found_skills = []
        for skill in skill_db:
            if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE):
                found_skills.append(skill)
        
        return list(set(found_skills))

    def classify_profile(self, skills: List[str], text: str) -> str:
        text = text.lower()
        skills = [s.lower() for s in skills]
        
        if any(s in skills for s in ['machine learning', 'ai', 'nlp', 'pytorch', 'tensorflow']):
            return "AI/ML"
        if any(s in skills for s in ['data science', 'pandas', 'numpy', 'scikit-learn']):
            return "Data Science"
        if any(s in skills for s in ['docker', 'kubernetes', 'aws', 'azure', 'devops', 'ci/cd']):
            return "DevOps"
        if any(s in skills for s in ['cloud', 'aws', 'gcp']):
            return "Cloud Computing"
        if any(s in skills for s in ['security', 'cybersecurity', 'penetration']):
            return "Cybersecurity"
        if any(s in skills for s in ['ui', 'ux', 'figma', 'design']):
            return "UI/UX"
        
        return "Software Development"

    def calculate_experience(self, text: str) -> float:
        # Placeholder for complex experience calculation
        # In a real scenario, we would parse dates from experience section
        years = re.findall(r'(\d+)\+?\s*years?', text)
        if years:
            return float(max(years))
        return 0.0
