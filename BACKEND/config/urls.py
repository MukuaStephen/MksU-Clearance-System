"""
URL Configuration for Machakos Clearance System
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

class HealthCheckView(APIView):
    """Health check endpoint"""
    def get(self, request):
        return Response({
            'status': 'healthy',
            'service': 'Machakos Clearance System API'
        }, status=status.HTTP_200_OK)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/health/', HealthCheckView.as_view(), name='health-check'),
    # OpenAPI schema & docs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # API endpoints (to be added)
    path('api/auth/', include('apps.users.urls')),
    path('api/students/', include('apps.students.urls')),
    path('api/departments/', include('apps.departments.urls')),
    path('api/clearances/', include('apps.clearances.urls')),
    path('api/approvals/', include('apps.approvals.urls')),
    path('api/finance/', include('apps.finance.urls')),
    path('api/notifications/', include('apps.notifications.urls')),
    path('api/audit-logs/', include('apps.audit_logs.urls')),
    path('api/gown-issuances/', include('apps.gown_issuance.urls')),
    path('api/analytics/', include('apps.analytics.urls')),
    path('api/academics/', include('apps.academics.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
