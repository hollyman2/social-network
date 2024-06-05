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
            'first_name',
            'last_name',
            'login',
            'phone',
            'picture',
        ]

    def create(self, validated_data):
        
        account = Account.objects.create_user(
            email=validated_data.get('email'),
            password=validated_data.get('password'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            login=validated_data.get('login'),
            phone=validated_data.get('phone'),
            picture=validated_data.get('picture'),
        )
        return account
    
    def edit(self, data, user):
        

        if data.get('email'):
            user.email=data.get('email')
        if data.get('phone'):
            user.phone=data.get('phone')
        if data.get('picture'):
            user.picture=data.get('picture')
        if data.get('login'):
            user.login=data.get('login')
        
        user.save()
    
        return user



class LoginSerializer(serializers.Serializer):
    login = serializers.CharField()
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
       
        return ApiKeySerializer(ApiKey.objects.create(key=secrets.token_urlsafe(200), user=user))