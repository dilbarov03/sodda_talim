from django.urls import path
from .views import LessonListView, TestDetailView, UserAnswerView, EntranceQuestionListView, AddLessonsView


urlpatterns = [
    path("lessons/", LessonListView.as_view(), name="lessons-list"),
    path("test/<int:pk>/", TestDetailView.as_view(), name="test-detail"),
    path("user-answer/", UserAnswerView.as_view(), name="user-answer"),
    path("entrance-questions/", EntranceQuestionListView.as_view(), name="entrance-questions-list"),
    path("add-lessons/", AddLessonsView.as_view(), name="add-lessons"),
]
    