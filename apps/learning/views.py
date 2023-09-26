from django.db.models import Case, When, Value, BooleanField

from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Lesson, Test, Question

from .serializers import LessonListSerializer, TestDetailSerializer


class LessonListView(ListAPIView):
    serializer_class = LessonListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Lesson.objects.annotate(is_active=Case(
            When(user_lessons__user=self.request.user, then=Value(True)),
            default=Value(False),
            output_field=BooleanField()
        ))
        

class TestDetailView(RetrieveAPIView):
    queryset = Test.objects.all()
    serializer_class = TestDetailSerializer
    permission_classes = (IsAuthenticated,)
