from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    """Admin interface for AuditLog model"""
    list_display = ('actor', 'action', 'entity', 'created_at', 'ip_address')
    list_filter = ('action', 'entity', 'created_at')
    search_fields = ('actor__email', 'entity', 'entity_id', 'ip_address')
    readonly_fields = ('id', 'created_at')
    
    fieldsets = (
        ('Actor', {'fields': ('id', 'actor')}),
        ('Action', {'fields': ('action', 'description')}),
        ('Entity', {'fields': ('entity', 'entity_id')}),
        ('Changes', {'fields': ('changes',)}),
        ('Source', {'fields': ('ip_address',)}),
        ('Timestamps', {'fields': ('created_at',), 'classes': ('collapse',)}),
    )
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
