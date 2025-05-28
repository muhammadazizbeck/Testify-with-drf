from django.urls import path
from . import views


urlpatterns = [
    path('free-test/',views.FreeTestAPIView.as_view(),name='free-test'),
    path('paid-test/',views.PaidTestAPIView.as_view(),name='paid-test'),
    
    path('create-test/',views.TestCreateAPIView.as_view(),name='create-test'),
    path('<int:test_id>/unlock/',views.UnlockTestAPIView.as_view(),name='unlock-test'),
    path('<int:test_id>/test-detail/',views.TestDetailAPIView.as_view(),name='question-list'),
    path('<int:test_id>/submit-test/',views.SubmitTestAPIView.as_view(),name='submit-test'),
    path('<int:test_id>/create-questions/',views.QuestionCreateAPIView.as_view(),name='create-test'),

    path('categories/',views.CategoryAPIView.as_view(),name='categories'),
    path('create-category/',views.CategoryCreateAPIView.as_view(),name='create-category'),
    path('<int:category_id>/category-detail/',views.CategoryDetailAPIView.as_view(),name='create-category'),
]