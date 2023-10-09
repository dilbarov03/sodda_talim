from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from apps.confirmation_service.models import SMSConfirmation

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
    

class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'image')


class ChangePasswordSerializer(serializers.Serializer):
    # Serializer for password change endpoint.
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct")
        return value
    
    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 6 characters")
        return value

    

class UpdatePhoneSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)
    signature = serializers.CharField(required=True)

    def validate_signature(self, value):
        confirm_signature = SMSConfirmation.objects.filter(signature=value).first()
        if confirm_signature is None:
            raise serializers.ValidationError("Wrong signature")
        if confirm_signature.confirmed is False:
            raise serializers.ValidationError(f"Signature is not confirmed!")
        confirm_signature.delete()

    def update_user_phone(self):
        phone_number = self.validated_data["phone_number"]
        user = self.context['request'].user
        user.phone = phone_number
        user.save(update_fields=['phone'])
        