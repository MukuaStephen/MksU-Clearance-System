"""
Serializers for Gown Issuance management
"""
from rest_framework import serializers
from apps.gown_issuance.models import GownIssuance
from apps.students.serializers import StudentSerializer
from decimal import Decimal


class GownIssuanceListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing gown issuances"""
    student_name = serializers.CharField(source='student.user.full_name', read_only=True)
    registration_number = serializers.CharField(source='student.registration_number', read_only=True)
    issued_by_name = serializers.CharField(source='issued_by.full_name', read_only=True, allow_null=True)
    is_overdue = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = GownIssuance
        fields = [
            'id',
            'student_name',
            'registration_number',
            'gown_number',
            'gown_size',
            'status',
            'deposit_paid',
            'issued_date',
            'expected_return_date',
            'is_overdue',
            'issued_by_name',
        ]
        read_only_fields = ['id']


class GownIssuanceSerializer(serializers.ModelSerializer):
    """Full serializer for gown issuance CRUD operations"""
    student = StudentSerializer(read_only=True)
    student_id = serializers.UUIDField(write_only=True, required=False)
    issued_by_name = serializers.CharField(source='issued_by.full_name', read_only=True, allow_null=True)
    returned_to_name = serializers.CharField(source='returned_to.full_name', read_only=True, allow_null=True)
    is_overdue = serializers.BooleanField(read_only=True)
    days_overdue = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = GownIssuance
        fields = [
            'id',
            'student',
            'student_id',
            'gown_number',
            'gown_size',
            'deposit_amount',
            'deposit_paid',
            'deposit_receipt',
            'issued_date',
            'issued_by',
            'issued_by_name',
            'expected_return_date',
            'actual_return_date',
            'returned_to',
            'returned_to_name',
            'status',
            'condition_notes',
            'deposit_refunded',
            'refund_amount',
            'refund_date',
            'is_overdue',
            'days_overdue',
            'notes',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'id',
            'issued_by',
            'returned_to',
            'actual_return_date',
            'refund_date',
            'is_overdue',
            'days_overdue',
            'created_at',
            'updated_at'
        ]
    
    def validate_student_id(self, value):
        """Validate student exists and doesn't have existing gown issuance"""
        from apps.students.models import Student
        
        try:
            student = Student.objects.get(id=value)
        except Student.DoesNotExist:
            raise serializers.ValidationError("Student not found")
        
        # Check if student already has a gown issued
        if GownIssuance.objects.filter(student=student).exists():
            if self.instance and self.instance.student == student:
                return value
            raise serializers.ValidationError(
                "Gown already issued to this student"
            )
        
        return value
    
    def validate_gown_number(self, value):
        """Validate gown number is unique"""
        if self.instance:
            if GownIssuance.objects.exclude(pk=self.instance.pk).filter(gown_number=value).exists():
                raise serializers.ValidationError("Gown number already in use")
        else:
            if GownIssuance.objects.filter(gown_number=value).exists():
                raise serializers.ValidationError("Gown number already in use")
        return value
    
    def validate_refund_amount(self, value):
        """Validate refund amount doesn't exceed deposit"""
        if value is not None:
            deposit = self.instance.deposit_amount if self.instance else Decimal('2000.00')
            if value > deposit:
                raise serializers.ValidationError("Refund amount cannot exceed deposit amount")
        return value


class GownReturnSerializer(serializers.Serializer):
    """Serializer for marking gown as returned"""
    condition_notes = serializers.CharField(required=False, allow_blank=True)
    
    def validate(self, attrs):
        """Validate return action"""
        return attrs


class GownRefundSerializer(serializers.Serializer):
    """Serializer for processing deposit refund"""
    refund_amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    
    def validate_refund_amount(self, value):
        """Validate refund amount"""
        if value <= 0:
            raise serializers.ValidationError("Refund amount must be greater than zero")
        return value
