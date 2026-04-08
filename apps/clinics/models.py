import uuid
from django.db import models

class Clinic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    logo_url = models.URLField(max_length=500, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    fax = models.CharField(max_length=50, blank=True, null=True)
    settings = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
