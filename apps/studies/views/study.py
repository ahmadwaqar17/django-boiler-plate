from rest_framework import viewsets, permissions, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.studies.models import Study
from apps.users.models import PhysicianProfile
from apps.users.serializers import PhysicianProfileSerializer
from apps.studies.serializers import StudyListSerializer, StudyCreateSerializer

class DoctorListView(generics.ListAPIView):
    
    serializer_class = PhysicianProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = PhysicianProfile.objects.all().select_related('user')
        # Filter by the same clinic as the current user
        if hasattr(self.request.user, 'clinic') and self.request.user.clinic:
            queryset = queryset.filter(user__clinic=self.request.user.clinic)
        return queryset

class StudyViewSet(viewsets.ModelViewSet):
    queryset = Study.objects.all().select_related('patient')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return StudyCreateSerializer
        return StudyListSerializer

    def perform_create(self, serializer):
        # Assign current user as technician (must have a profile)
        if hasattr(self.request.user, 'technician_profile'):
            serializer.save(technician=self.request.user.technician_profile)
        else:
            # Fallback for admins or others who might create studies
            serializer.save()

    def get_queryset(self):
        queryset = super().get_queryset()
        # In a real app, we might filter by clinic here too
        if hasattr(self.request.user, 'clinic') and self.request.user.clinic:
            queryset = queryset.filter(patient__clinic=self.request.user.clinic)
        
        return queryset.order_by('-created_at')
