import uuid
from django.db import models


class School(models.Model):
    """Academic School/Faculty"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=20, unique=True, help_text="School code (e.g., SCE, SBS)")
    dean_email = models.EmailField(blank=True, null=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'academic_schools'
        ordering = ['name']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.name} ({self.code})"


class AcademicDepartment(models.Model):
    """Academic department under a School (distinct from clearance departments)"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='departments')
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20, help_text="Department code (e.g., CS, ME)")
    head_email = models.EmailField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'academic_departments'
        unique_together = ('school', 'code')
        ordering = ['school__name', 'name']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.school.code}-{self.code} {self.name}"


class Course(models.Model):
    """Academic course/program under a department"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    department = models.ForeignKey(AcademicDepartment, on_delete=models.CASCADE, related_name='courses')
    code = models.CharField(max_length=30, help_text="Course code (e.g., BSC-CS)")
    name = models.CharField(max_length=255)
    duration_years = models.PositiveSmallIntegerField(default=4)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'academic_courses'
        unique_together = ('department', 'code')
        ordering = ['department__school__name', 'department__name', 'name']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"
