from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import random

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    

class EmailOTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def generate_otp(self):
        self.otp = "".join(str(random.randint(1,9)) for _ in range(5))
        self.created_at = timezone.now()
        self.save()

    





