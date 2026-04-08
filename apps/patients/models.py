import uuid
from django.db import models

class Patient(models.Model):
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('U', 'Unknown'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clinic = models.ForeignKey(
        'clinics.Clinic', 
        on_delete=models.CASCADE, 
        related_name='patients'
    )
    mrn = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    dob = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('clinic', 'mrn')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.mrn})"
