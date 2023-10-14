from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view

from .utils import check_number
from .models import User
from .serializers import RegisterUserSerializer, UpdateProfileSerializer, ChangePasswordSerializer, UpdatePhoneSerializer, RecoverPasswordSerializer, GetProfileSerializer


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


class ProfileGetView(generics.RetrieveAPIView):
    serializer_class = GetProfileSerializer
    permission_classes = (IsAuthenticated, )
    
    def get_object(self):
        return self.request.user


class UpdateProfileView(generics.UpdateAPIView):
    """Handles updating a user's profile."""
    queryset = User.objects.all()
    serializer_class = UpdateProfileSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated,)
    

class ChangePasswordView(generics.GenericAPIView):
    """Handles changing a user's password."""
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = request.user
            user.set_password(serializer.data.get("new_password"))
            user.save()
            return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdatePhoneView(generics.CreateAPIView):
    """Handles updating a user's phone."""
    serializer_class = UpdatePhoneSerializer
    permission_classes = (IsAuthenticated,)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        success = False
        if serializer.is_valid(raise_exception=True):
            serializer.update_user_phone()
            success = True
        return Response({"success": success})


@api_view(['GET'])
def check_phone_number(request, phone_number):
    if not phone_number:
        return Response({"message": "Number is not given", "exists": False}, status=status.HTTP_400_BAD_REQUEST)
    is_valid = check_number("+" + phone_number)
    if not is_valid:
        return Response({"message": "Invalid phone format", "exists": False},
                        status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(phone="+" + phone_number).exists():
        return Response({"message": "User with this phone number already exists", "exists": True}, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_200_OK, data={"message": "Success","exists": False})


class RecoverPasswordView(generics.CreateAPIView):
    serializer_class = RecoverPasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            success = True
            return Response({"success": success})
