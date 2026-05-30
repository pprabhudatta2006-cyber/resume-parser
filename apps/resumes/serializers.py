from rest_framework import serializers
from .models import Resume, ParsedResume

class ParsedResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParsedResume
        exclude = ('raw_text',)

class ResumeSerializer(serializers.ModelSerializer):
    parsed_data = ParsedResumeSerializer(read_only=True)

    class Meta:
        model = Resume
        fields = ('id', 'filename', 'file', 'uploaded_at', 'is_parsed', 'parsed_data')
        read_only_fields = ('id', 'uploaded_at', 'is_parsed', 'filename')

class ResumeUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        ext = value.name.split('.')[-1].lower()
        if ext not in ['pdf', 'docx']:
            raise serializers.ValidationError("Only PDF and DOCX files are allowed.")
        return value
