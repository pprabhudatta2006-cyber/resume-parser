from django.db import models
from django.conf import settings
import uuid

class Resume(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resumes')
    file = models.FileField(upload_to='resumes/')
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_parsed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} - {self.filename}"

class ParsedResume(models.Model):
    resume = models.OneToOneField(Resume, on_delete=models.CASCADE, related_name='parsed_data')
    full_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    linkedin_url = models.URLField(null=True, blank=True)
    github_url = models.URLField(null=True, blank=True)
    portfolio_url = models.URLField(null=True, blank=True)
    
    # Store complex structured data as JSON
    education = models.JSONField(default=list)
    skills = models.JSONField(default=list)
    experience = models.JSONField(default=list)
    projects = models.JSONField(default=list)
    certifications = models.JSONField(default=list)
    achievements = models.JSONField(default=list)
    languages = models.JSONField(default=list)
    
    total_experience_years = models.FloatField(default=0.0)
    candidate_profile = models.CharField(max_length=100, null=True, blank=True)
    
    raw_text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Parsed: {self.resume.filename}"
