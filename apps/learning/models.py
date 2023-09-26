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


class Test(BaseModel):
    class TestType(models.TextChoices):
        LISTENING = "listening", "Listening"
        SPEAKING = "speaking", "Speaking"
    
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name="Lesson")
    test_type = models.CharField(max_length=255, choices=TestType.choices, verbose_name="Test Type")
    order = models.IntegerField(verbose_name="Order", default=1)
    
    class Meta:
        verbose_name = "Test"
        verbose_name_plural = "Tests"
        ordering = ["order"]
