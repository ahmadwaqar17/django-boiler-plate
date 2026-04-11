from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.studies.views import StudyViewSet, DoctorListView

router = DefaultRouter()
router.register(r'', StudyViewSet, basename='study')

urlpatterns = [
    path('doctors/', DoctorListView.as_view(), name='doctor-list'),
    path('', include(router.urls)),
]
