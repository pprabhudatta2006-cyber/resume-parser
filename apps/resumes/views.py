from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Resume, ParsedResume
from .serializers import ResumeSerializer, ResumeUploadSerializer, ParsedResumeSerializer
from repositories.resume_repository import ResumeRepository
from services.nlp_service import NLPService
from utils.file_utils import extract_text
import os

class ResumeViewSet(viewsets.ModelViewSet):
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ResumeRepository.get_user_resumes(self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = ResumeUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            resume = ResumeRepository.create_resume(
                user=request.user,
                file=file,
                filename=file.name
            )
            return Response(ResumeSerializer(resume).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def parse(self, request, pk=None):
        resume = self.get_object()
        try:
            # Extract text
            text = extract_text(resume.file.path)
            
            # NLP Processing
            nlp_service = NLPService()
            entities = nlp_service.extract_entities(text)
            
            # Prepare data for model
            parsed_data = {
                'full_name': entities.get('name'),
                'email': entities.get('emails')[0] if entities.get('emails') else None,
                'phone': entities.get('phones')[0] if entities.get('phones') else None,
                'linkedin_url': next((l for l in entities.get('links', []) if 'linkedin' in l), None),
                'github_url': next((l for l in entities.get('links', []) if 'github' in l), None),
                'skills': entities.get('skills', []),
                'candidate_profile': nlp_service.classify_profile(entities.get('skills', []), text),
                'total_experience_years': nlp_service.calculate_experience(text),
                'raw_text': text
            }
            
            parsed_obj = ResumeRepository.save_parsed_data(resume, parsed_data)
            return Response(ParsedResumeSerializer(parsed_obj).data)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_SET_ERROR)

class ParsedResumeView(viewsets.ReadOnlyModelViewSet):
    serializer_class = ParsedResumeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ParsedResume.objects.filter(resume__user=self.request.user)
