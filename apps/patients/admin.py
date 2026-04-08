from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'mrn', 'clinic', 'dob', 'sex', 'created_at')
    list_filter = ('clinic', 'sex')
    search_fields = ('name', 'mrn')
