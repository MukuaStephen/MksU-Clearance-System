from django.contrib import admin
from .models import ClearanceRequest


@admin.register(ClearanceRequest)
class ClearanceRequestAdmin(admin.ModelAdmin):
    """Admin interface for ClearanceRequest model"""
    list_display = ('student', 'status', 'submission_date', 'completion_date', 'get_completion_percentage')
    list_filter = ('status', 'submission_date', 'completion_date')
    search_fields = ('student__registration_number', 'student__user__full_name')
    readonly_fields = ('id', 'submission_date', 'created_at', 'updated_at', 'get_completion_percentage')
    
    fieldsets = (
        ('Request Info', {'fields': ('id', 'student')}),
        ('Status', {'fields': ('status', 'completion_date', 'get_completion_percentage')}),
        ('Rejection', {'fields': ('rejection_reason',)}),
        ('Timestamps', {'fields': ('submission_date', 'created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
