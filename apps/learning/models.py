from django.db import models
from django.db.models import Q

from apps.common.models import BaseModel

class Language(BaseModel):
    name = models.CharField(max_length=255)
    
    class Meta:
        verbose_name = "Language"
        verbose_name_plural = "Languages"
        
    def __str__(self) -> str:
        return self.name


class Lesson(BaseModel):
    title = models.CharField(max_length=255, verbose_name="Title")
    subtitle = models.CharField(max_length=255, verbose_name="Subtitle", null=True, blank=True)
    body = models.TextField(verbose_name="Body")
    language = models.ForeignKey(Language, on_delete=models.CASCADE, verbose_name="Language", null=True)
    order = models.IntegerField(verbose_name="Order")
    
    class Meta:
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"
        ordering = ["order"]
        unique_together = ["language", "order"]
        
    def __str__(self):
        return f"{self.title} | {self.language}"
    

class Test(BaseModel):
    class TestType(models.TextChoices):
        LISTENING = "listening", "Listening"
        SPEAKING = "speaking", "Speaking"
    
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name="Lesson",
                               related_name="tests")
    test_type = models.CharField(max_length=255, choices=TestType.choices, verbose_name="Test Type")
    order = models.IntegerField(verbose_name="Order", default=1)
    
    class Meta:
        verbose_name = "Test"
        verbose_name_plural = "Tests"
        ordering = ["order", "created_at"]
        
    def __str__(self):
        return f"{self.lesson.title} - {self.test_type}"
    
    def get_status(self, user):
        try:
            user_test = self.user_tests.get(user=user, test=self)
            return user_test.status
        except UserTest.DoesNotExist:
            return UserTest.TestStatus.LOCKED

class Question(BaseModel):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name="Test",
                             related_name="questions")
    question = models.TextField(verbose_name="Question")
    correct_option = models.CharField(max_length=255, verbose_name="Correct Option")
    wrong_option = models.CharField(max_length=255, verbose_name="Wrong Option", null=True, blank=True)
    audio = models.FileField(upload_to="audio", verbose_name="Audio", null=True, blank=True)
    order = models.IntegerField(verbose_name="Order", default=1)
    
    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"
        ordering = ["order"]

    def __str__(self):
        return self.question[:50] + "..."


class UserLesson(BaseModel):
    class LessonStatus(models.TextChoices):
        OPEN = "open", "Open"
        CLOSED = "closed", "Closed"
        
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, verbose_name="User", 
                             related_name="user_lessons")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name="Lesson",
                               related_name="user_lessons")
    status = models.CharField(max_length=255, choices=LessonStatus.choices, verbose_name="Status",
                                default=LessonStatus.CLOSED)
    
    class Meta:
        verbose_name = "User Lesson"
        verbose_name_plural = "User Lessons"
        

class UserTest(BaseModel):
    
    class TestStatus(models.TextChoices):
        LOCKED = "locked", "Locked" # because of the lesson
        CLOSED = "closed", "Closed" # because of the subscription
        ACTIVE = "active", "Active"
        FINISHED = "finished", "Finished"
    
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, verbose_name="User", 
                             related_name="user_tests")
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name="Test",
                             related_name="user_tests")
    status = models.CharField(max_length=255, choices=TestStatus.choices, verbose_name="Status",
                              default=TestStatus.LOCKED)
    correct_count = models.IntegerField(verbose_name="Correct Count", default=0, null=True, blank=True)
    wrong_count = models.IntegerField(verbose_name="Wrong Count", default=0, null=True, blank=True)
    
    class Meta:
        verbose_name = "User Test"
        verbose_name_plural = "User Tests"
        ordering = ("id", )
        
    def save(self, *args, **kwargs):
        test = self.test
        lesson = test.lesson
        
        if not hasattr(kwargs.get('request'), 'user'):
            if self.status == "finished" and test == lesson.tests.last():        
                next_lesson = Lesson.objects.filter(language=lesson.language, order=lesson.order + 1).first()
                if next_lesson and next_lesson.order > 3:
                    if self.user.has_active_subscription():
                        lesson_status = "open"
                        test_status = "active"
                    else:
                        lesson_status = "closed"
                        test_status = "closed"    
                    
                    user_lesson, created = UserLesson.objects.get_or_create(user=self.user, lesson=next_lesson)

                    # If the object is created, set its status
                    if created:
                        user_lesson.status = lesson_status
                        user_lesson.save()
                    else:
                        # If the object already exists, update its status
                        user_lesson.status = lesson_status
                        user_lesson.save()
                    
                    test = next_lesson.tests.first()
                    if test and not UserTest.objects.filter(user=self.user, test=test).exists():
                        UserTest.objects.create(user=self.user, test=test, status=test_status) 
                        
            elif self.status == "finished" and test != lesson.tests.last():
                # if it is, then add the next test to the UserTest model
                next_test = Test.objects.filter(lesson=lesson).filter(Q(order__gt=test.order) | Q(id__gt=test.id)).first()
                if next_test:
                    user_test = UserTest.objects.filter(user=self.user, test=next_test).first()
                    if not user_test:
                        UserTest.objects.create(user=self.user, test=next_test, status="active")
                    else:
                        user_test.status = "active"
                        user_test.save()
    

                    
        super().save(*args, **kwargs)
            
        
class UserAnswer(BaseModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, verbose_name="User", 
                             related_name="user_questions")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Question",
                                 related_name="user_questions")
    is_correct = models.BooleanField(verbose_name="Correct")
    user_answer = models.CharField(max_length=255, verbose_name="User Answer")
    
    
    class Meta:
        verbose_name = "User Answer"
        verbose_name_plural = "User Answers"


class EntranceQuestion(BaseModel):
    language = models.ForeignKey(Language, on_delete=models.CASCADE, verbose_name="Language", null=True)
    question = models.TextField(verbose_name="Question")
    correct_option = models.CharField(max_length=255, verbose_name="Correct Option")
    wrong_option1 = models.CharField(max_length=255, verbose_name="Wrong Option 1", null=True, blank=True)
    wrong_option2 = models.CharField(max_length=255, verbose_name="Wrong Option 2", null=True, blank=True)
    order = models.IntegerField(verbose_name="Order", default=1)
    
    class Meta:
        verbose_name = "Entrance Question"
        verbose_name_plural = "Entrance Questions"
        ordering = ["order"]
        unique_together = ["language", "order"]

    def __str__(self):
        return self.question[:50] + "..."
    
    