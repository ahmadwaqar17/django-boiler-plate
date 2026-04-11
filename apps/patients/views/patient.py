from rest_framework import viewsets, filters
from django.db.models import Q
from apps.patients.models import Patient
from apps.patients.serializers import PatientSerializer

class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    queryset = Patient.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by user's clinic
        # if hasattr(self.request.user, 'clinic') and self.request.user.clinic:
        #     queryset = queryset.filter(clinic=self.request.user.clinic)
        
        # Search by MRN or Name
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(
                Q(mrn__icontains=search_query) | 
                Q(name__icontains=search_query)
            )
        
        return queryset

    def perform_create(self, serializer):
        # Automatically assign current user's clinic to the patient
        if hasattr(self.request.user, 'clinic') and self.request.user.clinic:
            serializer.save(clinic=self.request.user.clinic)
        else:
            # Fallback or error handling if needed
            serializer.save()
