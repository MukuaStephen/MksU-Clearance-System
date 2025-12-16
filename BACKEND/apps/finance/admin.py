from django.contrib import admin
from .models import FinanceRecord, Payment


@admin.register(FinanceRecord)
class FinanceRecordAdmin(admin.ModelAdmin):
    """Admin interface for FinanceRecord model"""
    list_display = ('student', 'graduation_fee_status', 'tuition_balance', 'last_verified_date')
    list_filter = ('graduation_fee_status', 'last_verified_date')
    search_fields = ('student__registration_number', 'student__user__full_name', 'mpesa_code')
    readonly_fields = ('id', 'created_at', 'updated_at', 'last_verified_date')
    
    fieldsets = (
        ('Student Info', {'fields': ('id', 'student')}),
        ('Finance', {'fields': ('tuition_balance', 'graduation_fee')}),
        ('Payment Status', {'fields': ('graduation_fee_status', 'mpesa_code', 'mpesa_payment_date')}),
        ('Verification', {'fields': ('verified_by', 'last_verified_date')}),
        ('Notes', {'fields': ('notes',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Admin interface for Payment model"""
    list_display = ('student', 'amount', 'graduation_fee_amount', 'payment_method', 'transaction_id', 'is_verified', 'payment_date')
    list_filter = ('is_verified', 'payment_method', 'payment_date', 'verification_date')
    search_fields = ('student__registration_number', 'student__user__full_name', 'transaction_id', 'phone_number')
    readonly_fields = ('id', 'graduation_fee_amount', 'verification_date', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Student Info', {'fields': ('id', 'student')}),
        ('Payment Details', {'fields': ('amount', 'graduation_fee_amount', 'payment_method', 'transaction_id', 'phone_number', 'payment_date')}),
        ('Verification', {'fields': ('is_verified', 'verified_by', 'verification_date')}),
        ('Documents', {'fields': ('receipt', 'fee_statement')}),
        ('Notes', {'fields': ('notes',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
