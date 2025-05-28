from django.urls import path
from . import views

urlpatterns = [
    path('user-account/',views.UserAccountAPIView.as_view(),name='user-account'),
    # path('payment/balance/update/',views.ClickWebhookAPIView.as_view(),name='update-balance'),
    # path("payment/balance/top-up/",views.BalanceTopUpAPIView.as_view(),name='top-up-balance'),
    path('user-account/update/',views.UserAccountUpdataAPIView.as_view(),name='user-account-update'),
]