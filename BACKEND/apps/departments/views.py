"""
Views for Department management
"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from apps.departments.models import Department
from apps.departments.serializers import (
    DepartmentSerializer,
    DepartmentListSerializer,
    DepartmentStaffSerializer
)
from apps.users.permissions import IsAdminOrReadOnly
from apps.audit_logs.mixins import AuditViewSetMixin


class DepartmentViewSet(AuditViewSetMixin, viewsets.ModelViewSet):
    """
    ViewSet for Department CRUD operations
    
    Permissions:
    - List/Retrieve: All authenticated users (read-only)
    - Create/Update/Delete: Admins only
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['department_type', 'is_active']
    search_fields = ['name', 'code', 'contact_email']
    ordering_fields = ['approval_order', 'name', 'created_at']
    ordering = ['approval_order']
    
    def get_serializer_class(self):
        """Use lightweight serializer for list action"""
        if self.action == 'list':
            return DepartmentListSerializer
        return DepartmentSerializer
    
    @action(detail=False, methods=['get'])
    def academic(self, request):
        """
        Get all academic departments
        GET /api/departments/academic/
        """
        departments = Department.objects.filter(
            department_type='academic',
            is_active=True
        ).order_by('approval_order')
        
        serializer = DepartmentListSerializer(departments, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def administrative(self, request):
        """
        Get all administrative departments
        GET /api/departments/administrative/
        """
        departments = Department.objects.filter(
            department_type='administrative',
            is_active=True
        ).order_by('approval_order')
        
        serializer = DepartmentListSerializer(departments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def staff(self, request, pk=None):
        """
        Get staff members assigned to this department
        GET /api/departments/{id}/staff/
        """
        department = self.get_object()
        
        # Get users with department_staff role assigned to this department
        from apps.users.models import User
        staff_members = User.objects.filter(
            role='department_staff',
            department=department,
            is_active=True
        ).values('id', 'full_name', 'email', 'admission_number', 'is_active')
        
        serializer = DepartmentStaffSerializer(staff_members, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """
        Get statistics for this department
        GET /api/departments/{id}/statistics/
        """
        department = self.get_object()
        
        # Get clearance approval statistics
        from apps.clearances.models import ClearanceApproval
        
        total_approvals = ClearanceApproval.objects.filter(department=department).count()
        pending_approvals = ClearanceApproval.objects.filter(
            department=department,
            status='pending'
        ).count()
        approved_count = ClearanceApproval.objects.filter(
            department=department,
            status='approved'
        ).count()
        rejected_count = ClearanceApproval.objects.filter(
            department=department,
            status='rejected'
        ).count()
        
        return Response({
            'department': DepartmentSerializer(department).data,
            'statistics': {
                'total_approvals': total_approvals,
                'pending_approvals': pending_approvals,
                'approved_count': approved_count,
                'rejected_count': rejected_count,
                'approval_rate': round((approved_count / total_approvals * 100), 2) if total_approvals > 0 else 0
            }
        })
    
    @action(detail=False, methods=['get'])
    def approval_workflow(self, request):
        """
        Get departments in approval order
        GET /api/departments/approval_workflow/
        Shows the clearance approval sequence
        """
        departments = Department.objects.filter(
            is_active=True
        ).order_by('approval_order')
        
        workflow = []
        for dept in departments:
            workflow.append({
                'order': dept.approval_order,
                'department': dept.name,
                'code': dept.code,
                'type': dept.department_type,
                'contact': dept.contact_email
            })
        
        return Response({
            'total_steps': len(workflow),
            'workflow': workflow
        })
