"""
URL Configuration for Approvals app
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.approvals.views import ClearanceApprovalViewSet

app_name = 'approvals'

router = DefaultRouter()
router.register(r'', ClearanceApprovalViewSet, basename='approval')

urlpatterns = [
    path('', include(router.urls)),
]
