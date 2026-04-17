from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.studies.views import (
    StudyViewSet, DoctorListView, ReportListView, FetchStudynReportView,
    ReportRetrieveUpdateView
)

router = DefaultRouter()
router.register(r'', StudyViewSet, basename='study')

urlpatterns = [
    path('doctors/', DoctorListView.as_view(), name='doctor-list'),
    path('reports/', ReportListView.as_view(), name='report-list'),
    path('reports/<uuid:pk>/', ReportRetrieveUpdateView.as_view(), name='report-detail'),
    path('fetch-study-report/', FetchStudynReportView.as_view(), name='fetch-study-report'),
    path('', include(router.urls)),
]
