import uuid
from django.db import models
from apps.students.models import Student


class ClearanceRequest(models.Model):
    """Student clearance request"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='clearance_requests',
        help_text="Student requesting clearance"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        help_text="Current clearance status"
    )
    submission_date = models.DateTimeField(
        auto_now_add=True,
        help_text="Date clearance was submitted"
    )
    completion_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Date clearance was completed/rejected"
    )
    rejection_reason = models.TextField(
        blank=True,
        help_text="Reason if clearance was rejected"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'clearance_requests'
        ordering = ['-submission_date']
        indexes = [
            models.Index(fields=['student']),
            models.Index(fields=['status']),
            models.Index(fields=['submission_date']),
        ]
    
    def __str__(self):
        return f"Clearance Request - {self.student} ({self.status})"
    
    def get_completion_percentage(self):
        """Calculate percentage of approvals completed"""
        from apps.departments.models import Department
        total_depts = Department.objects.filter(is_active=True).count()
        if total_depts == 0:
            return 0
        
        from apps.approvals.models import ClearanceApproval
        approved = self.approvals.filter(
            status__in=['approved', 'rejected']
        ).count()
        return int((approved / total_depts) * 100)
