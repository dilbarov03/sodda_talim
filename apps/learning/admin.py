from django.contrib import admin

from apps.learning.models import Lesson, Test, Question, UserLesson, UserAnswer, UserTest, EntranceQuestion, Language


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ["title", "order", "language"]
    list_filter = ["language"]
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
    list_per_page = 25
    

@admin.register(UserLesson)
class UserLessonAdmin(admin.ModelAdmin):
    list_display = ["user", "lesson", "status"]
    list_filter = ["user", "lesson", "status"]
    autocomplete_fields = ["user", "lesson"]
    list_per_page = 25


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    pass


@admin.register(UserTest)
class UserTestAdmin(admin.ModelAdmin):
    list_display = ["user", "test", "status"]
    list_filter = ["user", "test", "status"]
    autocomplete_fields = ["user", "test"]
    list_per_page = 25


@admin.register(EntranceQuestion)
class EntranceQuestionAdmin(admin.ModelAdmin):
    list_display = ["question", "correct_option", "wrong_option1", "wrong_option2", "order", "language"]
    search_fields = ["question", "correct_option"]
    list_filter = ["language"]

    def has_add_permission(self, request):
        if self.model.objects.count() >= 90:
            return False
        return super().has_add_permission(request)
    