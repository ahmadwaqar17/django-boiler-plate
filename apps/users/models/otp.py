import uuid
from django.db import models
from django.utils import timezone

class OTP(models.Model):
    PURPOSE_CHOICES = (
        ('signup', 'Signup'),
        ('password_reset', 'Password Reset'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField()
    otp_code = models.CharField(max_length=6)
    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES, default='signup')
    is_used = models.BooleanField(default=False)
    failed_attempts = models.IntegerField(default=0)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self, max_attempts=5):
        if self.is_used:
            return False, "OTP has already been used."
        if self.expires_at < timezone.now():
            return False, "OTP has expired."
        if self.failed_attempts >= max_attempts:
            return False, "Maximum verification attempts exceeded."
        return True, ""

    def __str__(self):
        return f"{self.email} - {self.otp_code}"
