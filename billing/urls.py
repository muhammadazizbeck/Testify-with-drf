from django.urls import path
from . import views

urlpatterns = [
    path('user-account/',views.UserAccountAPIView.as_view(),name='user-account'),
    path('user-account/update/',views.UserAccountUpdataAPIView.as_view(),name='user-account-update')
]