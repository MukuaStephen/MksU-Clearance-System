"""
Views for Clearance Request management
"""
from rest_framework import viewsets, filters, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

from apps.clearances.models import ClearanceRequest
from apps.clearances.serializers import (
    ClearanceRequestSerializer,
    ClearanceRequestListSerializer,
    ClearanceRequestCreateSerializer,
    ClearanceRequestDetailSerializer,
    ClearanceRequestSubmitSerializer
)
from apps.users.permissions import IsStudentOwnerOrAdmin, IsAdmin
from apps.students.models import Student
from apps.approvals.models import ClearanceApproval
from apps.notifications.utils import notify_clearance_submitted
from apps.audit_logs.mixins import AuditViewSetMixin


class ClearanceRequestViewSet(AuditViewSetMixin, viewsets.ModelViewSet):
    """
    ViewSet for Clearance Request CRUD operations
    
    Permissions:
    - List/Retrieve: Students see own requests, Admins/Staff see all
    - Create: Students only (must be eligible and have paid)
    - Update: Students can update draft, Admins can update any
    - Delete: Admins only
    """
    queryset = ClearanceRequest.objects.select_related('student__user').prefetch_related('approvals__department').all()
    serializer_class = ClearanceRequestSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'student__faculty', 'student__program', 'student__graduation_year']
    search_fields = [
        'student__registration_number',
        'student__user__full_name',
        'student__user__admission_number',
        'notes'
    ]
    ordering_fields = ['created_at', 'submission_date', 'completion_date', 'status']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Use different serializers for different actions"""
        if self.action == 'list':
            return ClearanceRequestListSerializer
        elif self.action == 'create':
            return ClearanceRequestCreateSerializer
        elif self.action == 'retrieve':
            return ClearanceRequestDetailSerializer
        elif self.action == 'submit':
            return ClearanceRequestSubmitSerializer
        return ClearanceRequestSerializer
    
    def get_queryset(self):
        """
        Filter queryset based on user role
        Students can only see their own clearance requests
        """
        user = self.request.user
        
        if user.role == 'admin':
            # Admins see all clearance requests
            return ClearanceRequest.objects.select_related('student__user').prefetch_related('approvals__department').all()
        elif user.role == 'department_staff':
            # Department staff see all clearance requests
            return ClearanceRequest.objects.select_related('student__user').prefetch_related('approvals__department').all()
        elif user.role == 'student':
            # Students see only their own clearance requests
            try:
                student = Student.objects.get(user=user)
                return ClearanceRequest.objects.filter(student=student).select_related('student__user').prefetch_related('approvals__department')
            except Student.DoesNotExist:
                return ClearanceRequest.objects.none()
        
        return ClearanceRequest.objects.none()
    
    def get_permissions(self):
        """
        Set different permissions based on action
        """
        if self.action == 'destroy':
            # Only admins can delete clearance requests
            return [IsAuthenticated(), IsAdmin()]
        elif self.action in ['update', 'partial_update']:
            # Students can update own draft, admins can update any
            return [IsAuthenticated()]
        else:
            # Default permissions
            return [IsAuthenticated()]
    
    def perform_create(self, serializer):
        """
        Create clearance request
        Only students can create for themselves
        """
        user = self.request.user
        
        if user.role != 'student':
            raise serializers.ValidationError({
                'error': 'Only students can create clearance requests'
            })
        
        # Get student record
        try:
            student = Student.objects.get(user=user)
        except Student.DoesNotExist:
            raise serializers.ValidationError({
                'error': 'Student record not found'
            })
        
        # Ensure student_id matches authenticated user
        student_id = serializer.validated_data.get('student_id')
        if student_id != student.id:
            raise serializers.ValidationError({
                'error': 'You can only create clearance requests for yourself'
            })
        
        serializer.save()
    
    def update(self, request, *args, **kwargs):
        """
        Update clearance request
        Students can only update draft status
        Admins can update any status
        """
        instance = self.get_object()
        user = request.user
        
        # Check permissions
        if user.role == 'student':
            # Students can only update their own draft requests
            try:
                student = Student.objects.get(user=user)
                if instance.student != student:
                    return Response(
                        {'error': 'You can only update your own clearance requests'},
                        status=status.HTTP_403_FORBIDDEN
                    )
                if instance.status != 'draft':
                    return Response(
                        {'error': 'You can only update draft clearance requests'},
                        status=status.HTTP_403_FORBIDDEN
                    )
            except Student.DoesNotExist:
                return Response(
                    {'error': 'Student record not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        return super().update(request, *args, **kwargs)
    
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """
        Submit clearance request for approval
        POST /api/clearances/{id}/submit/
        Changes status from draft to submitted
        """
        clearance_request = self.get_object()
        user = request.user
        
        # Check ownership for students
        if user.role == 'student':
            try:
                student = Student.objects.get(user=user)
                if clearance_request.student != student:
                    return Response(
                        {'error': 'You can only submit your own clearance requests'},
                        status=status.HTTP_403_FORBIDDEN
                    )
            except Student.DoesNotExist:
                return Response(
                    {'error': 'Student record not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        # Validate submission
        serializer = self.get_serializer(
            data=request.data,
            context={'clearance_request': clearance_request}
        )
        serializer.is_valid(raise_exception=True)
        
        # Update status to submitted
        clearance_request.status = 'submitted'
        clearance_request.submission_date = timezone.now()
        clearance_request.save()
        
        # Notify student and admins about submission
        notify_clearance_submitted(clearance_request)
        
        return Response({
            'message': 'Clearance request submitted successfully',
            'clearance_request': ClearanceRequestDetailSerializer(clearance_request).data
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def my_clearances(self, request):
        """
        Get current student's clearance requests
        GET /api/clearances/my_clearances/
        Students only
        """
        if request.user.role != 'student':
            return Response(
                {'error': 'Only students can access this endpoint'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            return Response(
                {'error': 'Student record not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        clearances = ClearanceRequest.objects.filter(
            student=student
        ).select_related('student__user').prefetch_related('approvals__department').order_by('-created_at')
        
        serializer = ClearanceRequestListSerializer(clearances, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pending_approvals(self, request):
        """
        Get clearance requests pending approval from user's department
        GET /api/clearances/pending_approvals/
        Department staff only
        """
        user = request.user
        
        if user.role != 'department_staff':
            return Response(
                {'error': 'Only department staff can access this endpoint'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if not user.department:
            return Response(
                {'error': 'No department assigned to your account'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get clearances with pending approvals for this department
        pending_approvals = ClearanceApproval.objects.filter(
            department=user.department,
            status='pending',
            clearance_request__status__in=['submitted', 'in_progress']
        ).select_related('clearance_request__student__user')
        
        # Get unique clearance requests
        clearance_ids = pending_approvals.values_list('clearance_request_id', flat=True)
        clearances = ClearanceRequest.objects.filter(
            id__in=clearance_ids
        ).select_related('student__user').prefetch_related('approvals__department')
        
        serializer = ClearanceRequestListSerializer(clearances, many=True)
        return Response({
            'department': user.department.name,
            'pending_count': clearances.count(),
            'clearances': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """
        Get clearance request statistics
        GET /api/clearances/statistics/
        Admins and department staff only
        """
        user = request.user
        
        if user.role not in ['admin', 'department_staff']:
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Base queryset
        queryset = ClearanceRequest.objects.all()
        
        # Filter by department for staff
        if user.role == 'department_staff' and user.department:
            # Get clearances that have approval for this department
            approval_ids = ClearanceApproval.objects.filter(
                department=user.department
            ).values_list('clearance_request_id', flat=True)
            queryset = queryset.filter(id__in=approval_ids)
        
        # Calculate statistics
        total = queryset.count()
        draft = queryset.filter(status='draft').count()
        submitted = queryset.filter(status='submitted').count()
        in_progress = queryset.filter(status='in_progress').count()
        completed = queryset.filter(status='completed').count()
        rejected = queryset.filter(status='rejected').count()
        
        return Response({
            'total_requests': total,
            'status_breakdown': {
                'draft': draft,
                'submitted': submitted,
                'in_progress': in_progress,
                'completed': completed,
                'rejected': rejected
            },
            'completion_rate': round((completed / total * 100), 2) if total > 0 else 0
        })
    
    @action(detail=True, methods=['get'])
    def approval_progress(self, request, pk=None):
        """
        Get detailed approval progress for a clearance request
        GET /api/clearances/{id}/approval_progress/
        """
        clearance_request = self.get_object()
        
        approvals = clearance_request.approvals.select_related(
            'department', 'approved_by'
        ).order_by('department__approval_order')
        
        progress_data = []
        for approval in approvals:
            progress_data.append({
                'order': approval.department.approval_order,
                'department': approval.department.name,
                'department_code': approval.department.code,
                'status': approval.status,
                'approved_by': approval.approved_by.full_name if approval.approved_by else None,
                'approval_date': approval.approval_date,
                'rejection_reason': approval.rejection_reason,
                'notes': approval.notes
            })
        
        return Response({
            'clearance_request_id': clearance_request.id,
            'overall_status': clearance_request.status,
            'completion_percentage': clearance_request.get_completion_percentage(),
            'total_departments': approvals.count(),
            'approved_count': approvals.filter(status='approved').count(),
            'pending_count': approvals.filter(status='pending').count(),
            'rejected_count': approvals.filter(status='rejected').count(),
            'progress': progress_data
        })
