from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Admin interface for Notification model"""

    list_display = (
        'recipient',
        'notification_type',
        'title',
        'is_read',
        'sent_via_email',
        'created_at',
    )
    list_filter = (
        'notification_type',
        'is_read',
        'sent_via_email',
        'created_at',
    )
    search_fields = (
        'recipient__email',
        'title',
        'message',
    )
    readonly_fields = (
        'id',
        'created_at',
        'updated_at',
        'read_at',
        'email_sent_at',
    )

    fieldsets = (
        ('Recipient', {'fields': ('id', 'recipient')}),
        ('Content', {'fields': ('notification_type', 'title', 'message')}),
        (
            'Related Objects',
            {'fields': ('clearance', 'approval', 'payment')},
        ),
        (
            'Delivery Status',
            {'fields': ('sent_via_email', 'email_sent_at')},
        ),
        ('Read Status', {'fields': ('is_read', 'read_at')}),
        (
            'Timestamps',
            {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)},
        ),
    )
