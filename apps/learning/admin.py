from django.contrib import admin

from apps.learning.models import Lesson, Test, Question, UserLesson, UserAnswer, UserTest


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ["title", "order"]
    search_fields = ["title"]


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0
    

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ["lesson", "test_type", "order"]
    list_filter = ["lesson", "test_type"]
    search_fields = ["lesson__title", "test_type"]
    inlines = [QuestionInline]
    autocomplete_fields = ["lesson"]
    

@admin.register(UserLesson)
class UserLessonAdmin(admin.ModelAdmin):
    pass


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    pass


@admin.register(UserTest)
class UserTestAdmin(admin.ModelAdmin):
    pass

