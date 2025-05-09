from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Django settings modulini sozlash
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Celery config'ni import qilish
app.config_from_object('django.conf:settings', namespace='CELERY')

# Django application'larini Celeryga ro‘yxatga olish
app.autodiscover_tasks()
