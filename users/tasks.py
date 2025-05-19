# from celery import shared_task
# from django.core.mail import send_mail
# from config.settings import DEFAULT_FROM_EMAIL

# @shared_task
# def sent_otp_email_task(email,otp):
#     send_mail(
#         subject='Tizimga kirishni tasdiqlash kodi',
#         message=f"Sizning tizimga kirishni tasdiqlash kodingiz {otp}",
#         from_email= DEFAULT_FROM_EMAIL,
#         recipient_list=[email],
#         fail_silently=False
#     )