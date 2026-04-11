from django.contrib import admin
from apps.studies.models import Study, Report

@admin.register(Study)
class StudyAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'modality', 'status', 'technician', 'created_at')
    list_filter = ('modality', 'status')
    search_fields = ('patient__name', 'id')

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'study', 'finalized_at')
    search_fields = ('study__id',)
