from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.utils.functional import SimpleLazyObject
from django.contrib.auth.models import AnonymousUser

from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from django.contrib.auth import get_user_model
from accounts_api.models import  ApiKey
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.shortcuts import get_object_or_404
from django.conf import settings


User = get_user_model()

def get_user(apikey):
    key = apikey
    apikey = get_object_or_404(ApiKey, key=key)
    user = User.objects.get(id=apikey.user.id)
    
    return user

def get_user_jwt(request):
    
    user = None
    try:
        user_jwt = JWTAuthentication().authenticate(Request(request))
        if user_jwt is not None:
            # store the first part from the tuple (user, obj)
            user = user_jwt[0]
            return user

    except:
        return True

     

class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.headers.get('Apikey'):
            
            api_key = request.headers.get('Apikey')
            try:
                user = get_user(apikey=api_key)
                request._force_auth_user = user
            except:
                response = Response(
                data='apikey недействителен',
                status=status.HTTP_403_FORBIDDEN
                )
                response.accepted_renderer = JSONRenderer()
                response.accepted_media_type = "application/json"
                response.renderer_context = {}
                response.render()
                return response
        else:
            
            
            if not SimpleLazyObject(lambda : get_user_jwt(request)) and request.path not in settings.AUTHENTICATE_URLS and 'admin' not in request.path.split('/')[1]:
            
                response = Response(
                data='вы должны быть авторизованны',
                status=status.HTTP_400_BAD_REQUEST
                )
                response.accepted_renderer = JSONRenderer()
                response.accepted_media_type = "application/json"
                response.renderer_context = {}
                response.render()
                return response

        response = self.get_response(request)
        return response
