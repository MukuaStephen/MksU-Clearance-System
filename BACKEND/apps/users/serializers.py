"""
Serializers for User authentication and management
"""
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model - used for user profile display"""
    
    role_display = serializers.CharField(source='get_role_display_name', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'admission_number', 'full_name', 
            'role', 'role_display', 'is_active', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'role_display']


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = User
        fields = [
            'email', 'admission_number', 'full_name',
            'password', 'password_confirm', 'role'
        ]
        extra_kwargs = {
            'role': {'required': False, 'default': 'student'}
        }
    
    def validate(self, attrs):
        """Validate password confirmation"""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                "password": "Password fields didn't match."
            })
        return attrs
    
    def validate_email(self, value):
        """Validate email uniqueness"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email already exists.")
        return value
    
    def validate_admission_number(self, value):
        """Validate admission number uniqueness"""
        if User.objects.filter(admission_number=value).exists():
            raise serializers.ValidationError("User with this admission number already exists.")
        return value
    
    def create(self, validated_data):
        """Create new user with hashed password"""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        
        # Set default role if not provided
        if 'role' not in validated_data:
            validated_data['role'] = 'student'
        
        # Create user with username = email
        user = User.objects.create_user(
            username=validated_data['email'],
            **validated_data
        )
        user.set_password(password)
        user.save()
        
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    
    def validate(self, attrs):
        """Validate user credentials"""
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            # Authenticate using email (username field stores email)
            user = authenticate(
                request=self.context.get('request'),
                username=email,
                password=password
            )
            
            if not user:
                raise serializers.ValidationError(
                    'Unable to log in with provided credentials.',
                    code='authorization'
                )
            
            if not user.is_active:
                raise serializers.ValidationError(
                    'User account is disabled.',
                    code='authorization'
                )
        else:
            raise serializers.ValidationError(
                'Must include "email" and "password".',
                code='authorization'
            )
        
        attrs['user'] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for changing password"""
    
    old_password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    new_password_confirm = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    
    def validate(self, attrs):
        """Validate passwords match"""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({
                "new_password": "Password fields didn't match."
            })
        return attrs
    
    def validate_old_password(self, value):
        """Validate old password is correct"""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct.")
        return value
    
    def save(self, **kwargs):
        """Update user password"""
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class TokenSerializer(serializers.Serializer):
    """Serializer for JWT token response"""
    
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    user = UserSerializer(read_only=True)
