from rest_framework import serializers
from apps.studies.models import Report
from apps.users.models import PhysicianProfile

class PhysicianSimpleSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.get_full_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = PhysicianProfile
        fields = ['id', 'name', 'email']

class ReportListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'

from rest_framework import serializers


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = [
            'id',
            'narrative_text',
            'structured_data',
            'finalized_at'
        ]

from apps.studies.models import Study
class StudySerializer(serializers.ModelSerializer):
    report = ReportSerializer(read_only=True)
    doctor = PhysicianSimpleSerializer(read_only=True)

    class Meta:
        model = Study
        fields = [
            'id',
            'modality',
            'status',
            'created_at',
            'report',
            'doctor'
        ]

from apps.patients.models import Patient

class PatientWithStudiesSerializer(serializers.ModelSerializer):
    studies = StudySerializer(many=True, read_only=True)

    class Meta:
        model = Patient
        fields = [
            'id',
            'name',
            'mrn',
            'studies'
        ]

class PatientSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'name', 'mrn']

class StudySimpleSerializer(serializers.ModelSerializer):
    patient = PatientSimpleSerializer(read_only=True)

    class Meta:
        model = Study
        fields = ['id', 'modality', 'status', 'created_at', 'patient']

class ReportDetailSerializer(serializers.ModelSerializer):
    study = StudySimpleSerializer(read_only=True)
    doctor = PhysicianSimpleSerializer(read_only=True)

    class Meta:
        model = Report
        fields = [
            'id',
            'doctor',
            'narrative_text',
            'structured_data',
            'finalized_at',
            'study'
        ]