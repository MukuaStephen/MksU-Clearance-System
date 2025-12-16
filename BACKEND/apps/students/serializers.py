"""
Serializers for Student model
"""
from rest_framework import serializers
from apps.students.models import Student
from apps.academics.models import School, AcademicDepartment, Course
from apps.users.serializers import UserSerializer


class StudentSerializer(serializers.ModelSerializer):
    """Serializer for Student model"""
    
    user = UserSerializer(read_only=True)
    user_email = serializers.EmailField(write_only=True, required=False)
    school = serializers.PrimaryKeyRelatedField(queryset=School.objects.all(), required=False, allow_null=True)
    department = serializers.PrimaryKeyRelatedField(queryset=AcademicDepartment.objects.all(), required=False, allow_null=True)
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), required=False, allow_null=True)
    
    class Meta:
        model = Student
        fields = [
            'id', 'user', 'user_email', 'registration_number', 'admission_year',
            'school', 'department', 'course',
            'faculty', 'program', 'graduation_year',
            'eligibility_status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'admission_year', 'created_at', 'updated_at']
    
    def validate_registration_number(self, value):
        """Validate registration number uniqueness"""
        if self.instance:
            # Update case - exclude current instance
            if Student.objects.exclude(pk=self.instance.pk).filter(registration_number=value).exists():
                raise serializers.ValidationError("Student with this registration number already exists.")
        else:
            # Create case
            if Student.objects.filter(registration_number=value).exists():
                raise serializers.ValidationError("Student with this registration number already exists.")
        return value


class StudentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a student with user account"""
    
    # User fields
    email = serializers.EmailField(required=True)
    full_name = serializers.CharField(required=True, max_length=255)
    admission_number = serializers.CharField(required=True, max_length=50)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    class Meta:
        model = Student
        fields = [
            'email', 'full_name', 'admission_number', 'password',
            'registration_number', 'admission_year',
            'school', 'department', 'course',
            'faculty', 'program',
            'graduation_year', 'eligibility_status'
        ]
        read_only_fields = ['admission_year']
    
    def create(self, validated_data):
        """Create user and student in one transaction"""
        from apps.users.models import User
        from django.db import transaction
        
        # Extract user fields
        email = validated_data.pop('email')
        full_name = validated_data.pop('full_name')
        admission_number = validated_data.pop('admission_number')
        password = validated_data.pop('password')
        
        with transaction.atomic():
            # Create user
            user = User.objects.create_user(
                username=email,
                email=email,
                full_name=full_name,
                admission_number=admission_number,
                password=password,
                role='student'
            )
            
            # Create student
            student = Student.objects.create(
                user=user,
                **validated_data
            )
        
        return student
