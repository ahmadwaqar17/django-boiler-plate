from rest_framework import serializers
from apps.patients.models import Patient

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'clinic', 'mrn', 'name', 'dob', 'sex', 'created_at', 'updated_at']
        read_only_fields = ['id', 'clinic', 'created_at', 'updated_at']
