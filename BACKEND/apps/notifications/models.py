import uuid
from django.db import models
from django.utils import timezone
from apps.users.models import User


class Notification(models.Model):
    """User notifications for clearance status updates"""

    NOTIFICATION_TYPES = [
        ('clearance_submitted', 'Clearance Submitted'),
        ('clearance_approved', 'Clearance Approved'),
        ('clearance_rejected', 'Clearance Rejected'),
        ('approval_pending', 'Approval Pending'),
        ('payment_received', 'Payment Received'),
        ('payment_verified', 'Payment Verified'),
        ('payment_failed', 'Payment Failed'),
        ('general', 'General'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications',
        help_text="User receiving notification",
    )
    notification_type = models.CharField(
        max_length=50,
        choices=NOTIFICATION_TYPES,
        default='general',
        help_text="Type of notification",
    )
    title = models.CharField(
        max_length=255,
        help_text="Notification title",
    )
    message = models.TextField(
        help_text="Notification message",
    )
    clearance = models.ForeignKey(
        'clearances.ClearanceRequest',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='notifications',
        help_text="Related clearance request",
    )
    approval = models.ForeignKey(
        'approvals.ClearanceApproval',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='notifications',
        help_text="Related clearance approval",
    )
    payment = models.ForeignKey(
        'finance.Payment',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='notifications',
        help_text="Related payment record",
    )
    is_read = models.BooleanField(
        default=False,
        help_text="Whether notification has been read",
    )
    read_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When notification was read",
    )
    sent_via_email = models.BooleanField(
        default=False,
        help_text="Whether notification email was sent",
    )
    email_sent_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When notification email was sent",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient']),
            models.Index(fields=['is_read']),
            models.Index(fields=['notification_type']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.title} - {self.recipient.email}"

    def mark_as_read(self):
        """Mark notification as read"""
        self.is_read = True
        self.read_at = timezone.now()
        self.save(update_fields=['is_read', 'read_at'])

    def mark_email_sent(self):
        """Mark notification email as sent"""
        self.sent_via_email = True
        self.email_sent_at = timezone.now()
        self.save(update_fields=['sent_via_email', 'email_sent_at'])
