import uuid
from django.db import models

class Study(models.Model):
    MODALITY_CHOICES = [
        ('ECHO', 'Echo'),
        ('VASCULAR', 'Vascular'),
        ('NUCLEAR', 'Nuclear'),
        ('EKG', 'EKG'),
    ]

    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('FINALIZED', 'Finalized'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(
        'patients.Patient',
        on_delete=models.CASCADE,
        related_name='studies'
    )
    technician = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='studies_created'
    )
    modality = models.CharField(max_length=50, choices=MODALITY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Study {self.id} - {self.get_modality_display()} - {self.patient.name}"


class Report(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    study = models.OneToOneField(
        Study,
        on_delete=models.CASCADE,
        related_name='report'
    )
    structured_data = models.JSONField(default=dict, blank=True)
    narrative_text = models.TextField(blank=True)
    finalized_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Report for Study {self.study.id}"
