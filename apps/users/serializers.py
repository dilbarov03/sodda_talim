from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User

class RegisterUserSerializer(serializers.ModelSerializer):
    """Serializer for creating user objects."""

    tokens = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'image', 'password', 'phone', 'tokens')
        extra_kwargs = {'password': {'write_only': True}}

    def get_tokens(self, user):
        tokens = RefreshToken.for_user(user)
        refresh = str(tokens)
        access = str(tokens.access_token)
        data = {
            "refresh": refresh,
            "access": access
        }
        return data
    
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 6 characters")
        return value

    def create(self, validated_data):
        user = User(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            image=validated_data['image'],
            phone=validated_data['phone']
        )
        user.set_password(validated_data['password'])
        user.save()    
        return user