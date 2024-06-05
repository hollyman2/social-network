from django.urls import path
from . import views

app_name = 'accounts_api'

urlpatterns = [
    path('signup/', views.SignUpAPIView.as_view(), name='signup'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('activate/<uidb64>/<token>/', views.ActivateAccountAPIView.as_view(), name='activate'),
    path('token/refresh/', views.RefreshTokenAPIView.as_view(), name='refresh'),
    path('apikey/', views.CreateApiKeyAPIView.as_view(), name='genarate_api_key'),
    path(
        'password-reset/',
        views.PasswordResetAPIView.as_view(),
        name='password_reset',
    ),
    path(
        'password-reset/<uidb64>/<token>/',
        views.PasswordResetConfirmAPIView.as_view(),
        name='password_reset_confirm'
    ),
    path(
        'email-change/',
        views.EmailChangeAPIView.as_view(),
        name='request-email-change'),
    path(
        'confirm-email-change/<uidb64>/<token>/',
        views.EmailChangeConfirmAPIView.as_view(),
        name='email_change_confirm'
    ),
    path('profile/', views.MyProfileView.as_view(), name='my_profile'),
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
]
