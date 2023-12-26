from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from apps.learning.models import Lesson, Test, UserLesson, UserTest
from .tasks import create_free_lesson, create_free_test, create_new_lesson, create_new_test



User = get_user_model()

@receiver(post_save, sender=Lesson)
def add_initial_lesson(sender, instance, created, **kwargs):
    if created:
        if instance.order <= 3:
            create_free_lesson.delay(instance.id)
        else:
            create_new_lesson.delay(instance.id)        
        

@receiver(post_save, sender=Test)
def add_tests(sender, instance, created, **kwargs):
    if created:
        if instance.lesson.order <= 3:
            create_free_test.delay(instance.id)
        else:
            create_new_test.delay(instance.id)
    


# @receiver(post_save, sender=UserTest)
# def next_lesson(sender, instance, created, **kwargs):
#     # check if this test is the last test of the lesson
#     test = instance.test
#     lesson = test.lesson
#     if instance.status == "finished" and test == lesson.tests.last():        
#         # check if user has active subscription
#         if instance.user.has_active_subscription():
#             # if it is, then add the next lesson to the UserLesson model
#             next_lesson = Lesson.objects.filter(order=lesson.order + 1).first()
#             if next_lesson:
#                 UserLesson.objects.get_or_create(user=instance.user, lesson=next_lesson) 
                  
#     elif instance.status == "finished" and test != lesson.tests.last():
#         # if it is, then add the next test to the UserTest model
#         next_test = Test.objects.filter(lesson=lesson, order=test.order+1).first()
#         if next_test:
#             if not UserTest.objects.filter(user=instance.user, test=next_test).exists():
#                 UserTest.objects.get_or_create(user=instance.user, test=next_test, status="active")
                