from celery import shared_task
from django.contrib.auth import get_user_model
from .models import UserLesson, UserTest, Lesson, Test

User = get_user_model()

@shared_task
def create_free_lesson(lesson):
    # for all free lessons
    users = User.objects.all()
    for user in users:
        if not UserLesson.objects.filter(user=user, lesson_id=lesson).exists():
            UserLesson.objects.create(user=user, lesson_id=lesson, status="open")
    return "UserLesson objects created successfully"


@shared_task
def create_free_test(test):
    # for all free lessons
    users = User.objects.all()
    for user in users:
        if not UserTest.objects.filter(user=user, test_id=test).exists():
            UserTest.objects.create(user=user, test_id=test, status="active")
    return "UserTest objects created successfully"


@shared_task
def create_new_lesson(lesson_id):
    lesson = Lesson.objects.filter(id=lesson_id).first()
    
    # get previous lesson
    previous_lesson = Lesson.objects.filter(language=lesson.language, order__lt=lesson.order).last()
    
    
    user_lessons = UserLesson.objects.filter(lesson=previous_lesson, status="open")
    users = []
    for user_lesson in user_lessons:
        user_test = UserTest.objects.filter(user=user_lesson.user, test__lesson=user_lesson.lesson, 
                                            status="finished").last()
        if previous_lesson.tests.last() == user_test.test:
            users.append(user_lesson.user)
    print(users)
            
    for user in users:
        if not UserLesson.objects.filter(user=user, lesson=lesson).exists():
            if user.has_active_subscription():
                UserLesson.objects.create(user=user, lesson=lesson, status="open")
            else:
                UserLesson.objects.create(user=user, lesson=lesson, status="closed")
    
    return "New UserLesson objects created successfully"


@shared_task
def create_new_test(test):
    test = Test.objects.filter(id=test).first()
    
    # get user lesson for this test
    user_lessons = UserLesson.objects.filter(lesson=test.lesson, status="open").all()
    for user_lesson in user_lessons:
        if not UserTest.objects.filter(user=user_lesson.user, test=test).exists():
            UserTest.objects.create(user=user_lesson.user, test=test, status="active")
    return "UserTest objects created successfully"
