from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import CustomUser


class RegistrationSerializer(serializers.ModelSerializer):
    """
    serializer for user registration
    """
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    class Meta:
        model = CustomUser
        fields = ('username', 'email')
    
    def create(self, validated_data):
        user = CustomUser.objects.create(
        username=validated_data['username'],
        email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    """
    serializer for user login
    """
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        try:
            user = CustomUser.objects.get(username=data['username'])
        except Exception:
            raise serializers.ValidationError(f"User does not exists!")
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Please provide correct password!") 
        return data


class CustomUserSerializer(serializers.ModelSerializer):
    """
    serializer for CustomUser model
    """
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'is_online')
        

class StartChatSerializer(serializers.Serializer):
    """
    serializer for starting the chat view
    required fields = ['username']
    """ 
    username = serializers.CharField(required=True)
    
    def validate(self, data):
        try:
            user = CustomUser.objects.get(username=data['username'])
        except Exception:
            raise serializers.ValidationError(f"User does not exists!")
        return data


