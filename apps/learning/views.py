from django.db.models import Case, When, Value, BooleanField, F, Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Lesson, Test, UserTest, UserAnswer, EntranceQuestion, UserLesson

from .serializers import LessonListSerializer, TestDetailSerializer, UserAnswerInputSerializer, EntranceQuestionSerializer


class LessonListView(ListAPIView):
    serializer_class = LessonListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user

        # Filter lessons associated with the current user or those with no associated UserLesson
        queryset = Lesson.objects.filter(
            Q(user_lessons__user=user) | Q(user_lessons__isnull=True)
        ).distinct()

        # Annotate the queryset with the is_active field
        queryset = queryset.annotate(
            is_active=Case(
                When(user_lessons__user=user, user_lessons__lesson_id=F('id'), then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )
        )

        return queryset
        

class TestDetailView(RetrieveAPIView):
    queryset = Test.objects.all()
    serializer_class = TestDetailSerializer
    permission_classes = (IsAuthenticated,)


class UserAnswerView(CreateAPIView):
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerInputSerializer

    def perform_create(self, serializer):
        user = self.request.user  # Assuming you're using authentication
        user_answers = serializer.create(validated_data=serializer.validated_data)
        serializer.is_valid(raise_exception=True)

        # Update the user's test status based on correctness
        if user_answers:
            self.update_user_test_status(user, user_answers)

    def update_user_test_status(self, user, user_answers):
        test_ids = set(answer.question.test.id for answer in user_answers)
        for test_id in test_ids:
            user_test = UserTest.objects.get_or_create(
                user=user,
                test_id=test_id
            )[0]
            correct_answers = UserAnswer.objects.filter(
                user=user,
                question__test__id=test_id,
                is_correct=True
            ).count()

            user_test.correct_count = correct_answers
            user_test.wrong_count = user_test.test.questions.count() - correct_answers

            if user_test.correct_count == user_test.test.questions.count():
                user_test.status = UserTest.TestStatus.FINISHED
            else:
                user_test.status = UserTest.TestStatus.ACTIVE

            user_test.save()
            
            
class EntranceQuestionListView(ListAPIView):
    queryset = EntranceQuestion.objects.all()
    serializer_class = EntranceQuestionSerializer
    pagination_class = None


class AddLessonsView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    
    state_param = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'lesson_count': openapi.Schema(type=openapi.TYPE_INTEGER, description='Lesson count')
        }
    )
    
    @swagger_auto_schema(request_body=state_param)
    def post(self, request):
        user = request.user
        lesson_count = request.data.get("lesson_count")
        if not lesson_count:
            return Response({"error": "Lesson count is required"}, status=400)
        lessons = Lesson.objects.filter(order__lte=lesson_count)
        for lesson in lessons:
            UserLesson.objects.get_or_create(user=user, lesson=lesson)
            tests = lesson.tests.all()
            for test in tests:
                UserTest.objects.get_or_create(user=user, test=test, status="active")
        return Response({"message": "Lessons added successfully"}, status=201)
                
            
