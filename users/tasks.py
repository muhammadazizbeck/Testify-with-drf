from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_otp_email_task(email, otp):
    try:
        send_mail(
            subject='Tizimga kirishni tasdiqlash kodi',
            message=f"Sizning tizimga kirishni tasdiqlash kodingiz {otp}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False
        )
        logger.info(f"OTP {otp} successfully sent to {email}")
    except Exception as e:
        logger.error(f"Failed to send OTP to {email}: {str(e)}")
        raise  