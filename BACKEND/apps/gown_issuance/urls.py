"""
URL Configuration for Gown Issuance
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.gown_issuance.views import GownIssuanceViewSet

router = DefaultRouter()
router.register(r'', GownIssuanceViewSet, basename='gown-issuance')

urlpatterns = [
    path('', include(router.urls)),
]
