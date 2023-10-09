from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from apps.confirmation_service.models import SMSConfirmation
from .utils import is_password_valid

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
        
        
class RecoverPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    signature = serializers.CharField(required=True)

    def validate(self, attrs):
        password = attrs.get('password', None)
        phone = attrs.get('phone', None)
        signature = attrs.get('signature', None)

        if is_password_valid(password)[0]:
            user = User.objects.filter(phone=phone).first()
            if user:
                confirm_signature = SMSConfirmation.objects.filter(signature=signature).first()
                if confirm_signature is None:
                    raise serializers.ValidationError("Wrong signature")
                if confirm_signature.confirmed is False:
                    raise serializers.ValidationError(f"{phone} is not confirmed!")


                user.set_password(password)
                user.save()
                confirm_signature.delete()

                attrs['user'] = user
                return attrs

            else:
                raise serializers.ValidationError({'error': f"Bu {phone } bilan foydalanuvchi mavjud emas"})

        else:
            raise serializers.ValidationError({'error': is_password_valid(password)[1]})
