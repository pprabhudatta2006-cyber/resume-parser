from django.db import models
from apps.resumes.models import ParsedResume
import uuid

class JobDescription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    required_skills = models.JSONField(default=list)
    min_experience_years = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class MatchResult(models.Model):
    job = models.ForeignKey(JobDescription, on_delete=models.CASCADE, related_name='matches')
    candidate = models.ForeignKey(ParsedResume, on_delete=models.CASCADE, related_name='job_matches')
    skill_match_score = models.FloatField()
    experience_match_score = models.FloatField()
    total_score = models.FloatField()
    matched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-total_score']
