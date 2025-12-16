"""
Views for Notification management
"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Count, Q

from apps.notifications.models import Notification
from apps.notifications.serializers import (
    NotificationSerializer,
    NotificationListSerializer,
    NotificationCreateSerializer,
    MarkAsReadSerializer,
    NotificationStatisticsSerializer
)
from apps.users.permissions import IsAdmin
from apps.audit_logs.mixins import AuditViewSetMixin


class NotificationViewSet(AuditViewSetMixin, viewsets.ModelViewSet):
    """
    ViewSet for Notification CRUD operations
    
    Permissions:
    - List/Retrieve: Users see only their own notifications
    - Create: Admins only (or system-generated)
    - Update: Not allowed (use mark_as_read action)
    - Delete: Users can delete their own notifications
    """
    queryset = Notification.objects.select_related('recipient').all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['notification_type', 'is_read', 'sent_via_email']
    search_fields = ['title', 'message']
    ordering_fields = ['created_at', 'read_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Use different serializers for different actions"""
        if self.action == 'list':
            return NotificationListSerializer
        elif self.action == 'create':
            return NotificationCreateSerializer
        elif self.action in ['mark_as_read', 'mark_as_unread']:
            return MarkAsReadSerializer
        return NotificationSerializer
    
    def get_queryset(self):
        """
        Users see only their own notifications
        Admins see all notifications
        """
        user = self.request.user
        
        if user.role == 'admin':
            return Notification.objects.select_related('recipient').all()
        else:
            return Notification.objects.filter(
                recipient=user
            ).select_related('recipient')
    
    def get_permissions(self):
        """Set different permissions based on action"""
        if self.action == 'create':
            # Only admins can create notifications manually
            return [IsAuthenticated(), IsAdmin()]
        elif self.action in ['update', 'partial_update']:
            # Disable update (use mark_as_read instead)
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated()]
    
    def destroy(self, request, *args, **kwargs):
        """
        Delete notification
        Users can only delete their own notifications
        """
        notification = self.get_object()
        user = request.user
        
        # Check ownership
        if notification.recipient != user and user.role != 'admin':
            return Response(
                {'error': 'You can only delete your own notifications'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().destroy(request, *args, **kwargs)
    
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """
        Mark notification as read
        POST /api/notifications/{id}/mark_as_read/
        """
        notification = self.get_object()
        user = request.user
        
        # Check ownership
        if notification.recipient != user and user.role != 'admin':
            return Response(
                {'error': 'You can only mark your own notifications as read'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if not notification.is_read:
            notification.is_read = True
            notification.read_at = timezone.now()
            notification.save()
        
        return Response({
            'message': 'Notification marked as read',
            'notification': NotificationSerializer(notification).data
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def mark_as_unread(self, request, pk=None):
        """
        Mark notification as unread
        POST /api/notifications/{id}/mark_as_unread/
        """
        notification = self.get_object()
        user = request.user
        
        # Check ownership
        if notification.recipient != user and user.role != 'admin':
            return Response(
                {'error': 'You can only mark your own notifications as unread'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if notification.is_read:
            notification.is_read = False
            notification.read_at = None
            notification.save()
        
        return Response({
            'message': 'Notification marked as unread',
            'notification': NotificationSerializer(notification).data
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        """
        Mark all user's notifications as read
        POST /api/notifications/mark_all_as_read/
        """
        user = request.user
        
        unread_notifications = Notification.objects.filter(
            recipient=user,
            is_read=False
        )
        
        count = unread_notifications.count()
        
        unread_notifications.update(
            is_read=True,
            read_at=timezone.now()
        )
        
        return Response({
            'message': f'{count} notification(s) marked as read'
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def unread(self, request):
        """
        Get user's unread notifications
        GET /api/notifications/unread/
        """
        user = request.user
        
        unread_notifications = Notification.objects.filter(
            recipient=user,
            is_read=False
        ).order_by('-created_at')
        
        serializer = NotificationListSerializer(unread_notifications, many=True)
        
        return Response({
            'count': unread_notifications.count(),
            'notifications': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """
        Get count of user's unread notifications
        GET /api/notifications/unread_count/
        """
        user = request.user
        
        count = Notification.objects.filter(
            recipient=user,
            is_read=False
        ).count()
        
        return Response({
            'unread_count': count
        })
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """
        Get notification statistics
        GET /api/notifications/statistics/
        """
        user = request.user
        
        # Filter by user or all (for admin)
        if user.role == 'admin':
            queryset = Notification.objects.all()
        else:
            queryset = Notification.objects.filter(recipient=user)
        
        total = queryset.count()
        unread = queryset.filter(is_read=False).count()
        read = total - unread
        
        # By type
        by_type = {}
        for ntype, label in Notification.NOTIFICATION_TYPES:
            count = queryset.filter(notification_type=ntype).count()
            by_type[label] = count
        
        # Recent notifications
        recent = queryset.order_by('-created_at')[:5]
        recent_serializer = NotificationListSerializer(recent, many=True)
        
        return Response({
            'total_notifications': total,
            'unread_count': unread,
            'read_count': read,
            'by_type': by_type,
            'recent_notifications': recent_serializer.data
        })
    
    @action(detail=False, methods=['delete'])
    def delete_all_read(self, request):
        """
        Delete all read notifications
        DELETE /api/notifications/delete_all_read/
        """
        user = request.user
        
        read_notifications = Notification.objects.filter(
            recipient=user,
            is_read=True
        )
        
        count = read_notifications.count()
        read_notifications.delete()
        
        return Response({
            'message': f'{count} read notification(s) deleted'
        }, status=status.HTTP_200_OK)
