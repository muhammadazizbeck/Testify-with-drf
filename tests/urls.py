from django.urls import path
from . import views


urlpatterns = [
    path('free-test/',views.FreeTestAPIView.as_view(),name='free-test'),
    path('paid-test/',views.PaidTestAPIView.as_view(),name='paid-test'),
    path('create-test/',views.TestCreateAPIView.as_view(),name='create-test'),
]