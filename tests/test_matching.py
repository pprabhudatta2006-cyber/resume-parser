from django.test import TestCase
from apps.matching.models import JobDescription
from apps.resumes.models import ParsedResume, Resume
from apps.authentication.models import User
from services.matching_service import MatchingService
import uuid

class MatchingServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@example.com", password="password")
        self.resume = Resume.objects.create(user=self.user, filename="test.pdf")
        self.candidate = ParsedResume.objects.create(
            resume=self.resume,
            skills=['Python', 'Django', 'PostgreSQL'],
            total_experience_years=3.0
        )
        self.job = JobDescription.objects.create(
            title="Senior Django Developer",
            required_skills=['Python', 'Django', 'Docker', 'AWS'],
            min_experience_years=5.0
        )

    def test_calculate_match(self):
        match_result = MatchingService.calculate_match(self.job, self.candidate)
        
        # 2 skills match out of 4 (50%)
        # 3 years exp < 5 years (60%)
        # Total: (50 * 0.7) + (60 * 0.3) = 35 + 18 = 53
        self.assertEqual(match_result['skill_match_score'], 50.0)
        self.assertEqual(match_result['experience_match_score'], 60.0)
        self.assertEqual(match_result['total_score'], 53.0)
