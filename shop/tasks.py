from celery import shared_task
from django.core.management import call_command
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_test_email(recipient):
    send_mail(
        subject="Bookshop",
        message="Це тестовий email, відправлений через Celery.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[recipient],
        fail_silently=False,
    )


@shared_task
def generate_report():
    print("Generating report...")
    return "Report generated"


@shared_task
def clear_expired_sessions():
    call_command("clearsessions")
    return "Expired sessions cleared"
