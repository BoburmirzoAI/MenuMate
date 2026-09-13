from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.users.views.auth import (
    ChangePasswordAPIView,
    ConfirmEmailVerificationAPIView,
    DeleteAccountAPIView,
    ForgotPasswordAPIView,
    ResetPasswordAPIView,
    SendEmailVerificationAPIView,
)
from apps.users.views.me import MeAPIView
from apps.users.views.register_login import (
    LoginAPIView,
    LogoutAPIView,
    RegisterAPIView,
)

app_name = 'users'

urlpatterns = [
    # ---- Auth ----
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    # ---- Password ----
    path('me/change-password/', ChangePasswordAPIView.as_view(), name='change-password'),
    path('forgot-password/', ForgotPasswordAPIView.as_view(), name='forgot-password'),
    path('reset-password/', ResetPasswordAPIView.as_view(), name='reset-password'),

    # ---- Email verification ----
    path('verify-email/send/',
         SendEmailVerificationAPIView.as_view(), name='verify-email-send'),
    path('verify-email/confirm/',
         ConfirmEmailVerificationAPIView.as_view(), name='verify-email-confirm'),

    # ---- Profile ----
    path('me/', MeAPIView.as_view(), name='me'),

    # ---- Delete ----
    path('me/delete/', DeleteAccountAPIView.as_view(), name='me-delete'),
]
