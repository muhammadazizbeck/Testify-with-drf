from celery import shared_task
import requests
from django.conf import settings

@shared_task
def sent_otp_email_task(email, otp):
    api_url = "https://api.sender.net/api/v2/email/send"
    api_token = settings.SENDER_NET_API_TOKEN  

    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "to": [email],
        "subject": "Tizimga kirishni tasdiqlash kodi",
        "html": f"<p>Sizning tizimga kirishni tasdiqlash kodingiz: <strong>{otp}</strong></p>",
        "from": {
            "email": settings.EMAIL_HOST_USER,  
            "name": "Sizning Tizim Nomi"
        }
    }

    response = requests.post(api_url, json=payload, headers=headers)

    if response.status_code in (200, 202):
        print(f"Email yuborildi: {email}")
        return True
    else:
        print(f"Email yuborishda xatolik: {response.text}")
        return False
