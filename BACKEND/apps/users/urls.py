"""
URL routing for users app (authentication endpoints)
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from apps.users.views import (
    RegisterView,
    LoginView,
    LogoutView,
    UserProfileView,
    ChangePasswordView,
    CustomTokenObtainPairView,
    verify_token,
    health_check,
    UserListCreateView,
)

app_name = 'users'

urlpatterns = [
    # Authentication endpoints
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify/', verify_token, name='verify_token'),
    
    # User profile endpoints
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    
    # Health check
    path('health/', health_check, name='health_check'),

    # User management endpoint
    path('', UserListCreateView.as_view(), name='user_list_create'),
]
