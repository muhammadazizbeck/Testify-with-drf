from django.urls import path
from . import views

app_name = 'tests'
urlpatterns = [
    path('create-test/',views.TestCreateAPIView.as_view(),name='create-test')
]