from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ResumeViewSet, ParsedResumeView

router = DefaultRouter()
router.register(r'', ResumeViewSet, basename='resume')

urlpatterns = [
    path('', include(router.urls)),
    path('parsed/<uuid:pk>/', ParsedResumeView.as_view({'get': 'retrieve'}), name='parsed-resume-detail'),
]
