"""
Serializers for Department management
"""
from rest_framework import serializers
from apps.departments.models import Department


class DepartmentSerializer(serializers.ModelSerializer):
    """
    Serializer for Department CRUD operations
    Read access for all authenticated users
    Write access for admins only
    """
    
    class Meta:
        model = Department
        fields = [
            'id',
            'name',
            'code',
            'department_type',
            'approval_order',
            'contact_email',
            'contact_phone',
            'is_active',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_code(self, value):
        """Ensure department code is uppercase"""
        return value.upper()
    
    def validate_contact_email(self, value):
        """Validate email format"""
        if value:
            value = value.lower()
        return value
    
    def validate_approval_order(self, value):
        """Ensure approval order is positive"""
        if value <= 0:
            raise serializers.ValidationError("Approval order must be a positive integer")
        return value
    
    def validate(self, attrs):
        """
        Additional validation
        """
        # Check for duplicate code
        code = attrs.get('code')
        if code:
            instance = self.instance
            existing = Department.objects.filter(code=code)
            
            if instance:
                # Exclude current instance in update
                existing = existing.exclude(id=instance.id)
            
            if existing.exists():
                raise serializers.ValidationError({
                    'code': 'Department with this code already exists'
                })
        
        return attrs


class DepartmentListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing departments
    """
    class Meta:
        model = Department
        fields = ['id', 'name', 'code', 'department_type', 'approval_order', 'is_active']


class DepartmentStaffSerializer(serializers.Serializer):
    """
    Serializer for listing department staff
    """
    id = serializers.IntegerField()
    full_name = serializers.CharField()
    email = serializers.EmailField()
    admission_number = serializers.CharField()
    is_active = serializers.BooleanField()
