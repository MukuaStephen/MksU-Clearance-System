"""
URL Configuration for Clearances app
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.clearances.views import ClearanceRequestViewSet

app_name = 'clearances'

router = DefaultRouter()
router.register(r'', ClearanceRequestViewSet, basename='clearance')

urlpatterns = [
    path('', include(router.urls)),
]
