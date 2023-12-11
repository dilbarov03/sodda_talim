from celery import shared_task
from django.contrib.auth import get_user_model
from .models import UserLesson, UserTest

User = get_user_model()

@shared_task
def create_user_lesson(lesson):
    print("hiesffses")
    users = User.objects.all()
    for user in users:
        if not UserLesson.objects.filter(user=user, lesson_id=lesson).exists():
            UserLesson.objects.create(user=user, lesson_id=lesson, status="open")
    return "UserLesson objects created successfully"


@shared_task
def create_user_test(test):
    users = User.objects.all()
    for user in users:
        if not UserTest.objects.filter(user=user, test_id=test).exists():
            UserTest.objects.create(user=user, test_id=test, status="active")
    return "UserTest objects created successfully"
