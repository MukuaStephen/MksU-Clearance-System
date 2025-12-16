"""
Serializers for Notification management
"""
from rest_framework import serializers
from apps.notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """
    Full serializer for notification CRUD operations
    """
    recipient_name = serializers.CharField(source='recipient.full_name', read_only=True)
    recipient_email = serializers.CharField(source='recipient.email', read_only=True)
    
    class Meta:
        model = Notification
        fields = [
            'id',
            'recipient',
            'recipient_name',
            'recipient_email',
            'notification_type',
            'title',
            'message',
            'clearance',
            'approval',
            'payment',
            'is_read',
            'read_at',
            'sent_via_email',
            'email_sent_at',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'id',
            'is_read',
            'read_at',
            'sent_via_email',
            'email_sent_at',
            'created_at',
            'updated_at'
        ]


class NotificationListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing notifications
    """
    class Meta:
        model = Notification
        fields = [
            'id',
            'notification_type',
            'title',
            'message',
            'is_read',
            'created_at'
        ]
        read_only_fields = fields


class NotificationCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating notifications
    """
    recipient_id = serializers.UUIDField()
    
    class Meta:
        model = Notification
        fields = [
            'id',
            'recipient_id',
            'notification_type',
            'title',
            'message',
            'clearance',
            'approval',
            'payment'
        ]
        read_only_fields = ['id']
    
    def validate_recipient_id(self, value):
        """Validate recipient exists"""
        from apps.users.models import User
        
        try:
            User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Recipient not found")
        
        return value
    
    def create(self, validated_data):
        """Create notification"""
        from apps.users.models import User
        
        recipient_id = validated_data.pop('recipient_id')
        recipient = User.objects.get(id=recipient_id)
        
        notification = Notification.objects.create(
            recipient=recipient,
            **validated_data
        )
        
        return notification


class MarkAsReadSerializer(serializers.Serializer):
    """
    Serializer for marking notification as read
    """
    read = serializers.BooleanField(default=True)


class NotificationStatisticsSerializer(serializers.Serializer):
    """
    Serializer for notification statistics
    """
    total_notifications = serializers.IntegerField()
    unread_count = serializers.IntegerField()
    read_count = serializers.IntegerField()
    by_type = serializers.DictField()
    recent_notifications = NotificationListSerializer(many=True)
