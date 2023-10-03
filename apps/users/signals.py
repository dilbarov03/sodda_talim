from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from apps.learning.models import Lesson, UserLesson, UserTest, Test

@receiver(post_save, sender=User)
def add_initial_lessons(sender, instance, created, **kwargs):
    if created:
        # Add the first three lessons to the UserLesson model
        lessons_to_add = Lesson.objects.all()[:3]
        for lesson in lessons_to_add:
            UserLesson.objects.create(user=instance, lesson=lesson)
            
            # make all tests in these three lessons available to the user
            tests = lesson.tests.all()
            for test in tests:
                UserTest.objects.create(user=instance, test=test, status="active")
            