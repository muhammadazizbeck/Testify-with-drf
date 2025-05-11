from django.urls import path
from . import views

urlpatterns = [
    path('my-tests/',views.MyTestAPIView.as_view(),name='my-tests'),
    path('free-tests/',views.FreeTestAPIVIew.as_view(),name='free-tests'),
    path('paid-tests/',views.PaidTestAPIView.as_view(),name='paid-tests'),
    path('create-test/',views.CreateTestAPIView.as_view(),name='create-test'),
    path('buy-test/<int:test_id>/',views.BuyPaidTestAPIView.as_view(),name='buy-test'),
    path('create-category/',views.CreateCategoryAPIView.as_view(),name='create-category'),
]