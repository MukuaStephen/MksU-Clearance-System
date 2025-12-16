from django.contrib import admin
from .models import ClearanceApproval


@admin.register(ClearanceApproval)
class ClearanceApprovalAdmin(admin.ModelAdmin):
    """Admin interface for ClearanceApproval model"""
    list_display = ('clearance_request', 'department', 'status', 'approved_by', 'approval_date')
    list_filter = ('status', 'department', 'approval_date')
    search_fields = ('clearance_request__student__registration_number', 'department__name')
    readonly_fields = ('id', 'created_at', 'updated_at', 'approval_date')
    
    fieldsets = (
        ('Request Info', {'fields': ('id', 'clearance_request', 'department')}),
        ('Approval', {'fields': ('status', 'approved_by', 'approval_date')}),
        ('Details', {'fields': ('rejection_reason', 'notes', 'evidence_file')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
