import uuid
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from apps.clearances.models import ClearanceRequest
from apps.departments.models import Department
from apps.users.models import User
from typing import Optional


def validate_evidence_file_size(value):
    """Validate evidence file size (max 5MB)"""
    max_size_mb = 5
    if value.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"File size cannot exceed {max_size_mb}MB")


def evidence_upload_path(instance, filename):
    """Generate upload path for evidence files"""
    # Organize by department and clearance request
    dept_code = instance.department.code
    student_reg = instance.clearance_request.student.registration_number
    return f'evidence/{dept_code}/{student_reg}/{filename}'


class ClearanceApproval(models.Model):
    """Department approval for clearance request"""
    
    APPROVAL_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clearance_request = models.ForeignKey(
        ClearanceRequest,
        on_delete=models.CASCADE,
        related_name='approvals',
        help_text="Clearance request being approved"
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name='approvals',
        help_text="Department performing approval"
    )
    status = models.CharField(
        max_length=20,
        choices=APPROVAL_STATUS_CHOICES,
        default='pending',
        help_text="Approval status"
    )
    approved_by: Optional[User] = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approvals_made',
        help_text="Staff member who approved/rejected"
    )
    approval_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Date of approval/rejection"
    )
    rejection_reason: str = models.TextField(
        blank=True,
        help_text="Reason for rejection if applicable"
    )
    notes = models.TextField(
        blank=True,
        help_text="Additional notes from the approver"
    )
    evidence_file = models.FileField(
        upload_to=evidence_upload_path,
        null=True,
        blank=True,
        validators=[validate_evidence_file_size],
        help_text="Evidence document for clearance (max 5MB)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'clearance_approvals'
        ordering = ['clearance_request', 'department__approval_order']
        unique_together = ['clearance_request', 'department']
        indexes = [
            models.Index(fields=['clearance_request']),
            models.Index(fields=['department']),
            models.Index(fields=['status']),
            models.Index(fields=['approval_date']),
        ]
    
    def __str__(self):
        return f"{self.department.code} - {self.clearance_request.student} ({self.status})"
    
    def approve(self, user: User, notes: str = "") -> None:
        """Approve clearance"""
        self.status = 'approved'
        self.approved_by = user
        self.approval_date = timezone.now()
        self.notes = notes
        self.save()
    
    def reject(self, user: User, rejection_reason: str, notes: str = "") -> None:
        """Reject clearance"""
        self.status = 'rejected'
        self.approved_by = user
        self.approval_date = timezone.now()
        self.rejection_reason = rejection_reason
        self.notes = notes
        self.save()
