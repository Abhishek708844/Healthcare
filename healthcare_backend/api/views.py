# api/views.py
from rest_framework import generics, permissions, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserRegisterSerializer, PatientSerializer, DoctorSerializer, PatientDoctorMappingSerializer
from .models import Patient, Doctor, PatientDoctorMapping

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only return patients created by the currently logged-in user
        return Patient.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        # Automatically set the creator to the current user
        serializer.save(created_by=self.request.user)

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]

# NEW: Add the PatientDoctorMapping ViewSet
class PatientDoctorMappingViewSet(viewsets.ModelViewSet):
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only return mappings where the patient belongs to the current user
        return PatientDoctorMapping.objects.filter(patient__created_by=self.request.user)

    def perform_create(self, serializer):
        patient = serializer.validated_data['patient']
        
        # Check if the patient belongs to the current user
        if patient.created_by != self.request.user:
            raise PermissionDenied("You can only assign doctors to your own patients.")
        
        # Check if this mapping already exists
        if PatientDoctorMapping.objects.filter(patient=patient, doctor=serializer.validated_data['doctor']).exists():
            raise serializers.ValidationError("This doctor is already assigned to the patient.")
        
        serializer.save()

    # Custom action to get doctors for a specific patient (implements GET /api/mappings/<patient_id>/)
    @action(detail=False, methods=['get'], url_path='patient/(?P<patient_id>[^/.]+)')
    def get_doctors_for_patient(self, request, patient_id=None):
        try:
            patient = Patient.objects.get(id=patient_id)
            
            # Check if patient belongs to current user
            if patient.created_by != request.user:
                return Response({"error": "You can only view doctors for your own patients."}, status=403)
            
            mappings = PatientDoctorMapping.objects.filter(patient=patient)
            serializer = self.get_serializer(mappings, many=True)
            return Response(serializer.data)
            
        except Patient.DoesNotExist:
            return Response({"error": "Patient not found."}, status=404)