from django.contrib import admin
from .models import GownIssuance


@admin.register(GownIssuance)
class GownIssuanceAdmin(admin.ModelAdmin):
    """Admin interface for GownIssuance model"""
    list_display = ('gown_number', 'student', 'gown_size', 'status', 'deposit_paid', 'issued_date', 'expected_return_date', 'is_overdue')
    list_filter = ('status', 'deposit_paid', 'deposit_refunded', 'gown_size', 'issued_date')
    search_fields = ('gown_number', 'student__registration_number', 'student__user__full_name', 'deposit_receipt')
    readonly_fields = ('id', 'created_at', 'updated_at', 'is_overdue', 'days_overdue')
    
    fieldsets = (
        ('Student Info', {'fields': ('id', 'student')}),
        ('Gown Details', {'fields': ('gown_number', 'gown_size')}),
        ('Deposit', {'fields': ('deposit_amount', 'deposit_paid', 'deposit_receipt')}),
        ('Issuance', {'fields': ('issued_date', 'issued_by', 'expected_return_date')}),
        ('Return', {'fields': ('actual_return_date', 'returned_to', 'status', 'condition_notes')}),
        ('Refund', {'fields': ('deposit_refunded', 'refund_amount', 'refund_date')}),
        ('Status', {'fields': ('is_overdue', 'days_overdue')}),
        ('Notes', {'fields': ('notes',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
    
    def is_overdue(self, obj):
        return obj.is_overdue
    is_overdue.boolean = True
    is_overdue.short_description = 'Overdue'
