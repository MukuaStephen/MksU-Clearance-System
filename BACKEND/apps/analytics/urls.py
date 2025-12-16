"""
URL Configuration for Analytics
"""
from django.urls import path
from apps.analytics.views import (
    ClearanceCompletionRateView,
    DepartmentBottlenecksView,
    FinancialSummaryView,
    OverallDashboardView
)

urlpatterns = [
    path('clearance-completion/', ClearanceCompletionRateView.as_view(), name='clearance-completion'),
    path('department-bottlenecks/', DepartmentBottlenecksView.as_view(), name='department-bottlenecks'),
    path('financial-summary/', FinancialSummaryView.as_view(), name='financial-summary'),
    path('dashboard/', OverallDashboardView.as_view(), name='dashboard'),
]
