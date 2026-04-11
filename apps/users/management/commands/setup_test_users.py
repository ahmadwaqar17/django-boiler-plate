from django.core.management.base import BaseCommand
from apps.users.models import User, TechnicianProfile, PhysicianProfile, AdminProfile
from apps.clinics.models import Clinic
from django.db import transaction

class Command(BaseCommand):
    help = 'Create 3 test users with different roles (technician, physician, admin)'

    def handle(self, *args, **kwargs):
        self.stdout.write("Creating test users...")

        with transaction.atomic():
            # Get or create a default clinic
            clinic, created = Clinic.objects.get_or_create(
                name="Test Clinic",
                defaults={"address": "123 Test St"}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created clinic: {clinic.name}"))

            users_data = [
                {
                    "email": "tech@example.com",
                    "first_name": "John",
                    "last_name": "Technician",
                    "role": "technician",
                    "password": "password123",
                    "profile_model": TechnicianProfile
                },
                {
                    "email": "doc@example.com",
                    "first_name": "Jane",
                    "last_name": "Physician",
                    "role": "physician",
                    "password": "password123",
                    "profile_model": PhysicianProfile
                },
                {
                    "email": "admin@example.com",
                    "first_name": "Super",
                    "last_name": "Admin",
                    "role": "admin",
                    "password": "password123",
                    "profile_model": AdminProfile
                }
            ]

            for user_info in users_data:
                is_admin = user_info["role"] == "admin"
                user, created = User.objects.get_or_create(
                    email=user_info["email"],
                    defaults={
                        "first_name": user_info["first_name"],
                        "last_name": user_info["last_name"],
                        "role": user_info["role"],
                        "clinic": clinic,
                        "is_active": True,
                        "is_verified": True,
                        "is_staff": is_admin,
                        "is_superuser": is_admin
                    }
                )

                if created:
                    user.set_password(user_info["password"])
                    user.save()
                    self.stdout.write(self.style.SUCCESS(f"Created user: {user.get_full_name()}"))
                else:
                    # Update existing user names if they are empty
                    updated = False
                    if not user.first_name:
                        user.first_name = user_info["first_name"]
                        updated = True
                    if not user.last_name:
                        user.last_name = user_info["last_name"]
                        updated = True
                    if updated:
                        user.save()
                        self.stdout.write(self.style.SUCCESS(f"Updated names for: {user.email}"))
                    else:
                        self.stdout.write(self.style.WARNING(f"User {user.email} already exists"))
                
                # Ensure role-specific profile exists
                profile, prof_created = user_info["profile_model"].objects.get_or_create(user=user)
                if prof_created:
                    self.stdout.write(self.style.SUCCESS(f"Created profile for: {user.email}"))

        self.stdout.write(self.style.SUCCESS("Setup complete! Password for all: password123"))
