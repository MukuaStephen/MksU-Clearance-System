"""
Views for Clearance Approval management
"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Avg, Count, Q, F
from django.db.models.functions import Extract
from datetime import timedelta

from apps.approvals.models import ClearanceApproval
from apps.approvals.serializers import (
    ClearanceApprovalSerializer,
    ClearanceApprovalListSerializer,
    ApprovalActionSerializer,
    BulkApprovalSerializer,
    ApprovalStatisticsSerializer
)
from apps.users.permissions import CanApproveClearance, IsAdmin, IsAdminOrDepartmentStaff
from apps.clearances.models import ClearanceRequest
from apps.departments.models import Department
from apps.notifications.utils import (
    notify_approval_action,
    notify_clearance_approved,
    notify_clearance_rejected,
)
from apps.audit_logs.models import AuditLog


class ClearanceApprovalViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Clearance Approval CRUD operations
    
    Permissions:
    - List/Retrieve: Department staff see their dept, Admins see all
    - Create: Not allowed (created automatically with clearance request)
    - Update: Department staff for their dept, Admins for all
    - Delete: Admins only
    - approve/reject: CanApproveClearance permission
    """
    queryset = ClearanceApproval.objects.select_related(
        'clearance_request__student__user',
        'department',
        'approved_by'
    ).all()
    serializer_class = ClearanceApprovalSerializer
    permission_classes = [IsAuthenticated, CanApproveClearance]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'status',
        'department',
        'department__department_type',
        'clearance_request__status',
        'clearance_request__student__faculty',
        'clearance_request__student__graduation_year'
    ]
    search_fields = [
        'clearance_request__student__registration_number',
        'clearance_request__student__user__full_name',
        'clearance_request__student__user__admission_number',
        'notes',
        'rejection_reason'
    ]
    ordering_fields = ['created_at', 'approval_date', 'department__approval_order']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Use different serializers for different actions"""
        if self.action == 'list':
            return ClearanceApprovalListSerializer
        elif self.action in ['approve_reject', 'approve', 'reject']:
            return ApprovalActionSerializer
        elif self.action == 'bulk_approve':
            return BulkApprovalSerializer
        return ClearanceApprovalSerializer
    
    def get_queryset(self):
        """
        Filter queryset based on user role
        Department staff see only their department's approvals
        """
        user = self.request.user

        if user.role == 'admin':
            # Admins see all approvals
            return ClearanceApproval.objects.select_related(
                'clearance_request__student__user',
                'department',
                'approved_by'
            ).all()
        elif user.role in [
            'department_staff',
            'library_staff',
            'finance_staff',
            'hostel_staff',
            'academic_staff',
            'gown_issuance_staff',
            'clearance_officer'
        ]:
            # Department-specific staff see only their department's approvals
            if hasattr(user, 'department') and user.department:
                return ClearanceApproval.objects.filter(
                    department=user.department
                ).select_related(
                    'clearance_request__student__user',
                    'department',
                    'approved_by'
                )

        return ClearanceApproval.objects.none()
    
    def get_permissions(self):
        """Set different permissions based on action"""
        if self.action == 'create':
            # Disable direct creation (created with clearance request)
            return [IsAuthenticated(), IsAdmin()]
        elif self.action == 'destroy':
            # Only admins can delete
            return [IsAuthenticated(), IsAdmin()]
        else:
            return super().get_permissions()
    
    def create(self, request, *args, **kwargs):
        """Disable direct creation"""
        return Response(
            {'error': 'Approvals are created automatically with clearance requests'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    @action(detail=True, methods=['post'])
    def approve_reject(self, request, pk=None):
        """
        Approve or reject a clearance approval
        POST /api/approvals/{id}/approve_reject/
        Body: {"action": "approve|reject", "notes": "...", "rejection_reason": "..."}
        """
        approval = self.get_object()
        user = request.user
        
        # Validate request
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        action_type = serializer.validated_data['action']
        notes = serializer.validated_data.get('notes', '')
        rejection_reason = serializer.validated_data.get('rejection_reason', '')
        
        # Check if already processed
        if approval.status != 'pending':
            return Response(
                {'error': f'This approval is already {approval.status}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if this is the next department in line
        clearance_request = approval.clearance_request
        
        # Get first pending approval by order
        first_pending = clearance_request.approvals.filter(
            status='pending'
        ).order_by('department__approval_order').first()
        
        if first_pending and first_pending.id != approval.id:
            return Response(
                {
                    'error': 'Approvals must be processed in order',
                    'next_department': first_pending.department.name
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Process approval
        if action_type == 'approve':
            approval.status = 'approved'
            approval.approved_by = user
            approval.approval_date = timezone.now()
            approval.notes = notes or 'Approved'
            approval.save()
            
            # Update clearance request status
            clearance_request.status = 'in_progress'
            clearance_request.save()
            
            # Check if all approvals are complete
            pending_count = clearance_request.approvals.filter(status='pending').count()
            if pending_count == 0:
                # All approved
                clearance_request.status = 'completed'
                clearance_request.completion_date = timezone.now()
                clearance_request.save()
                
                message = 'Approved! All departments have cleared this student.'
                # Notify student of approval action and completion
                notify_approval_action(approval)
                notify_clearance_approved(clearance_request)
            # Audit log for approve
            try:
                AuditLog.log_action(
                    actor=user,
                    action='approve',
                    entity='ClearanceApproval',
                    entity_id=approval.id,
                    description=f'Approval #{approval.id} approved for clearance #{clearance_request.id}',
                    changes={'notes': notes},
                    ip_address=request.META.get('REMOTE_ADDR'),
                )
            except Exception:
                pass
            else:
                message = f'Approved! {pending_count} department(s) remaining.'
                # Notify student about approval action
                notify_approval_action(approval)
            
        else:  # reject
            approval.status = 'rejected'
            approval.approved_by = user
            approval.approval_date = timezone.now()
            approval.rejection_reason = rejection_reason
            approval.notes = notes
            approval.save()
            
            # Reject entire clearance request
            clearance_request.status = 'rejected'
            clearance_request.save()
            
            message = 'Rejected. Clearance request has been rejected.'
            # Notify student of rejection
            notify_clearance_rejected(clearance_request)
            # Audit log for reject
            try:
                AuditLog.log_action(
                    actor=user,
                    action='reject',
                    entity='ClearanceApproval',
                    entity_id=approval.id,
                    description=f'Approval #{approval.id} rejected for clearance #{clearance_request.id}',
                    changes={'notes': notes, 'rejection_reason': rejection_reason},
                    ip_address=request.META.get('REMOTE_ADDR'),
                )
            except Exception:
                pass
        
        return Response({
            'message': message,
            'approval': ClearanceApprovalSerializer(approval).data
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """
        Approve a clearance approval (shortcut)
        POST /api/approvals/{id}/approve/
        """
        request.data['action'] = 'approve'
        return self.approve_reject(request, pk)
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """
        Reject a clearance approval (shortcut)
        POST /api/approvals/{id}/reject/
        """
        request.data['action'] = 'reject'
        return self.approve_reject(request, pk)
    
    @action(detail=False, methods=['post'])
    def bulk_approve(self, request):
        """
        Bulk approve multiple clearances
        POST /api/approvals/bulk_approve/
        Body: {
            "approval_ids": [1, 2, 3],
            "action": "approve|reject",
            "notes": "...",
            "rejection_reason": "..."
        }
        """
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        approval_ids = serializer.validated_data['approval_ids']
        action_type = serializer.validated_data['action']
        notes = serializer.validated_data.get('notes', '')
        rejection_reason = serializer.validated_data.get('rejection_reason', '')
        user = request.user
        
        # Get approvals
        approvals = ClearanceApproval.objects.filter(id__in=approval_ids, status='pending')
        
        success_count = 0
        failed_count = 0
        errors = []
        
        for approval in approvals:
            try:
                clearance_request = approval.clearance_request
                
                # Check order
                first_pending = clearance_request.approvals.filter(
                    status='pending'
                ).order_by('department__approval_order').first()
                
                if first_pending and first_pending.id != approval.id:
                    errors.append({
                        'approval_id': approval.id,
                        'error': 'Not next in approval order'
                    })
                    failed_count += 1
                    continue
                
                # Process
                if action_type == 'approve':
                    approval.status = 'approved'
                    approval.approved_by = user
                    approval.approval_date = timezone.now()
                    approval.notes = notes or 'Bulk approved'
                    approval.save()
                    
                    clearance_request.status = 'in_progress'
                    
                    # Check completion
                    if clearance_request.approvals.filter(status='pending').count() == 0:
                        clearance_request.status = 'completed'
                        clearance_request.completion_date = timezone.now()
                    
                    clearance_request.save()
                else:  # reject
                    approval.status = 'rejected'
                    approval.approved_by = user
                    approval.approval_date = timezone.now()
                    approval.rejection_reason = rejection_reason
                    approval.notes = notes
                    approval.save()
                    
                    clearance_request.status = 'rejected'
                    clearance_request.save()
                
                success_count += 1
                
            except Exception as e:
                errors.append({
                    'approval_id': approval.id,
                    'error': str(e)
                })
                failed_count += 1
        
        return Response({
            'message': f'Bulk {action_type} completed',
            'success_count': success_count,
            'failed_count': failed_count,
            'errors': errors
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def pending(self, request):
        """
        Get pending approvals for current user's department
        GET /api/approvals/pending/
        """
        user = request.user
        
        if user.role == 'admin':
            # Admins see all pending
            approvals = ClearanceApproval.objects.filter(
                status='pending',
                clearance_request__status__in=['submitted', 'in_progress']
            ).select_related('clearance_request__student__user', 'department')
        elif user.role == 'department_staff':
            # Department staff see their dept pending
            if not user.department:
                return Response(
                    {'error': 'No department assigned'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            approvals = ClearanceApproval.objects.filter(
                department=user.department,
                status='pending',
                clearance_request__status__in=['submitted', 'in_progress']
            ).select_related('clearance_request__student__user', 'department')
        else:
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = ClearanceApprovalListSerializer(approvals, many=True)
        return Response({
            'count': approvals.count(),
            'approvals': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def my_approvals(self, request):
        """
        Get approvals processed by current user
        GET /api/approvals/my_approvals/
        """
        user = request.user
        
        if user.role not in ['admin', 'department_staff']:
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        approvals = ClearanceApproval.objects.filter(
            approved_by=user
        ).select_related(
            'clearance_request__student__user',
            'department'
        ).order_by('-approval_date')
        
        serializer = ClearanceApprovalListSerializer(approvals, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """
        Get approval statistics
        GET /api/approvals/statistics/
        """
        user = request.user
        
        if user.role not in ['admin', 'department_staff']:
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Filter by department for staff
        if user.role == 'department_staff' and user.department:
            department = user.department
            approvals = ClearanceApproval.objects.filter(department=department)
        else:
            department = None
            approvals = ClearanceApproval.objects.all()
        
        # Calculate statistics
        total = approvals.count()
        pending = approvals.filter(status='pending').count()
        approved = approvals.filter(status='approved').count()
        rejected = approvals.filter(status='rejected').count()
        
        # Average approval time (in hours)
        approved_approvals = approvals.filter(status='approved', approval_date__isnull=False)
        if approved_approvals.exists():
            time_diffs = []
            for approval in approved_approvals:
                if approval.approval_date and approval.created_at:
                    diff = (approval.approval_date - approval.created_at).total_seconds() / 3600
                    time_diffs.append(diff)
            avg_time = sum(time_diffs) / len(time_diffs) if time_diffs else None
        else:
            avg_time = None
        
        return Response({
            'department': department.name if department else 'All Departments',
            'total_approvals': total,
            'pending_count': pending,
            'approved_count': approved,
            'rejected_count': rejected,
            'approval_rate': round((approved / total * 100), 2) if total > 0 else 0,
            'average_approval_time_hours': round(avg_time, 2) if avg_time else None
        })
