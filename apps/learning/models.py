from django.db import models
from django.db.models import Q

from apps.common.models import BaseModel


class Lesson(BaseModel):
    title = models.CharField(max_length=255, verbose_name="Title")
    body = models.TextField(verbose_name="Body")
    order = models.IntegerField(verbose_name="Order", unique=True)
    
    class Meta:
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"
        ordering = ["order"]
        
    def __str__(self):
        return self.title


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
    order = models.IntegerField(verbose_name="Order", default=1)
    
    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"
        ordering = ["order"]

    def __str__(self):
        return self.question[:50] + "..."


class UserLesson(BaseModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, verbose_name="User", 
                             related_name="user_lessons")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name="Lesson",
                               related_name="user_lessons")
    
    class Meta:
        verbose_name = "User Lesson"
        verbose_name_plural = "User Lessons"
        
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) 
        


class UserTest(BaseModel):
    
    class TestStatus(models.TextChoices):
        LOCKED = "locked", "Locked"
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
        
    def save(self, *args, **kwargs):
        test = self.test
        lesson = test.lesson
        if self.status == "finished" and test == lesson.tests.last():        
            # check if user has active subscription
            if self.user.has_active_subscription():
                # if it is, then add the next lesson to the UserLesson model
                next_lesson = Lesson.objects.filter(order=lesson.order + 1).first()
                if next_lesson:
                    UserLesson.objects.get_or_create(user=self.user, lesson=next_lesson)
                    # make first test of this lesson active to the user
                    test = next_lesson.tests.first()
                    if test and not UserTest.objects.filter(user=self.user, test=test).exists():
                        UserTest.objects.create(user=self.user, test=test, status="active") 
                    
        elif self.status == "finished" and test != lesson.tests.last():
            # if it is, then add the next test to the UserTest model
            next_test = Test.objects.filter(lesson=lesson).filter(Q(order__gt=test.order) | Q(id__gt=test.id)).first()
            if next_test:
                if not UserTest.objects.filter(user=self.user, test=next_test).exists():
                    UserTest.objects.get_or_create(user=self.user, test=next_test, status="active")
                    
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
    question = models.TextField(verbose_name="Question")
    correct_option = models.CharField(max_length=255, verbose_name="Correct Option")
    wrong_option = models.CharField(max_length=255, verbose_name="Wrong Option", null=True, blank=True)
    order = models.IntegerField(verbose_name="Order", default=1)
    
    class Meta:
        verbose_name = "Entrance Question"
        verbose_name_plural = "Entrance Questions"
        ordering = ["order"]

    def __str__(self):
        return self.question[:50] + "..."
    
    