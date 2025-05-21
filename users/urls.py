from django.urls import path
from . import views


app_name = 'users'
urlpatterns = [
    path('auth/login/',views.LoginAPIView.as_view(),name='login'),
    path('auth/logout/',views.LogoutAPIView.as_view(),name='logout'),
    path('auth/register/',views.RegisterAPIView.as_view(),name='send-otp'),
    path('auth/change-password/',views.ChangePasswordAPIView.as_view(),name='change-password'),
]