"""
URL Configuration for Students app
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.students.views import StudentViewSet

app_name = 'students'

router = DefaultRouter()
router.register(r'', StudentViewSet, basename='student')

urlpatterns = [
    path('', include(router.urls)),
]
