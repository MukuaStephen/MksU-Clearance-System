import uuid
from django.db import models
from apps.users.models import User


class AuditLog(models.Model):
    """Audit trail for all system actions"""
    
    ACTION_CHOICES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('approve', 'Approve'),
        ('reject', 'Reject'),
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    actor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='audit_logs_created',
        help_text="User performing the action"
    )
    action = models.CharField(
        max_length=20,
        choices=ACTION_CHOICES,
        help_text="Action type"
    )
    entity = models.CharField(
        max_length=100,
        help_text="Entity/Model name (e.g., 'ClearanceRequest', 'User')"
    )
    entity_id = models.CharField(
        max_length=100,
        help_text="ID of the entity"
    )
    description = models.TextField(
        blank=True,
        help_text="Action description"
    )
    changes = models.JSONField(
        default=dict,
        blank=True,
        help_text="JSON object containing before/after values"
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        help_text="IP address of the requester"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'audit_logs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['actor']),
            models.Index(fields=['action']),
            models.Index(fields=['entity']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.action} - {self.entity} by {self.actor}"
    
    @staticmethod
    def log_action(actor, action, entity, entity_id, description="", changes=None, ip_address=None):
        """Create an audit log entry"""
        return AuditLog.objects.create(
            actor=actor,
            action=action,
            entity=entity,
            entity_id=str(entity_id),
            description=description,
            changes=changes or {},
            ip_address=ip_address
        )
