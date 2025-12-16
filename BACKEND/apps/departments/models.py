import uuid
from django.db import models


class Department(models.Model):
    """University department for clearance approvals"""
    
    DEPARTMENT_TYPE_CHOICES = [
        ('finance', 'Finance Office'),
        ('faculty', 'Faculty/Academic'),
        ('library', 'Library'),
        ('mess', 'Mess/Cafeteria'),
        ('hostel', 'Hostel/Residence'),
        ('workshop', 'Workshop'),
        ('sports', 'Sports & Games'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=255,
        help_text="Department name"
    )
    code = models.CharField(
        max_length=20,
        unique=True,
        help_text="Department code (e.g., FIN, LIB, MESS)"
    )
    department_type = models.CharField(
        max_length=20,
        choices=DEPARTMENT_TYPE_CHOICES,
        help_text="Type of department"
    )
    head_email = models.EmailField(
        help_text="Department head email address"
    )
    description = models.TextField(
        blank=True,
        help_text="Department description"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether department is active in the clearance process"
    )
    approval_order = models.IntegerField(
        default=0,
        help_text="Order in which this department should approve (0 = first)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'departments'
        ordering = ['approval_order', 'name']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['department_type']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.code})"
