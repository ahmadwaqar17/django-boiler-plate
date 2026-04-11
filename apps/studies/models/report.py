import uuid
from django.db import models
from .study import Study

class Report(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    study = models.OneToOneField(
        Study,
        on_delete=models.CASCADE,
        related_name='report'
    )
    doctor = models.ForeignKey(
        'users.PhysicianProfile',
        on_delete=models.SET_NULL,
        null=True,
        related_name='reports'
    )
    structured_data = models.JSONField(default=dict, blank=True)
    narrative_text = models.TextField(blank=True)
    finalized_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Report for Study {self.study.id}"
