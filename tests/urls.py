from django.urls import path
from . import views

urlpatterns = [
    path('my-tests/',views.MyTestAPIView.as_view(),name='my-tests'),
    path('free-tests/',views.FreeTestAPIVIew.as_view(),name='free-tests'),
    path('paid-tests/',views.PaidTestAPIView.as_view(),name='paid-tests'),
    path('buy-tests/<int:test_id>/',views.BuyPaidTestAPIView.as_view(),name='buy-tests')
]