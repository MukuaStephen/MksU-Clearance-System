"""
Serializers for Academic entities (School, AcademicDepartment, Course)
"""
from rest_framework import serializers
from apps.academics.models import School, AcademicDepartment, Course


class SchoolSerializer(serializers.ModelSerializer):
    """Serializer for School model"""
    
    class Meta:
        model = School
        fields = [
            'id',
            'name',
            'code',
            'dean_email',
            'description',
            'is_active',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AcademicDepartmentSerializer(serializers.ModelSerializer):
    """Serializer for AcademicDepartment model"""
    school_name = serializers.CharField(source='school.name', read_only=True)
    school_code = serializers.CharField(source='school.code', read_only=True)
    
    class Meta:
        model = AcademicDepartment
        fields = [
            'id',
            'school',
            'school_name',
            'school_code',
            'name',
            'code',
            'head_email',
            'is_active',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CourseSerializer(serializers.ModelSerializer):
    """Serializer for Course model"""
    department_name = serializers.CharField(source='department.name', read_only=True)
    department_code = serializers.CharField(source='department.code', read_only=True)
    school_name = serializers.CharField(source='department.school.name', read_only=True)
    school_code = serializers.CharField(source='department.school.code', read_only=True)
    
    class Meta:
        model = Course
        fields = [
            'id',
            'department',
            'department_name',
            'department_code',
            'school_name',
            'school_code',
            'code',
            'name',
            'duration_years',
            'is_active',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
