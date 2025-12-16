"""
Serializers for Clearance Approval management
"""
from rest_framework import serializers
from apps.approvals.models import ClearanceApproval
from apps.clearances.models import ClearanceRequest
from apps.departments.models import Department


class ClearanceApprovalListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing approvals
    """
    student_name = serializers.CharField(source='clearance_request.student.user.full_name', read_only=True)
    registration_number = serializers.CharField(source='clearance_request.student.registration_number', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.full_name', read_only=True, allow_null=True)
    
    class Meta:
        model = ClearanceApproval
        fields = [
            'id',
            'clearance_request',
            'student_name',
            'registration_number',
            'department_name',
            'status',
            'approved_by_name',
            'approval_date',
            'evidence_file',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class ClearanceApprovalSerializer(serializers.ModelSerializer):
    """
    Full serializer for approval CRUD operations
    """
    department_name = serializers.CharField(source='department.name', read_only=True)
    department_code = serializers.CharField(source='department.code', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.full_name', read_only=True, allow_null=True)
    student_info = serializers.SerializerMethodField()
    clearance_status = serializers.CharField(source='clearance_request.status', read_only=True)
    
    class Meta:
        model = ClearanceApproval
        fields = [
            'id',
            'clearance_request',
            'department',
            'department_name',
            'department_code',
            'status',
            'approved_by',
            'approved_by_name',
            'approval_date',
            'rejection_reason',
            'notes',
            'evidence_file',
            'student_info',
            'clearance_status',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'approved_by', 'approval_date', 'created_at', 'updated_at']
    
    def get_student_info(self, obj):
        """Get student information"""
        student = obj.clearance_request.student
        return {
            'id': student.id,
            'full_name': student.user.full_name,
            'email': student.user.email,
            'admission_number': student.user.admission_number,
            'registration_number': student.registration_number,
            'faculty': student.faculty,
            'program': student.program,
            'graduation_year': student.graduation_year
        }


class ApprovalActionSerializer(serializers.Serializer):
    """
    Serializer for approve/reject actions
    """
    action = serializers.ChoiceField(choices=['approve', 'reject'], required=True)
    notes = serializers.CharField(required=False, allow_blank=True)
    rejection_reason = serializers.CharField(required=False, allow_blank=True)
    
    def validate(self, attrs):
        """Validate action data"""
        action = attrs.get('action')
        rejection_reason = attrs.get('rejection_reason', '')
        
        # Rejection requires a reason
        if action == 'reject' and not rejection_reason:
            raise serializers.ValidationError({
                'rejection_reason': 'Rejection reason is required when rejecting'
            })
        
        return attrs


class BulkApprovalSerializer(serializers.Serializer):
    """
    Serializer for bulk approval actions
    """
    approval_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=True,
        min_length=1
    )
    action = serializers.ChoiceField(choices=['approve', 'reject'], required=True)
    notes = serializers.CharField(required=False, allow_blank=True)
    rejection_reason = serializers.CharField(required=False, allow_blank=True)
    
    def validate(self, attrs):
        """Validate bulk action data"""
        action = attrs.get('action')
        rejection_reason = attrs.get('rejection_reason', '')
        
        # Rejection requires a reason
        if action == 'reject' and not rejection_reason:
            raise serializers.ValidationError({
                'rejection_reason': 'Rejection reason is required when rejecting'
            })
        
        # Validate approval IDs exist and are accessible
        approval_ids = attrs.get('approval_ids', [])
        user = self.context.get('request').user
        
        # Check if approvals exist
        approvals = ClearanceApproval.objects.filter(id__in=approval_ids)
        
        if approvals.count() != len(approval_ids):
            raise serializers.ValidationError({
                'approval_ids': 'Some approval IDs are invalid'
            })
        
        # Department staff can only approve for their department
        if user.role == 'department_staff':
            if not user.department:
                raise serializers.ValidationError({
                    'error': 'No department assigned to your account'
                })
            
            invalid_approvals = approvals.exclude(department=user.department)
            if invalid_approvals.exists():
                raise serializers.ValidationError({
                    'approval_ids': 'You can only approve clearances for your department'
                })
        
        # Check if any approvals are already processed
        processed = approvals.exclude(status='pending')
        if processed.exists():
            raise serializers.ValidationError({
                'approval_ids': f'{processed.count()} approval(s) are already processed'
            })
        
        return attrs


class ApprovalStatisticsSerializer(serializers.Serializer):
    """
    Serializer for approval statistics
    """
    department = serializers.CharField()
    total_approvals = serializers.IntegerField()
    pending_count = serializers.IntegerField()
    approved_count = serializers.IntegerField()
    rejected_count = serializers.IntegerField()
    approval_rate = serializers.FloatField()
    average_approval_time = serializers.FloatField(allow_null=True)
