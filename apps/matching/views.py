from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import JobDescription, MatchResult
from .serializers import JobDescriptionSerializer, MatchResultSerializer, BulkMatchSerializer
from apps.resumes.models import ParsedResume
from services.matching_service import MatchingService

class JobDescriptionViewSet(viewsets.ModelViewSet):
    queryset = JobDescription.objects.all()
    serializer_class = JobDescriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def match(self, request, pk=None):
        job = self.get_object()
        candidate_ids = request.data.get('candidate_ids', [])
        
        if not candidate_ids:
            candidates = ParsedResume.objects.all()
        else:
            candidates = ParsedResume.objects.filter(resume_id__in=candidate_ids)
            
        results = []
        for candidate in candidates:
            match_data = MatchingService.calculate_match(job, candidate)
            result, created = MatchResult.objects.update_or_create(
                job=job,
                candidate=candidate,
                defaults=match_data
            )
            results.append(result)
            
        serializer = MatchResultSerializer(results, many=True)
        return Response(serializer.data)

class RankingViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MatchResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        job_id = self.request.query_params.get('job_id')
        if job_id:
            return MatchResult.objects.filter(job_id=job_id).order_by('-total_score')
        return MatchResult.objects.all()
