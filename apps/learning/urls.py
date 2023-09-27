from django.urls import path
from .views import LessonListView, TestDetailView, UserAnswerView


urlpatterns = [
    path("lessons/", LessonListView.as_view(), name="lessons-list"),
    path("test/<int:pk>/", TestDetailView.as_view(), name="test-detail"),
    path("user-answer/", UserAnswerView.as_view(), name="user-answer"),
]
    