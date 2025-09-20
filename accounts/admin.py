"""
Admin configuration for accounts app
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Department, StudentProfile, Faculty

# Unregister the default User admin
admin.site.unregister(User)

class StudentProfileInline(admin.StackedInline):
    """Inline admin for student profile"""
    model = StudentProfile
    can_delete = False
    verbose_name_plural = 'Student Profile'

class FacultyInline(admin.StackedInline):
    """Inline admin for faculty profile"""
    model = Faculty
    can_delete = False
    verbose_name_plural = 'Faculty Profile'

class CustomUserAdmin(UserAdmin):
    """Custom user admin with profile inlines"""
    inlines = (StudentProfileInline, FacultyInline)
    
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)

# Register the custom User admin
admin.site.register(User, CustomUserAdmin)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """Admin interface for departments"""
    list_display = ['name', 'code', 'head_of_department', 'established_year']
    list_filter = ['established_year']
    search_fields = ['name', 'code']
    ordering = ['name']

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    """Admin interface for student profiles"""
    list_display = ['user', 'student_id', 'department', 'year', 'enrollment_date', 'is_active']
    list_filter = ['department', 'year', 'is_active', 'enrollment_date']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'student_id']
    readonly_fields = ['enrollment_date']
    ordering = ['-enrollment_date']

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    """Admin interface for faculty"""
    list_display = ['user', 'employee_id', 'department', 'designation', 'is_featured', 'join_date']
    list_filter = ['department', 'designation', 'is_featured', 'join_date']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'employee_id']
    readonly_fields = ['join_date']
    ordering = ['-join_date']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'employee_id', 'department', 'designation')
        }),
        ('Professional Details', {
            'fields': ('specialization', 'qualification', 'experience_years', 'is_featured')
        }),
        ('Contact Information', {
            'fields': ('phone', 'office_room', 'office_hours')
        }),
        ('Profile', {
            'fields': ('profile_picture', 'bio', 'research_interests', 'publications')
        }),
        ('System', {
            'fields': ('join_date',),
            'classes': ('collapse',)
        })
    )