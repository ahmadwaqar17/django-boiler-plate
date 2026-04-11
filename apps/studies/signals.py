from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.studies.models import Study, Report

@receiver(post_save, sender=Study)
def create_report_for_study(sender, instance, created, **kwargs):
    if created:
        Report.objects.create(study=instance, doctor=instance.doctor)
