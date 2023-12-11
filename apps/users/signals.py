from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from apps.learning.models import Lesson, UserLesson, UserTest, Test

@receiver(post_save, sender=User)
def add_initial_lessons(sender, instance, created, **kwargs):
    if created:
        # Add the first three lessons to the UserLesson model
        lessons_to_add = Lesson.objects.filter(order__lte=3)
        for lesson in lessons_to_add:
            if UserLesson.objects.filter(user=instance, lesson=lesson).exists():
                continue
            
            UserLesson.objects.create(user=instance, lesson=lesson, status="open")
            
            # make all tests in these three lessons available to the user
            tests = lesson.tests.all()
            for test in tests:
                UserTest.objects.create(user=instance, test=test, status="active")
    else:
        # If the user has an active subscription, make all lessons available to the user
        if instance.has_active_subscription():
            closed_lessons = UserLesson.objects.filter(user=instance, status="closed")
            closed_lessons_list = list(closed_lessons)
            closed_lessons.update(status="open")
            
            if len(closed_lessons_list) == 0:
                return
            
            elif len(closed_lessons_list) == 1:
                last_lesson = closed_lessons_list[0]
                # make the first test of the last lesson available to the user
                UserTest.objects.filter(user=instance, test__lesson=last_lesson.lesson, status="closed").update(status="active")
            else:
                for lesson in closed_lessons_list[:-1]:
                    UserTest.objects.filter(user=instance, test__lesson=lesson.lesson, status="closed").update(status="active")
                
                last_lesson = closed_lessons_list[-1]
                # make the first test of the last lesson available to the user
                user_test = UserTest.objects.filter(user=instance, test__lesson=last_lesson.lesson, status="closed").first()
                user_test.status = "active"
                user_test.save()
            