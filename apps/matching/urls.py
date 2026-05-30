from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobDescriptionViewSet, RankingViewSet

router = DefaultRouter()
router.register(r'jobs', JobDescriptionViewSet, basename='job')
router.register(r'candidates/ranking', RankingViewSet, basename='ranking')

urlpatterns = [
    path('', include(router.urls)),
]
