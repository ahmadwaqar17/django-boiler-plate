from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from apps.users.models import User


class Command(BaseCommand):
    help = 'Clean up users who signed up but have not confirmed their email within 24 hours'

    def handle(self, *args, **kwargs):
        # 24 hours ago
        threshold_date = timezone.now() - timedelta(days=1)
        
        # Filter users who are inactive AND created before the threshold date
        unconfirmed_users = User.objects.filter(
            is_active=False,
            created_at__lt=threshold_date
        )
        
        count = unconfirmed_users.count()
        if count > 0:
            unconfirmed_users.delete()
            self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} unconfirmed users.'))
        else:
            self.stdout.write(self.style.SUCCESS('No unconfirmed users found to delete.'))
