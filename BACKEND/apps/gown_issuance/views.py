"""
Views for Gown Issuance management
"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from apps.gown_issuance.models import GownIssuance
from apps.gown_issuance.serializers import (
    GownIssuanceSerializer,
    GownIssuanceListSerializer,
    GownReturnSerializer,
    GownRefundSerializer
)
from apps.users.permissions import IsAdmin
from apps.audit_logs.mixins import AuditViewSetMixin


class GownIssuanceViewSet(AuditViewSetMixin, viewsets.ModelViewSet):
    """
    ViewSet for Gown Issuance CRUD operations
    
    Permissions:
    - List/Retrieve: Admin and department staff
    - Create/Update/Delete: Admin only
    """
    queryset = GownIssuance.objects.select_related('student', 'student__user', 'issued_by', 'returned_to').all()
    serializer_class = GownIssuanceSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deposit_paid', 'deposit_refunded', 'gown_size', 'issued_date']
    search_fields = ['gown_number', 'student__registration_number', 'student__user__full_name']
    ordering_fields = ['issued_date', 'expected_return_date', 'gown_number']
    ordering = ['-issued_date']
    
    def get_serializer_class(self):
        """Use list serializer for list action"""
        if self.action == 'list':
            return GownIssuanceListSerializer
        return GownIssuanceSerializer
    
    def perform_create(self, serializer):
        """Set issued_by to current user"""
        serializer.save(issued_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def mark_returned(self, request, pk=None):
        """
        Mark gown as returned
        POST /api/gown-issuances/{id}/mark_returned/
        """
        gown_issuance = self.get_object()
        
        if gown_issuance.status == 'returned':
            return Response(
                {'error': 'Gown already marked as returned'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = GownReturnSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        condition_notes = serializer.validated_data.get('condition_notes', '')
        gown_issuance.mark_returned(
            returned_to=request.user,
            condition_notes=condition_notes
        )
        
        # Log the action
        from apps.audit_logs.models import AuditLog
        AuditLog.log_action(
            user=request.user,
            action='mark_returned',
            resource_type='gown_issuance',
            resource_id=str(gown_issuance.id),
            details=f"Gown {gown_issuance.gown_number} marked as returned"
        )
        
        output_serializer = GownIssuanceSerializer(gown_issuance)
        return Response(output_serializer.data)
    
    @action(detail=True, methods=['post'])
    def process_refund(self, request, pk=None):
        """
        Process deposit refund
        POST /api/gown-issuances/{id}/process_refund/
        """
        gown_issuance = self.get_object()
        
        if gown_issuance.deposit_refunded:
            return Response(
                {'error': 'Deposit already refunded'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if gown_issuance.status != 'returned':
            return Response(
                {'error': 'Gown must be returned before processing refund'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = GownRefundSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            gown_issuance.process_refund(
                refund_amount=serializer.validated_data['refund_amount']
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Log the action
        from apps.audit_logs.models import AuditLog
        AuditLog.log_action(
            user=request.user,
            action='process_refund',
            resource_type='gown_issuance',
            resource_id=str(gown_issuance.id),
            details=f"Refund of KES {gown_issuance.refund_amount} processed for gown {gown_issuance.gown_number}"
        )
        
        output_serializer = GownIssuanceSerializer(gown_issuance)
        return Response(output_serializer.data)
    
    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """
        Get list of overdue gown returns
        GET /api/gown-issuances/overdue/
        """
        from django.utils import timezone
        
        overdue_gowns = self.get_queryset().filter(
            status='issued',
            expected_return_date__lt=timezone.now().date()
        )
        
        serializer = self.get_serializer(overdue_gowns, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """
        Get gown issuance statistics
        GET /api/gown-issuances/statistics/
        """
        from django.db.models import Count, Sum, Q
        from django.utils import timezone
        
        queryset = self.get_queryset()
        
        stats = {
            'total_issued': queryset.count(),
            'currently_issued': queryset.filter(status='issued').count(),
            'returned': queryset.filter(status='returned').count(),
            'lost': queryset.filter(status='lost').count(),
            'damaged': queryset.filter(status='damaged').count(),
            'overdue': queryset.filter(
                status='issued',
                expected_return_date__lt=timezone.now().date()
            ).count(),
            'deposits_pending': queryset.filter(deposit_paid=False).count(),
            'deposits_collected': queryset.filter(deposit_paid=True).aggregate(
                total=Sum('deposit_amount')
            )['total'] or 0,
            'refunds_pending': queryset.filter(
                status='returned',
                deposit_refunded=False
            ).count(),
            'refunds_processed': queryset.filter(deposit_refunded=True).aggregate(
                total=Sum('refund_amount')
            )['total'] or 0,
        }
        
        return Response(stats)
