from django.contrib import admin
from .models import Department


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """Admin interface for Department model"""
    list_display = ('name', 'code', 'department_type', 'approval_order', 'is_active')
    list_filter = ('department_type', 'is_active', 'approval_order')
    search_fields = ('name', 'code', 'head_email')
    readonly_fields = ('id', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Department Info', {'fields': ('id', 'name', 'code', 'department_type')}),
        ('Contact', {'fields': ('head_email',)}),
        ('Configuration', {'fields': ('approval_order', 'is_active')}),
        ('Description', {'fields': ('description',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
