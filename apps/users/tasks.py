from celery import shared_task
import time

@shared_task
def debug_task():
    """A sample debug task."""
    time.sleep(2)
    return 'Debug task completed'

@shared_task
def future_send_email_task(subject, message, recipient_list):
    """
    Placeholder task for sending emails asynchronously.
    Not currently used in signup flow.
    """
    # from django.core.mail import send_mail
    # send_mail(subject, message, None, recipient_list)
    pass
