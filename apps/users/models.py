from typing import ClassVar

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from common.models import UUIDTimestampMixin

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin, UUIDTimestampMixin):
    email = models.EmailField(unique=True, db_index=True)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: ClassVar[list[str]] = []

    objects = UserManager()

    def __str__(self):
        return self.email


class OTP(UUIDTimestampMixin):
    PURPOSE_CHOICES = (
        ("signup", "Signup"),
        ("password_reset", "Password Reset"),
    )

    email = models.EmailField()
    otp_code = models.CharField(max_length=6)
    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES, default="signup")
    is_used = models.BooleanField(default=False)
    failed_attempts = models.IntegerField(default=0)
    expires_at = models.DateTimeField()

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
