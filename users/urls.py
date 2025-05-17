from django.urls import path
from . import views

urlpatterns = [
    path('auth/register/',views.RegisterAPIView.as_view(),name='send-otp'),
    path('auth/verify-otp/',views.VerifyOTPAPIView.as_view(),name='verify-otp'),
]