import uuid
import re
from django.db import models
from django.core.exceptions import ValidationError
from apps.users.models import User
from apps.academics.models import School, AcademicDepartment, Course


def validate_registration_number(value):
    """Validate registration number format: SCHOOL/DEPT/NNNN/YYYY"""
    pattern = r'^[A-Z]{2,10}/[A-Z]{2,10}/\d{4}/\d{4}$'
    if not re.match(pattern, value):
        raise ValidationError(
            f"Registration number must follow format SCHOOL/DEPT/NNNN/YYYY (e.g., SCE/CS/0001/2024)"
        )


class Student(models.Model):
    """Student profile and academic information"""
    
    ELIGIBILITY_STATUS_CHOICES = [
        ('eligible', 'Eligible'),
        ('ineligible', 'Ineligible'),
        ('pending', 'Pending Review'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student_profile',
        help_text="Link to user account"
    )
    registration_number = models.CharField(
        max_length=50,
        unique=True,
        validators=[validate_registration_number],
        help_text="Student registration/admission number (format: SCHOOL/DEPT/NNNN/YYYY)"
    )
    admission_year = models.IntegerField(
        null=True,
        blank=True,
        help_text="Year of admission (auto-extracted from registration number)"
    )
    # Normalized academic relations (kept alongside legacy text fields for compatibility)
    school = models.ForeignKey(
        School,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students',
        help_text="Academic School/Faculty"
    )
    department = models.ForeignKey(
        AcademicDepartment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students',
        help_text="Academic Department"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students',
        help_text="Academic Course/Program"
    )
    faculty = models.CharField(
        max_length=255,
        help_text="Faculty/School name"
    )
    program = models.CharField(
        max_length=255,
        help_text="Program/Course name"
    )
    graduation_year = models.IntegerField(
        help_text="Expected graduation year"
    )
    eligibility_status = models.CharField(
        max_length=20,
        choices=ELIGIBILITY_STATUS_CHOICES,
        default='pending',
        help_text="Academic eligibility status"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'students'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['registration_number']),
            models.Index(fields=['user']),
            models.Index(fields=['eligibility_status']),
            models.Index(fields=['admission_year']),
        ]
    
    def __str__(self):
        return f"{self.user.full_name} - {self.registration_number}"
    
    def parse_registration_number(self):
        """Parse registration number and return components"""
        pattern = r'^([A-Z]{2,10})/([A-Z]{2,10})/(\d{4})/(\d{4})$'
        match = re.match(pattern, self.registration_number)
        if match:
            return {
                'school_code': match.group(1),
                'department_code': match.group(2),
                'sequence': match.group(3),
                'admission_year': int(match.group(4))
            }
        return None
    
    def save(self, *args, **kwargs):
        """Auto-extract admission_year from registration_number on save"""
        if self.registration_number and not self.admission_year:
            parsed = self.parse_registration_number()
            if parsed:
                self.admission_year = parsed['admission_year']
        super().save(*args, **kwargs)
