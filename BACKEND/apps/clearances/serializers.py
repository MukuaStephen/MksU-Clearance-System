"""
Serializers for Clearance Request management
"""
from rest_framework import serializers
from apps.clearances.models import ClearanceRequest
from apps.students.serializers import StudentSerializer
from apps.approvals.models import ClearanceApproval
from apps.departments.models import Department
from apps.finance.models import Payment


class ClearanceRequestListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing clearance requests
    """
    student_name = serializers.CharField(source='student.user.full_name', read_only=True)
    registration_number = serializers.CharField(source='student.registration_number', read_only=True)
    completion_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = ClearanceRequest
        fields = [
            'id',
            'student_name',
            'registration_number',
            'status',
            'submission_date',
            'completion_date',
            'completion_percentage',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_completion_percentage(self, obj):
        """Calculate approval completion percentage"""
        return obj.get_completion_percentage()


class ClearanceRequestSerializer(serializers.ModelSerializer):
    """
    Full serializer for clearance request CRUD operations
    """
    student = StudentSerializer(read_only=True)
    student_id = serializers.IntegerField(write_only=True)
    completion_percentage = serializers.SerializerMethodField()
    approval_summary = serializers.SerializerMethodField()
    payment_status = serializers.SerializerMethodField()
    
    class Meta:
        model = ClearanceRequest
        fields = [
            'id',
            'student',
            'student_id',
            'status',
            'submission_date',
            'completion_date',
            'rejection_reason',
            'completion_percentage',
            'approval_summary',
            'payment_status',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'status', 'submission_date', 'completion_date', 'created_at', 'updated_at']
    
    def get_completion_percentage(self, obj):
        """Calculate approval completion percentage"""
        return obj.get_completion_percentage()
    
    def get_approval_summary(self, obj):
        """Get summary of approvals by status"""
        approvals = obj.approvals.all()
        return {
            'total': approvals.count(),
            'approved': approvals.filter(status='approved').count(),
            'rejected': approvals.filter(status='rejected').count(),
            'pending': approvals.filter(status='pending').count(),
        }
    
    def get_payment_status(self, obj):
        """Get student's payment status"""
        try:
            payment = Payment.objects.get(student=obj.student)
            return {
                'has_paid': payment.is_verified,
                'amount': str(payment.amount),
                'payment_method': payment.payment_method,
                'verified': payment.is_verified
            }
        except Payment.DoesNotExist:
            return {
                'has_paid': False,
                'amount': '0',
                'payment_method': None,
                'verified': False
            }
    
    def validate_student_id(self, value):
        """Validate student exists and is eligible"""
        from apps.students.models import Student
        
        try:
            student = Student.objects.get(id=value)
        except Student.DoesNotExist:
            raise serializers.ValidationError("Student not found")
        
        # Check if student is eligible for clearance
        if student.eligibility_status != 'eligible':
            raise serializers.ValidationError(
                f"Student is not eligible for clearance. Status: {student.get_eligibility_status_display()}"
            )
        
        # Check if student already has a clearance request in progress
        existing = ClearanceRequest.objects.filter(
            student=student,
            status__in=['draft', 'submitted', 'in_progress']
        )
        
        if existing.exists():
            raise serializers.ValidationError(
                "Student already has a clearance request in progress"
            )
        
        return value
    
    def validate(self, attrs):
        """Additional validation"""
        # If updating, check status transitions
        if self.instance:
            old_status = self.instance.status
            new_status = attrs.get('status', old_status)
            
            # Define valid status transitions
            valid_transitions = {
                'draft': ['submitted'],
                'submitted': ['in_progress', 'rejected'],
                'in_progress': ['completed', 'rejected'],
                'completed': [],
                'rejected': []
            }
            
            if new_status != old_status and new_status not in valid_transitions.get(old_status, []):
                raise serializers.ValidationError({
                    'status': f'Cannot transition from {old_status} to {new_status}'
                })
        
        return attrs


class ClearanceRequestCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new clearance request
    Automatically creates approval records for all departments
    """
    student_id = serializers.UUIDField()  # Changed from IntegerField to UUIDField
    
    class Meta:
        model = ClearanceRequest
        fields = ['student_id']
    
    def validate_student_id(self, value):
        """Validate student exists and is eligible"""
        from apps.students.models import Student
        
        try:
            student = Student.objects.get(id=value)
        except Student.DoesNotExist:
            raise serializers.ValidationError("Student not found")
        
        # Check eligibility (relaxed check - allow pending too)
        if student.eligibility_status == 'ineligible':
            raise serializers.ValidationError(
                f"Student is not eligible for clearance. Status: {student.get_eligibility_status_display()}"
            )
        
        # Payment check is optional for now (TODO: uncomment when payment system is ready)
        # try:
        #     payment = Payment.objects.get(student=student)
        #     if not payment.is_verified:
        #         raise serializers.ValidationError(
        #             "Student has not completed payment verification. Please verify payment first."
        #         )
        # except Payment.DoesNotExist:
        #     raise serializers.ValidationError(
        #         "No payment record found. Student must pay clearance fees first."
        #     )
        
        return value
    
    def create(self, validated_data):
        """
        Create clearance request and approval records for all departments
        """
        from apps.students.models import Student
        
        student_id = validated_data.pop('student_id')
        student = Student.objects.get(id=student_id)
        
        # Create clearance request with initial pending status
        clearance_request = ClearanceRequest.objects.create(
            student=student,
            status='pending',
            **validated_data
        )
        
        # Create approval records for all active departments
        departments = Department.objects.filter(is_active=True).order_by('approval_order')
        
        for department in departments:
            ClearanceApproval.objects.create(
                clearance_request=clearance_request,
                department=department,
                status='pending',
                notes=f'Awaiting approval from {department.name}'
            )
        
        return clearance_request


class ClearanceRequestSubmitSerializer(serializers.Serializer):
    """
    Serializer for submitting a clearance request
    """
    confirm = serializers.BooleanField(required=True)
    
    def validate_confirm(self, value):
        """Ensure confirmation is True"""
        if not value:
            raise serializers.ValidationError("You must confirm submission")
        return value
    
    def validate(self, attrs):
        """Validate clearance request can be submitted"""
        clearance_request = self.context.get('clearance_request')
        
        if not clearance_request:
            raise serializers.ValidationError("Clearance request not found")
        
        if clearance_request.status != 'draft':
            raise serializers.ValidationError(
                f"Cannot submit clearance request with status: {clearance_request.status}"
            )
        
        # Verify payment again at submission
        try:
            payment = Payment.objects.get(student=clearance_request.student)
            if not payment.is_verified:
                raise serializers.ValidationError(
                    "Payment verification required before submission"
                )
        except Payment.DoesNotExist:
            raise serializers.ValidationError(
                "No payment record found"
            )
        
        # Check all required departments have approval records
        approval_count = clearance_request.approvals.count()
        department_count = Department.objects.filter(is_active=True).count()
        
        if approval_count != department_count:
            raise serializers.ValidationError(
                "Approval records incomplete. Please contact admin."
            )
        
        return attrs


class ClearanceApprovalDetailSerializer(serializers.Serializer):
    """
    Serializer for displaying approval details within clearance request
    """
    id = serializers.IntegerField()
    department = serializers.CharField(source='department.name')
    department_code = serializers.CharField(source='department.code')
    department_type = serializers.CharField(source='department.department_type')
    approval_order = serializers.IntegerField(source='department.approval_order')
    status = serializers.CharField()
    approved_by = serializers.CharField(source='approved_by.full_name', allow_null=True)
    approval_date = serializers.DateTimeField(allow_null=True)
    rejection_reason = serializers.CharField(allow_null=True)
    notes = serializers.CharField()
    created_at = serializers.DateTimeField()


class ClearanceRequestDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer with all approvals for single clearance view
    """
    student = StudentSerializer(read_only=True)
    approvals = ClearanceApprovalDetailSerializer(many=True, read_only=True)
    completion_percentage = serializers.SerializerMethodField()
    payment_info = serializers.SerializerMethodField()
    current_department = serializers.SerializerMethodField()
    
    class Meta:
        model = ClearanceRequest
        fields = [
            'id',
            'student',
            'status',
            'submission_date',
            'completion_date',
            'rejection_reason',
            'approvals',
            'completion_percentage',
            'payment_info',
            'current_department',
            'created_at',
            'updated_at'
        ]
    
    def get_completion_percentage(self, obj):
        """Calculate approval completion percentage"""
        return obj.get_completion_percentage()
    
    def get_payment_info(self, obj):
        """Get detailed payment information"""
        try:
            payment = Payment.objects.get(student=obj.student)
            return {
                'id': payment.id,
                'amount': str(payment.amount),
                'payment_method': payment.payment_method,
                'transaction_id': payment.transaction_id,
                'payment_date': payment.payment_date,
                'is_verified': payment.is_verified,
                'verified_by': payment.verified_by.full_name if payment.verified_by else None,
                'verification_date': payment.verification_date
            }
        except Payment.DoesNotExist:
            return None
    
    def get_current_department(self, obj):
        """Get the next pending department in approval workflow"""
        if obj.status == 'completed':
            return None
        
        # Get first pending approval ordered by department approval_order
        pending_approval = obj.approvals.filter(
            status='pending'
        ).order_by('department__approval_order').first()
        
        if pending_approval:
            return {
                'id': pending_approval.department.id,
                'name': pending_approval.department.name,
                'code': pending_approval.department.code,
                'approval_order': pending_approval.department.approval_order
            }
        
        return None
