"""
URL Configuration for Finance app
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.finance.views import PaymentViewSet, mpesa_callback

app_name = 'finance'

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('', include(router.urls)),
    path('mpesa_callback/', mpesa_callback, name='mpesa_callback'),
]
