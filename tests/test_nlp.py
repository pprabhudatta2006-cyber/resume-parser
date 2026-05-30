from django.test import TestCase
from services.nlp_service import NLPService

class NLPServiceTest(TestCase):
    def setUp(self):
        self.nlp_service = NLPService()
        self.sample_text = """
        John Doe
        Email: john.doe@example.com
        Phone: +1-234-567-8901
        Skills: Python, Django, Docker, AWS.
        Experience: 5 years of software development.
        """

    def test_extract_entities(self):
        entities = self.nlp_service.extract_entities(self.sample_text)
        self.assertIn('john.doe@example.com', entities['emails'])
        self.assertIn('Python', entities['skills'])
        self.assertIn('Django', entities['skills'])

    def test_classify_profile(self):
        skills = ['Python', 'Django', 'Docker']
        profile = self.nlp_service.classify_profile(skills, self.sample_text)
        self.assertEqual(profile, "Software Development")
        
        ai_skills = ['Python', 'Machine Learning', 'NLP']
        profile_ai = self.nlp_service.classify_profile(ai_skills, "AI Engineer")
        self.assertEqual(profile_ai, "AI/ML")
