from django.urls import path
from .views import RegisterView, LoginView, LogoutView, AdminOnlyView, UserOnlyView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('admin-only/', AdminOnlyView.as_view(), name='admin_only'),
    path('user-only/', UserOnlyView.as_view(), name='user_only'),
]
