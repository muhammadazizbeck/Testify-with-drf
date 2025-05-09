from django.urls import path
from . import views

urlpatterns = [
    path('auth/send-otp/',views.SendOTPAPIView.as_view(),name='send-otp'),
    path('auth/verify-otp/',views.VerifyOTPAPIView.as_view(),name='verify-otp'),
    path('auth/logout/',views.LogoutAPIView.as_view(),name='logout')
]