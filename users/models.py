from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import random

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_superadmin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)


    def __str__(self):
        return self.email
    

class EmailOTP(models.Model):
    email = models.EmailField()
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return self.created_at < timezone.now() - timezone.timedelta(minutes=5)

    @classmethod
    def generate_otp(cls, email):
        cls.objects.filter(email=email).delete()
        otp_code = "".join(str(random.randint(1, 9)) for _ in range(6))
        return cls.objects.create(email=email, otp_code=otp_code)

    





