from django.contrib import admin
from .models import School, AcademicDepartment, Course


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'dean_email', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'code')


@admin.register(AcademicDepartment)
class AcademicDepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'school', 'head_email', 'is_active')
    list_filter = ('school', 'is_active')
    search_fields = ('name', 'code', 'school__name', 'school__code')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'department', 'is_active', 'duration_years')
    list_filter = ('department__school', 'department', 'is_active')
    search_fields = ('name', 'code', 'department__name', 'department__school__name')
