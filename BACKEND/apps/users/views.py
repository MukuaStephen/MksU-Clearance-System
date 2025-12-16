"""
Views for User authentication and management
"""
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import login, logout

from apps.users.models import User
from apps.users.serializers import (
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
    ChangePasswordSerializer,
    TokenSerializer
)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom JWT token serializer to include user data"""
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add custom claims
        token['email'] = user.email
        token['role'] = user.role
        token['full_name'] = user.full_name
        token['admission_number'] = user.admission_number
        
        return token
    
    def validate(self, attrs):
        """Override to use email instead of username"""
        # Get email from username field (we store email as username)
        data = super().validate(attrs)
        
        # Add user data to response
        data['user'] = UserSerializer(self.user).data
        
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom JWT token view"""
    serializer_class = CustomTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    """
    API endpoint for user registration
    POST /api/auth/register/
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """
    API endpoint for user login
    POST /api/auth/login/
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        # Add custom claims
        refresh['email'] = user.email
        refresh['role'] = user.role
        refresh['full_name'] = user.full_name
        
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'message': 'Login successful'
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """
    API endpoint for user logout
    POST /api/auth/logout/
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            return Response({
                'message': 'Logout successful'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    API endpoint to get or update user profile
    GET/PUT /api/auth/profile/
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class ChangePasswordView(generics.UpdateAPIView):
    """
    API endpoint to change user password
    PUT /api/auth/change-password/
    """
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            'message': 'Password changed successfully'
        }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def verify_token(request):
    """
    API endpoint to verify JWT token validity
    GET /api/auth/verify/
    """
    return Response({
        'valid': True,
        'user': UserSerializer(request.user).data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def health_check(request):
    """
    API health check endpoint
    GET /api/health/
    """
    return Response({
        'status': 'healthy',
        'message': 'MksU Clearance System API is running'
    }, status=status.HTTP_200_OK)
