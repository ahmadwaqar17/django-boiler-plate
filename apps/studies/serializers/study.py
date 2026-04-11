from rest_framework import serializers
from apps.studies.models import Study, Report
from apps.patients.models import Patient
from apps.patients.serializers import PatientSerializer

class StudyListSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    mrn = serializers.CharField(source='patient.mrn', read_only=True)
    technician_name = serializers.CharField(source='technician.user.get_full_name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.user.get_full_name', read_only=True)

    class Meta:
        model = Study
        fields = ['id', 'patient_name', 'mrn', 'modality', 'status', 'technician_name', 'doctor_name', 'created_at']

class StudyCreateSerializer(serializers.ModelSerializer):
    patient_id = serializers.UUIDField(write_only=True)
    doctor_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Study
        fields = ['patient_id', 'modality', 'doctor_id']

    def create(self, validated_data):
        patient_id = validated_data.pop('patient_id')
        doctor_id = validated_data.pop('doctor_id', None)
        
        # Map patient_id to patient object
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            raise serializers.ValidationError({"patient_id": "Patient not found."})
        
        # Map doctor_id to doctor profile
        doctor = None
        if doctor_id:
            from apps.users.models import PhysicianProfile
            try:
                doctor = PhysicianProfile.objects.get(id=doctor_id)
            except PhysicianProfile.DoesNotExist:
                raise serializers.ValidationError({"doctor_id": "Physician profile not found."})
        
        study = Study.objects.create(patient=patient, doctor=doctor, **validated_data)
        return study
