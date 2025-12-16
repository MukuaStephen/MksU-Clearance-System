"""
URL Configuration for Academics
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.academics.views import (
    SchoolViewSet,
    AcademicDepartmentViewSet,
    CourseViewSet
)

router = DefaultRouter()
router.register(r'schools', SchoolViewSet, basename='school')
router.register(r'departments', AcademicDepartmentViewSet, basename='academic-department')
router.register(r'courses', CourseViewSet, basename='course')

urlpatterns = [
    path('', include(router.urls)),
]
