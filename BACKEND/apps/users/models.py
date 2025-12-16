import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Custom User model with email/admission number as login"""
    
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('department_staff', 'Department Staff'),
        ('student', 'Student'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    admission_number = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True,
        help_text="Registration/Admission number for students"
    )
    full_name = models.CharField(max_length=255)
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='student',
        help_text="User role in the system"
    )
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Override username field to use email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']
    
    class Meta:
        db_table = 'users'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['admission_number']),
            models.Index(fields=['role']),
        ]
    
    def __str__(self):
        return f"{self.full_name} ({self.email})"
    
    def get_role_display_name(self):
        return dict(self.ROLE_CHOICES).get(self.role, 'Unknown')
