from rest_framework import serializers

from .models import Lesson, Test, Question


class TestListSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    class Meta:
        model = Test
        fields = ("id", "test_type", "status")
        
    def get_status(self, obj):
        return obj.get_status(self.context["request"].user)


class LessonListSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField()
    tests = TestListSerializer(many=True)
    class Meta:
        model = Lesson
        fields = ("id", "title", "body", "is_active", "tests")


class QuestionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ("id", "question", "correct_option", "wrong_option")
        

class TestDetailSerializer(serializers.ModelSerializer):
    questions = QuestionListSerializer(many=True)
    status = serializers.SerializerMethodField()
    
    class Meta:
        model = Test
        fields = ("id", "test_type", "status","questions")

    def get_status(self, obj):
        return obj.get_status(self.context["request"].user)
