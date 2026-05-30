from rest_framework import serializers
from .models import JobDescription, MatchResult
from apps.resumes.serializers import ParsedResumeSerializer

class JobDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDescription
        fields = '__all__'

class MatchResultSerializer(serializers.ModelSerializer):
    candidate = ParsedResumeSerializer(read_only=True)
    
    class Meta:
        model = MatchResult
        fields = '__all__'

class BulkMatchSerializer(serializers.Serializer):
    job_id = serializers.UUIDField()
    candidate_ids = serializers.ListField(child=serializers.UUIDField(), required=False)
