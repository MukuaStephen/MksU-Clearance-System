from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """Admin interface for Student model"""
    list_display = ('user', 'registration_number', 'admission_year', 'program', 'course', 'eligibility_status', 'created_at')
    list_filter = ('eligibility_status', 'admission_year', 'faculty', 'school', 'department', 'created_at')
    search_fields = ('registration_number', 'user__full_name', 'user__email')
    readonly_fields = ('id', 'created_at', 'updated_at')
    
    fieldsets = (
        ('User Info', {'fields': ('user',)}),
        ('Academic Info', {'fields': ('registration_number', 'admission_year', 'school', 'department', 'course', 'faculty', 'program', 'graduation_year')}),
        ('Status', {'fields': ('eligibility_status',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
