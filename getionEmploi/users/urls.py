from django.urls import path
from .views import (
    RegisterView, LoginView, LogoutView, CheckAuthView,
    RequestUpdatePasswordView, VerifyOTPUpdatePasswordView,
    UpdateEmailRequestView, VerifyOTPUpdateEmailView,
    AdminOnlyView, UserOnlyView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('check-auth/', CheckAuthView.as_view(), name='check_auth'),

    path('request-update-password/', RequestUpdatePasswordView.as_view(), name='request_update_password'),
    path('verify-update-password/', VerifyOTPUpdatePasswordView.as_view(), name='verify_update_password'),

    path('request-update-email/', UpdateEmailRequestView.as_view(), name='request_update_email'),
    path('verify-update-email/', VerifyOTPUpdateEmailView.as_view(), name='verify_update_email'),

    path('admin-only/', AdminOnlyView.as_view(), name='admin_only'),
    path('user-only/', UserOnlyView.as_view(), name='user_only'),
]
