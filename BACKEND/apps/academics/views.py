"""
Views for Academic entities (read-only endpoints for UI dropdowns)
"""
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from apps.academics.models import School, AcademicDepartment, Course
from apps.academics.serializers import (
    SchoolSerializer,
    AcademicDepartmentSerializer,
    CourseSerializer
)


class SchoolViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only ViewSet for Schools
    
    Permissions:
    - List/Retrieve: Any authenticated user
    """
    queryset = School.objects.filter(is_active=True).order_by('name')
    serializer_class = SchoolSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'code']
    search_fields = ['name', 'code']
    ordering_fields = ['name', 'code']
    ordering = ['name']


class AcademicDepartmentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only ViewSet for Academic Departments
    
    Permissions:
    - List/Retrieve: Any authenticated user
    """
    queryset = AcademicDepartment.objects.select_related('school').filter(is_active=True).order_by('school__name', 'name')
    serializer_class = AcademicDepartmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'school', 'code']
    search_fields = ['name', 'code', 'school__name', 'school__code']
    ordering_fields = ['name', 'code', 'school__name']
    ordering = ['school__name', 'name']


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only ViewSet for Courses
    
    Permissions:
    - List/Retrieve: Any authenticated user
    """
    queryset = Course.objects.select_related('department', 'department__school').filter(is_active=True).order_by('department__school__name', 'department__name', 'name')
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'department', 'department__school', 'code', 'duration_years']
    search_fields = ['name', 'code', 'department__name', 'department__school__name']
    ordering_fields = ['name', 'code', 'duration_years']
    ordering = ['department__school__name', 'department__name', 'name']
