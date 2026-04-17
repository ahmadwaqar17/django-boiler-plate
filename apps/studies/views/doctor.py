from django.utils import timezone
from apps.patients.models import Patient
from apps.studies.models import Report
from rest_framework import generics
from apps.studies.serializers import ReportListSerializer,PatientWithStudiesSerializer,ReportDetailSerializer
from core.permissions import IsDoctor


class ReportListView(generics.ListAPIView):
    permission_classes = [IsDoctor]
    serializer_class = ReportListSerializer
    queryset = Report.objects.all()

    # def get_queryset(self):
    #     return Report.objects.filter(doctor=self.request.user.physician_profile).order_by('-created_at')


class ReportRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsDoctor]
    serializer_class = ReportDetailSerializer
    queryset = Report.objects.select_related('study').all()

    def perform_update(self, serializer):
        # Save narrative_text and structured_data
        report = serializer.save()
        
        # Populate finalized_at
        report.finalized_at = timezone.now()
        report.save(update_fields=['finalized_at'])
        
        # Change associated study status
        if hasattr(report, 'study') and report.study:
            study = report.study
            study.status = 'FINALIZED'
            study.save(update_fields=['status'])



class FetchStudynReportView(generics.ListAPIView):
    permission_classes = [IsDoctor]
    serializer_class = PatientWithStudiesSerializer
    queryset = Patient.objects.prefetch_related('studies__report').all()
    