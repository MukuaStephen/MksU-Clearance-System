"""
URL Configuration for Departments app
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.departments.views import DepartmentViewSet

app_name = 'departments'

router = DefaultRouter()
router.register(r'', DepartmentViewSet, basename='department')

urlpatterns = [
    path('', include(router.urls)),
]
