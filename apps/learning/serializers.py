from rest_framework import serializers

from .models import Lesson, Test, Question, UserAnswer, UserTest, EntranceQuestion


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
    user_answer = serializers.SerializerMethodField()
    class Meta:
        model = Question
        fields = ("id", "question", "correct_option", "wrong_option", "user_answer")
        
    def get_user_answer(self, obj):
        user = self.context["request"].user
        user_answer = UserAnswer.objects.filter(user=user, question=obj).first()
        if user_answer:
            return {
                "id": user_answer.id,
                "user_answer": user_answer.user_answer,
                "is_correct": user_answer.is_correct
            }
        return None
        

class TestDetailSerializer(serializers.ModelSerializer):
    questions = QuestionListSerializer(many=True)
    status = serializers.SerializerMethodField()
    test_result = serializers.SerializerMethodField()
    
    class Meta:
        model = Test
        fields = ("id", "test_type", "status","questions", "test_result")

    def get_status(self, obj):
        return obj.get_status(self.context["request"].user)
    
    def get_test_result(self, obj):
        user = self.context["request"].user
        user_test = UserTest.objects.filter(user=user, test=obj).first()
        if user_test:
            return {
                "id": user_test.id,
                "status": user_test.status,
                "correct_count": user_test.correct_count,
                "wrong_count": user_test.wrong_count
            }
        return None


class UserAnswerInputSerializer(serializers.Serializer):
    user_answers = serializers.ListField(child=serializers.DictField())
    
    def validate_user_answers(self, value):
        if not value:
            raise serializers.ValidationError("User answers cannot be empty")
        for answer in value:
            if not answer.get("question_id"):
                raise serializers.ValidationError("Question ID is required")
            if Question.objects.filter(id=answer.get("question_id")).count() == 0:
                raise serializers.ValidationError("Invalid Question ID")
            if not answer.get("user_answer"):
                raise serializers.ValidationError("User answer is required")
        return value

    def create(self, validated_data):
        user = self.context['request'].user  # Assuming you're using authentication
        user_answers_data = validated_data.get('user_answers', [])
        
        user_answer_instances = []
        for answer_data in user_answers_data:
            question_id = answer_data.get('question_id')
            question = Question.objects.filter(pk=question_id).first()
            user_answer = answer_data.get('user_answer')
            
            test = question.test
            user_test = UserTest.objects.filter(user=user, test=test).first()
            if user_test and user_test.status == "finished":
                raise serializers.ValidationError("You have already finished this test")   
            else:
                UserAnswer.objects.filter(user=user, question=question).delete()

                user_answer_instance = UserAnswer.objects.create(
                    user=user,
                    question=question,
                    user_answer=user_answer,
                    is_correct=user_answer == question.correct_option
                )
                user_answer_instances.append(user_answer_instance)

        return user_answer_instances
    
    def to_representation(self, instance):
        test = Question.objects.filter(id=instance["user_answers"][0]["question_id"]).first().test
        return TestDetailSerializer(test, context=self.context).data
    

class UserTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTest
        fields = ("id", "user", "test", "status")


class EntranceQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntranceQuestion
        fields = ("id", "question", "correct_option", "wrong_option")
