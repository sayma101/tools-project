"""
Admin configuration for courses app
"""
from django.contrib import admin
from .models import Course, Enrollment, Assignment, Material

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Admin interface for courses"""
    list_display = ['code', 'name', 'department', 'instructor', 'credits', 'semester', 'year', 'is_active', 'is_featured']
    list_filter = ['department', 'level', 'semester', 'year', 'is_active', 'is_featured']
    search_fields = ['name', 'code', 'instructor__user__first_name', 'instructor__user__last_name']
    ordering = ['department', 'code']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code', 'description', 'department', 'instructor')
        }),
        ('Course Details', {
            'fields': ('credits', 'level', 'semester', 'year', 'max_students')
        }),
        ('Schedule & Location', {
            'fields': ('schedule', 'classroom')
        }),
        ('Prerequisites & Materials', {
            'fields': ('prerequisites', 'syllabus')
        }),
        ('Status', {
            'fields': ('is_active', 'is_featured')
        })
    )
    
    filter_horizontal = ['prerequisites']

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    """Admin interface for enrollments"""
    list_display = ['student', 'course', 'enrollment_date', 'status', 'grade', 'is_active']
    list_filter = ['status', 'is_active', 'enrollment_date', 'course__department']
    search_fields = ['student__user__first_name', 'student__user__last_name', 'course__name', 'course__code']
    readonly_fields = ['enrollment_date']
    ordering = ['-enrollment_date']

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    """Admin interface for assignments"""
    list_display = ['title', 'course', 'due_date', 'max_points', 'is_published']
    list_filter = ['is_published', 'due_date', 'course__department']
    search_fields = ['title', 'course__name', 'course__code']
    ordering = ['due_date']

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    """Admin interface for course materials"""
    list_display = ['title', 'course', 'material_type', 'is_published', 'upload_date']
    list_filter = ['material_type', 'is_published', 'upload_date', 'course__department']
    search_fields = ['title', 'course__name', 'course__code']
    ordering = ['-upload_date']