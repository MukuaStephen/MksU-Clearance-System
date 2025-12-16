"""
Views for Student management
"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from apps.students.models import Student
from apps.students.serializers import StudentSerializer, StudentCreateSerializer
from apps.users.permissions import IsAdmin, IsStudentOwnerOrAdmin
from apps.audit_logs.mixins import AuditViewSetMixin


class StudentViewSet(AuditViewSetMixin, viewsets.ModelViewSet):
    """
    ViewSet for Student CRUD operations
    
    Permissions:
    - List/Retrieve: Students can see own data, Admins can see all
    - Create: Admins only
    - Update/Delete: Admins only, Students can update limited fields
    """
    queryset = Student.objects.select_related('user').all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, IsStudentOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'school', 'department', 'course',
        'faculty', 'program', 'graduation_year', 'admission_year', 'eligibility_status'
    ]
    search_fields = ['registration_number', 'user__full_name', 'user__email', 'user__admission_number']
    ordering_fields = ['created_at', 'graduation_year', 'admission_year', 'registration_number']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Use different serializer for create"""
        if self.action == 'create':
            return StudentCreateSerializer
        return StudentSerializer
    
    def get_queryset(self):
        """
        Filter queryset based on user role
        Students can only see their own record
        """
        user = self.request.user
        
        if user.role == 'admin':
            # Admins see all students
            return Student.objects.select_related('user').all()
        elif user.role == 'student':
            # Students see only their own record
            return Student.objects.filter(user=user).select_related('user')
        elif user.role == 'department_staff':
            # Department staff see all students (for clearance processing)
            return Student.objects.select_related('user').all()
        
        return Student.objects.none()
    
    def get_permissions(self):
        """
        Set different permissions based on action
        """
        if self.action in ['create', 'destroy']:
            # Only admins can create or delete students
            return [IsAuthenticated(), IsAdmin()]
        elif self.action in ['update', 'partial_update']:
            # Admins can update all, students can update own limited fields
            return [IsAuthenticated(), IsStudentOwnerOrAdmin()]
        else:
            # List and retrieve use default permissions
            return super().get_permissions()
    
    def create(self, request, *args, **kwargs):
        """Create student with user account"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        student = serializer.save()
        
        # Return full student data
        output_serializer = StudentSerializer(student)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get'])
    def clearance_status(self, request, pk=None):
        """
        Get student's clearance status
        GET /api/students/{id}/clearance_status/
        """
        student = self.get_object()
        
        # Get student's clearance requests
        from apps.clearances.models import ClearanceRequest
        clearances = ClearanceRequest.objects.filter(student=student).order_by('-created_at')
        
        if clearances.exists():
            latest_clearance = clearances.first()
            
            # Get approvals for this clearance
            approvals = latest_clearance.approvals.select_related('department').all()
            
            return Response({
                'student': StudentSerializer(student).data,
                'clearance_id': latest_clearance.id,
                'status': latest_clearance.status,
                'submission_date': latest_clearance.submission_date,
                'completion_percentage': latest_clearance.get_completion_percentage(),
                'approvals': [
                    {
                        'department': approval.department.name,
                        'status': approval.status,
                        'approval_date': approval.approval_date,
                        'notes': approval.notes
                    }
                    for approval in approvals
                ]
            })
        else:
            return Response({
                'student': StudentSerializer(student).data,
                'message': 'No clearance request submitted yet'
            })
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Get current student's own data
        GET /api/students/me/
        """
        if request.user.role != 'student':
            return Response(
                {'error': 'Only students can access this endpoint'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            student = Student.objects.select_related('user').get(user=request.user)
            serializer = self.get_serializer(student)
            return Response(serializer.data)
        except Student.DoesNotExist:
            return Response(
                {'error': 'Student record not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'])
    def eligible(self, request):
        """
        Get list of eligible students for clearance
        GET /api/students/eligible/
        Only accessible by admins and department staff
        """
        if request.user.role not in ['admin', 'department_staff']:
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        eligible_students = Student.objects.filter(
            eligibility_status='eligible'
        ).select_related('user')
        
        serializer = self.get_serializer(eligible_students, many=True)
        return Response(serializer.data)
