from django.urls import path
from . import views

app_name = 'accounts_api'

urlpatterns = [
    path('signup/', views.SignUpAPIView.as_view(), name='signup'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('activate/<uidb64>/<token>/', views.ActivateAccountAPIView.as_view(), name='activate'),
    path('token/refresh/', views.RefreshTokenAPIView.as_view(), name='refresh'),
    path('apikey/', views.CreateApiKeyAPIView.as_view(), name='genarate_api_key')
]
