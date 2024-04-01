from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import ApiKey
import secrets

Account = get_user_model()


class SignupSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'email',
            'password',
        ]

    def create(self, validated_data):
        
        account = Account.objects.create_user(
            email=validated_data.get('email'),
            password=validated_data.get('password'),
        )
        return account


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=128)

    def validate(self, attrs):
        validate_password(attrs.get('password'))
        return attrs


class ApiKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiKey
        fields = (
            'user',
            'key',
            'is_active',
        )
    def create(self, user):
       
        return ApiKeySerializer(ApiKey.objects.create(key=secrets.token_urlsafe(30), user=user))