from django.db import models

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
        ordering = ["order"]
        
    def __str__(self):
        return self.test_type
    
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
