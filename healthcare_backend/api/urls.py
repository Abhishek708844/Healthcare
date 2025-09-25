# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, PatientViewSet, DoctorViewSet, PatientDoctorMappingViewSet  # ← ADD PatientDoctorMappingViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Create a router
router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patient')  # /api/patients/
router.register(r'doctors', DoctorViewSet, basename='doctor')  # /api/doctors/
router.register(r'mappings', PatientDoctorMappingViewSet, basename='mapping')  # ← ADD THIS LINE

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),  # Include the router URLs
]