"""
Views for Audit Logs
"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from django.utils import timezone

from apps.audit_logs.models import AuditLog
from apps.audit_logs.serializers import (
    AuditLogSerializer,
    AuditLogListSerializer,
    AuditLogStatisticsSerializer,
)
from apps.users.permissions import IsAdmin


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Admin-only viewset for reading audit logs
    """
    queryset = AuditLog.objects.select_related('actor').all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['action', 'entity', 'actor', 'ip_address', 'created_at']
    search_fields = ['entity', 'entity_id', 'description', 'actor__email', 'actor__full_name', 'ip_address']
    ordering_fields = ['created_at', 'action', 'actor']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return AuditLogListSerializer
        return AuditLogSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        # Date range filtering
        start = self.request.query_params.get('start')
        end = self.request.query_params.get('end')
        if start:
            qs = qs.filter(created_at__gte=start)
        if end:
            qs = qs.filter(created_at__lte=end)
        # Date-only window filtering: created_at__date
        date_start = self.request.query_params.get('date_start')
        date_end = self.request.query_params.get('date_end')
        if date_start:
            qs = qs.filter(created_at__date__gte=date_start)
        if date_end:
            qs = qs.filter(created_at__date__lte=date_end)
        # Path/entity contains filter
        contains = self.request.query_params.get('contains')
        if contains:
            qs = qs.filter(entity__icontains=contains)
        return qs

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """
        Audit log statistics for admins
        """
        qs = self.get_queryset()
        total = qs.count()
        by_action = {a: qs.filter(action=a).count() for a, _ in AuditLog.ACTION_CHOICES}
        # Top entities
        top_entities_qs = qs.values('entity').annotate(count=Count('id')).order_by('-count')[:5]
        top_entities = [{'entity': e['entity'], 'count': e['count']}] if False else [
            {'entity': e['entity'], 'count': e['count']} for e in top_entities_qs
        ]
        # Top users
        top_users_qs = qs.values('actor__email', 'actor__full_name').annotate(count=Count('id')).order_by('-count')[:5]
        top_users = [
            {
                'email': u['actor__email'],
                'name': u['actor__full_name'],
                'count': u['count']
            } for u in top_users_qs
        ]
        recent = qs.order_by('-created_at')[:10]
        recent_ser = AuditLogListSerializer(recent, many=True)
        return Response({
            'total_logs': total,
            'by_action': by_action,
            'top_entities': top_entities,
            'top_users': top_users,
            'recent_logs': recent_ser.data
        })

    @action(detail=False, methods=['get'])
    def recent(self, request):
        qs = self.get_queryset().order_by('-created_at')[:20]
        return Response(AuditLogListSerializer(qs, many=True).data)

    @action(detail=False, methods=['get'])
    def by_user(self, request):
        user_id = request.query_params.get('user')
        if not user_id:
            return Response({'error': 'user query param required'}, status=status.HTTP_400_BAD_REQUEST)
        qs = self.get_queryset().filter(actor_id=user_id)
        return Response(AuditLogListSerializer(qs, many=True).data)
