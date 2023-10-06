from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from .models import User
from .serializers import RegisterUserSerializer


class UserRegisterView(generics.CreateAPIView):
    """Handles creating and listing Users."""
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer
    parser_classes = (MultiPartParser, FormParser)

def create(self, request, *args, **kwargs):
    serializer = RegisterUserSerializer(data=request.data)
    if serializer.is_valid():
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    